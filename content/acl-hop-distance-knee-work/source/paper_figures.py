"""논문 그림·제목부를 원문 PDF에서 잘라 assets/paper/에 저장하고, 강조 테두리 좌표를 boxes.json에 기록한다.
원문 PDF는 저작권 때문에 저장소에 넣지 않는다(사용자 제공본을 인자로 준다).
사용: python3 content/acl-hop-distance-knee-work/source/paper_figures.py <Kotsifaki2022.pdf> <Aspetar2023.pdf>
- Kotsifaki A et al. BJSM 2022 (© Author(s), No commercial re-use): 1쪽 제목·저자, Figure 2(5쪽), Figure 3(6쪽)
- Kotsifaki R et al. BJSM 2023 (CC BY-NC 4.0): 1쪽 제목·저자, 9쪽(508) Box 5 Jumping biomechanics
자르기만 하고 그림 내용은 바꾸지 않는다. 강조 테두리는 카드 HTML에서 그림 위에 따로 얹는다."""
import json, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'assets/paper'
K22, G23 = (Path(p).resolve() for p in sys.argv[1:3])
DPI = 400
PT = DPI / 72  # 1pt → px


def render_crop(pdf, page, x0, y0, x1, y1, name):
    """PDF 쪽의 pt 좌표 영역을 400dpi로 렌더해 저장"""
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(['pdftoppm', '-png', '-r', str(DPI), '-f', str(page), '-l', str(page),
                        '-x', str(round(x0 * PT)), '-y', str(round(y0 * PT)),
                        '-W', str(round((x1 - x0) * PT)), '-H', str(round((y1 - y0) * PT)),
                        str(pdf), f'{td}/c'], check=True)
        Image.open(next(Path(td).glob('c*.png'))).convert('RGB').save(OUT / name)


def embedded(pdf, page, index):
    """쪽에 들어 있는 원본 래스터 그림(재압축 없이 PNG로)"""
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(['pdfimages', '-png', '-f', str(page), '-l', str(page), str(pdf), f'{td}/i'], check=True)
        return Image.open(sorted(Path(td).glob('i-*.png'))[index]).convert('RGB')


def teal_box(im, x0, y0, x1, y1, pad):
    """무릎(청록) 영역의 경계 상자 + 여유"""
    px = im.load()
    pts = [(x, y) for y in range(y0, y1, 2) for x in range(x0, x1, 2)
           if px[x, y][0] < 140 and px[x, y][1] > 170 and px[x, y][2] > 170]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return [max(min(xs) - pad, 0), max(min(ys) - pad, 0), min(max(xs) + pad, im.width), min(max(ys) + pad, im.height)]


OUT.mkdir(parents=True, exist_ok=True)
boxes = {}

# 02: Kotsifaki 2022 제목·저자 (1쪽)
render_crop(K22, 1, 140, 42, 552, 200, 'k2022-title.png')

# 03: Figure 3 도약(Propulsion) 패널만 (왼쪽 축 이름~Control 글자). 착지 패널은 x1032부터
fig3 = embedded(K22, 6, 0)
fig3.crop((0, 0, 872, fig3.height)).save(OUT / 'k2022-fig3-propulsion.png')
boxes['fig3_knee'] = teal_box(fig3, 0, 0, 872, fig3.height, 12)

# 04: Figure 2 위쪽(도약 일, J/kg)만. 가로 구분선 y1236 위
fig2 = embedded(K22, 5, 0)
fig2.crop((0, 0, fig2.width, 1234)).save(OUT / 'k2022-fig2-propulsion.png')
kb = teal_box(fig2, 0, 0, fig2.width, 1234, 0)
boxes['fig2_knee'] = [kb[0] - 70, kb[1] - 36, min(kb[2] + 150, fig2.width - 4), 1226]  # 'Knee' 이름표까지 포함

# 05(착지): Figure 3 착지(Landing) 패널(x1000~), Figure 2 아래쪽(착지 흡수 일, J/kg) 패널(가로 구분선 y1242 아래)
fig3.crop((1000, 0, fig3.width, fig3.height)).save(OUT / 'k2022-fig3-landing.png')
lb = teal_box(fig3, 1000, 0, fig3.width, fig3.height, 12)
# 아랫선은 세 막대 무릎 띠 아래끝 중 가장 높은 곳(대조군 13%)까지 — 더 내리면 비수술측·대조군 'Ankle' 글자를 가로지른다
low = min(teal_box(fig3, x0, 0, x0 + 200, fig3.height, 0)[3] for x0 in (1040, 1250, 1460))
boxes['fig3_landing_knee'] = [lb[0] - 1000, lb[1], min(lb[2] - 1000, fig3.width - 1000 - 4), low + 2]
fig2.crop((0, 1244, fig2.width, fig2.height)).save(OUT / 'k2022-fig2-landing.png')
kb = teal_box(fig2, 0, 1244, fig2.width, fig2.height, 0)
boxes['fig2_landing_knee'] = [kb[0] - 70, kb[1] - 1244 - 50, min(kb[2] + 150, fig2.width - 4), fig2.height - 1244 - 4]  # 'Knee' 이름표까지 포함

# 06: Aspetar 2023 Box 5 (9쪽, 508) — Return to sport/completion 머리글(전문 선수 최소 기준) + Jumping biomechanics 항목. 사이 항목은 생략
render_crop(G23, 9, 44, 336.0, 287, 414.9, 'g2023-box5-rts.png')
render_crop(G23, 9, 44, 624.2, 287, 667.4, 'g2023-box5-jumping.png')

# 07: Aspetar 2023 제목·저자 (1쪽) + Andreas Bjerregaard 이름 위치(pdftotext -bbox 실측, pt)
gx0, gy0 = 140, 40  # OPEN ACCESS 로고 제외 → 저자 글씨를 크게
render_crop(G23, 1, gx0, gy0, 552, 152, 'g2023-header.png')
ax0, ay0, ax1, ay1 = 241.97, 116.66, 338.6, 131.85  # 'Andreas' 시작 ~ 'Bjerregaard' 끝(쉼표 제외)
boxes['g2023_andreas'] = [round((ax0 - gx0) * PT) - 14, round((ay0 - gy0) * PT) - 8, round((ax1 - gx0) * PT) + 14, round((ay1 - gy0) * PT) + 10]

for f in sorted(OUT.glob('*.png')):
    boxes.setdefault('size', {})[f.name] = Image.open(f).size
(OUT / 'boxes.json').write_text(json.dumps(boxes, indent=1), encoding='utf-8')
print(json.dumps(boxes))
