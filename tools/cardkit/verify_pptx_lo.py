"""PowerPoint가 없는 Linux(클라우드)용 대체 검사: LibreOffice로 PPTX를 렌더해 exports/ PNG와 비교한다.
verify_pptx.ps1과 같은 기준(세로 어긋남 ≤2px, 픽셀 차이 <8%, 상자 속성)이지만 PowerPoint 렌더가 아니므로
결과는 'LO-PASS'/'LO-FAIL'로만 기록하고 qa/pptx-check.json(PowerPoint PASS)은 만들지 않는다.
RCardnews 폰트는 ~/.fonts에 임시 복사 후 검사가 끝나면 지운다.
사용: python3 tools/cardkit/verify_pptx_lo.py content/<slug>"""
import json, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
from PIL import Image

ROOT = Path(sys.argv[1]).resolve()
PPTX = ROOT / f'adobe-express/{ROOT.name}-express.pptx'
OUT = ROOT / 'adobe-express/build/pptx-render-lo'
FONTS = Path(__file__).resolve().parents[2] / 'templates/fonts'
fontdir = Path.home() / '.fonts/rcardnews-verify'
fontdir.mkdir(parents=True, exist_ok=True)
for f in FONTS.glob('RCardnews-W*.ttf'):
    shutil.copy(f, fontdir)
subprocess.run(['fc-cache', '-f', str(fontdir)], capture_output=True)
warn = []
try:
    with zipfile.ZipFile(PPTX) as z:
        slides = sorted(n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n))
        for n in slides:
            x = z.read(n).decode('utf-8')
            for body in re.findall(r'<p:txBody>.*?</p:txBody>', x):
                if '<a:t' not in body:
                    continue
                if 'wrap="none"' not in body or '<a:noAutofit/>' not in body or body.count('<a:p>') != 1:
                    warn.append(f'{n}: wrap/autofit/paragraphs')
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', td, str(PPTX)], check=True, capture_output=True)
        pdf = Path(td) / (PPTX.stem + '.pdf')
        subprocess.run(['pdftoppm', '-png', '-scale-to-x', '1080', '-scale-to-y', '1350', str(pdf), str(OUT / 'p')], check=True)
finally:
    shutil.rmtree(fontdir, ignore_errors=True)
    subprocess.run(['fc-cache', '-f'], capture_output=True)
renders = sorted(OUT.glob('p-*.png'))
exports = sorted(p for p in (ROOT / 'exports').glob('*.png') if re.fullmatch(r'\d\d\.png', p.name))
if len(renders) != len(exports):
    warn.append(f'slide count {len(renders)} != PNG count {len(exports)}')


def profile(im):
    px = im.load()
    return [sum(1 for x in range(100, 980, 4) if px[x, y][0] < 120) for y in range(1350)]


rows, fail = [], bool(warn)
for e, r in zip(exports, renders):
    a, b = Image.open(e).convert('RGB'), Image.open(r).convert('RGB').resize((1080, 1350))
    pa, pb = a.load(), b.load()
    diff = total = 0
    for y in range(0, 1350, 3):
        for x in range(0, 1080, 3):
            p, q = pa[x, y], pb[x, y]; total += 1
            diff += sum(abs(p[i] - q[i]) for i in range(3)) > 120
    fa, fb = profile(a), profile(b)
    best = min(range(-10, 11), key=lambda d: sum((fa[y] - fb[y + d]) ** 2 for y in range(120, 1230)))
    ok = abs(best) <= 2 and diff / total < 0.08
    fail |= not ok
    rows.append({'card': e.stem, 'verticalShiftPx': best, 'diffPct': round(100 * diff / total, 2), 'pass': ok})
    b.save(OUT / f'{e.stem}.png')
for r in renders:
    r.unlink()
report = {'pptx': str(PPTX.relative_to(ROOT)), 'renderer': 'LibreOffice (PowerPoint 아님)', 'slides': len(renders), 'warnings': warn,
          'cards': rows, 'result': 'LO-FAIL' if fail else 'LO-PASS'}
(ROOT / 'qa/pptx-check-libreoffice.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
for r in rows:
    print(r)
print(warn or '', report['result'], '(LibreOffice 대체 검사. PowerPoint 검증 PASS가 아님)')
