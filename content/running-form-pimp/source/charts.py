"""Gindre 2026 표2(p.2127) 수치로 속도-접지 시간 그래프를 HTML(인라인 SVG + Noto Sans KR)로 만든다.
render_charts.cjs가 PNG(assets/charts/)로 렌더 → 카드에서는 <img>로 사용(PPTX에도 그림으로 들어감).
x축은 빠름(왼쪽) → 느림(오른쪽)으로 뒤집어 '느려질수록 오래 딛는다'가 왼→오 상승으로 읽히게 한다.
점은 표2의 거리별 값 그대로, 점 사이 직선(보간 없음). 같은 속도의 중복값(100·200 m, 마라톤·50 km)은 한 점."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'charts'
OUT.mkdir(exist_ok=True)
FONT = (HERE / '../../../templates/fonts/NotoSansKR-VF.ttf').resolve().as_uri()

# (거리, 속도 km/h, 접지 ms) — 표2, 남성 아마추어 러너 추정치
DATA = [('100·200 m', 18.0, 190), ('400 m', 15.7, 210), ('800 m', 13.5, 230), ('1500 m', 12.5, 250),
        ('3000 m', 11.8, 250), ('하프', 10.6, 275), ('10 km', 10.5, 275), ('마라톤', 10.0, 285),
        ('5 km', 9.6, 295), ('100 km', 8.2, 320), ('160 km', 7.1, 330)]
W, H = 888, 680
L, R, T, B = 104, 40, 70, 560
INK, MUTED, BLUE, GRID = '#121416', '#5e6570', '#0879d8', '#e3e9ee'
VMAX, VMIN = 19, 6       # 왼쪽이 빠름
CMIN, CMAX = 150, 350


def X(v): return L + (W - L - R) * (VMAX - v) / (VMAX - VMIN)
def Y(c): return B - (B - T) * (c - CMIN) / (CMAX - CMIN)


def page(svg):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>@font-face{{font-family:"Noto Sans KR";src:url("{FONT}");font-weight:100 900}}'
            f'html,body{{margin:0;background:#fff}}svg{{display:block;font-family:"Noto Sans KR"}}</style></head><body>'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{svg}</svg></body></html>')


def chart():
    s = []
    for c in (200, 250, 300, 350):
        s.append(f'<line x1="{L}" x2="{W - R}" y1="{Y(c)}" y2="{Y(c)}" stroke="{GRID}" stroke-width="2"/>')
        s.append(f'<text x="{L - 16}" y="{Y(c) + 11}" text-anchor="end" font-size="30" fill="{MUTED}">{c}</text>')
    s.append(f'<text x="4" y="{T - 30}" text-anchor="start" font-size="28" font-weight="650" fill="{MUTED}">접지 ms</text>')
    for v in (18, 14, 10, 7):
        s.append(f'<text x="{X(v)}" y="{B + 46}" text-anchor="middle" font-size="30" font-weight="650" fill="{INK}">{v}</text>')
    s.append(f'<text x="{L}" y="{B + 98}" text-anchor="start" font-size="30" font-weight="650" fill="{MUTED}">← 빠름</text>')
    s.append(f'<text x="{(L + W - R) / 2}" y="{B + 98}" text-anchor="middle" font-size="30" fill="{MUTED}">속도 km/h</text>')
    s.append(f'<text x="{W - R}" y="{B + 98}" text-anchor="end" font-size="30" font-weight="650" fill="{MUTED}">느림 →</text>')
    pts = ' '.join(f'{X(v):.1f},{Y(c):.1f}' for _, v, c in DATA)
    s.append(f'<polyline points="{pts}" fill="none" stroke="{BLUE}" stroke-width="7" stroke-linejoin="round"/>')
    for _, v, c in DATA:
        s.append(f'<circle cx="{X(v):.1f}" cy="{Y(c):.1f}" r="9" fill="{BLUE}"/>')
    # 강조 라벨 3개
    for name, v, c, dx, dy, anchor in (('단거리', 18.0, 190, 24, 44, 'start'), ('마라톤', 10.0, 285, 24, 70, 'start'),
                                         ('160 km', 7.1, 330, 0, -70, 'end')):
        x, y = X(v) + dx, Y(c) + dy
        s.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="32" font-weight="800" fill="{INK}">{name}</text>')
        s.append(f'<text x="{x}" y="{y + 38}" text-anchor="{anchor}" font-size="32" font-weight="650" fill="{BLUE}">약 {c}ms</text>')
    return page(''.join(s))


(OUT / 'speed-contact.html').write_text(chart(), encoding='utf-8')
print('chart html written')
