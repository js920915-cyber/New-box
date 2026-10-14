"""Noto Sans KR 가변 폰트를 굵기별 정적 폰트로 고정하고 이름을 'RCardnews W{굵기}'로 통일한다.
각 파일을 독립 패밀리의 Regular(400)로 표기해 PowerPoint·Express가 굵게 처리나 패밀리 묶음을 하지 않게 한다. SIL OFL 1.1."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

FONTS = Path(__file__).resolve().parents[2] / 'templates/fonts'  # 한 번 만들어 모든 주제에서 재사용
SRC = FONTS / 'NotoSansKR-VF.ttf'
OUT = FONTS
OUT.mkdir(parents=True, exist_ok=True)
for old in OUT.glob('RCardnews-*.ttf'):
    old.unlink()

for w in (500, 650, 700, 750, 800, 850):
    font = instantiateVariableFont(TTFont(SRC), {'wght': w}, updateFontNames=False)
    family, ps = f'RCardnews W{w}', f'RCardnews-W{w}'
    name = font['name']
    for nid in (16, 17, 21, 22, 25):
        name.removeNames(nameID=nid)
    name.names = [n for n in name.names if not (n.platformID == 3 and n.langID != 0x409)]  # 한국어 'Noto Sans KR' 이름 제거
    if 'STAT' in font:
        del font['STAT']
    for nid, val in ((1, family), (2, 'Regular'), (3, f'{ps};2026'), (4, family), (6, ps)):
        name.setName(val, nid, 3, 1, 0x409)
        name.setName(val, nid, 1, 0, 0)
    font['OS/2'].usWeightClass = 400
    font['OS/2'].fsSelection = (font['OS/2'].fsSelection & ~0b1100001) | 0b1000000  # REGULAR, not bold/italic
    font['head'].macStyle = 0
    font.save(OUT / f'{ps}.ttf')
    print(ps, round((OUT / f'{ps}.ttf').stat().st_size / 1e6, 1), 'MB')
