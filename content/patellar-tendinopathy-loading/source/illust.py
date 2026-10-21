"""2·3장 물컵 비유 그림과 5장 힘-시간 개념 그래프를 HTML(인라인 SVG)로 만든다.
render_illust.cjs가 PNG(assets/illust/, 2배 해상도)로 렌더 → 카드에서는 <img>로 사용(PPTX에도 그림으로 들어감).
물컵은 2026-10-21 사용자 지시(물컵 그림)로 그린 비유 그림이다. 글자는 넣지 않고 카드 HTML에서 쓴다.
힘-시간 곡선은 개념 설명용 모식도이며 실제 측정값이 아니다.
사용: python3 source/illust.py && node source/render_illust.cjs"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'illust'
INK, MUTED, BLUE, WATER, FAINT, GRID = '#121416', '#5e6570', '#0879d8', '#bfe0f7', '#c3ccd4', '#e3e9ee'


def page(w, h, svg):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:#fff}}svg{{display:block}}</style></head><body>'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{svg}</svg></body></html>')


def cup(cx, base, w, h, fill, overflow=False):
    """컵: 위 폭 w, 아래 폭 0.78w, 높이 h, 바닥 y=base. fill = 물 높이 비율(0~1)."""
    tl, tr = cx - w / 2, cx + w / 2
    bl, br = cx - w * .39, cx + w * .39
    top = base - h
    s = []
    if overflow:
        # 위에서 쏟아지는 물줄기
        s.append(f'<path d="M{cx - w * .07:.1f},0 L{cx + w * .07:.1f},0 L{cx + w * .1:.1f},{top - 20:.1f} L{cx - w * .1:.1f},{top - 20:.1f} Z" fill="{BLUE}" opacity=".8"/>')
        # 바닥에 고인 물
        s.append(f'<ellipse cx="{cx}" cy="{base + 4}" rx="{w * .95:.1f}" ry="14" fill="{WATER}"/>')
    # 물(컵 안쪽 사다리꼴 일부)
    wl = top + h * (1 - fill)
    k = (wl - top) / h  # 물 높이에서의 폭 보간
    xl, xr = tl + (bl - tl) * k, tr + (br - tr) * k
    s.append(f'<path d="M{xl:.1f},{wl:.1f} L{xr:.1f},{wl:.1f} L{br - 4:.1f},{base - 4} L{bl + 4:.1f},{base - 4} Z" fill="{WATER}"/>')
    if overflow:
        # 가장자리 위로 부풀어 넘치는 수면과 양옆으로 흘러내리는 물
        s.append(f'<path d="M{tl - 6:.1f},{top + 2:.1f} Q{cx:.1f},{top - 34:.1f} {tr + 6:.1f},{top + 2:.1f} Z" fill="{WATER}"/>')
        for side in (-1, 1):
            x0 = cx + side * (w / 2 + 2)
            x1 = cx + side * (w * .39 + 14)
            s.append(f'<path d="M{x0:.1f},{top - 2:.1f} C{x0 + side * 22:.1f},{top + h * .25:.1f} {x1 + side * 10:.1f},{base - h * .45:.1f} {x1 + side * 6:.1f},{base:.1f}" '
                     f'fill="none" stroke="{WATER}" stroke-width="16" stroke-linecap="round"/>')
            s.append(f'<circle cx="{x0 + side * 46:.1f}" cy="{top + h * .18:.1f}" r="7" fill="{WATER}"/>')
            s.append(f'<circle cx="{x0 + side * 34:.1f}" cy="{top + h * .42:.1f}" r="5" fill="{WATER}"/>')
    else:
        s.append(f'<line x1="{xl + 3:.1f}" x2="{xr - 3:.1f}" y1="{wl:.1f}" y2="{wl:.1f}" stroke="{BLUE}" stroke-width="5" stroke-linecap="round"/>')
    # 유리 윤곽
    s.append(f'<path d="M{tl:.1f},{top:.1f} L{bl:.1f},{base} L{br:.1f},{base} L{tr:.1f},{top:.1f}" fill="none" stroke="{MUTED}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>')
    return ''.join(s)


def arrow(x0, x1, y):
    return (f'<line x1="{x0}" x2="{x1 - 14}" y1="{y}" y2="{y}" stroke="{FAINT}" stroke-width="7" stroke-linecap="round"/>'
            f'<path d="M{x1 - 22},{y - 16} L{x1},{y} L{x1 - 22},{y + 16}" fill="none" stroke="{FAINT}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')


def cups2():
    W, H = 888, 310
    return page(W, H, cup(222, 286, 190, 205, .55) + cup(666, 286, 190, 205, 1, overflow=True))


def ghost(cx, base, w, h):
    """이전 단계 컵 크기를 점선으로 겹쳐 그려 커진 정도를 보여준다."""
    tl, tr, bl, br, top = cx - w / 2, cx + w / 2, cx - w * .39, cx + w * .39, base - h
    return (f'<path d="M{tl:.1f},{top:.1f} L{bl:.1f},{base - 3} L{br:.1f},{base - 3} L{tr:.1f},{top:.1f}" fill="none" '
            f'stroke="{BLUE}" stroke-width="4" stroke-dasharray="10 9" stroke-linecap="round" opacity=".75"/>')


def cups3():
    W, H, base = 888, 420, 404
    sizes = [(92, 120, 140), (362, 210, 245), (716, 320, 370)]  # (cx, 위 폭, 높이)
    s = ''
    for i, (cx, w, h) in enumerate(sizes):
        s += cup(cx, base, w, h, .6)
        if i:
            s += ghost(cx, base, sizes[i - 1][1], sizes[i - 1][2])
    # 컵 위를 지나 오른쪽 위로 올라가는 성장 화살표
    pts = [(92, 236), (362, 138), (520, 72)]
    d = 'M' + ' L'.join(f'{x},{y}' for x, y in pts)
    s += f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2 16"/>'
    s += f'<path d="M{520 - 30},{72 - 1} L520,72 L{520 - 13},{72 + 27}" fill="none" stroke="{BLUE}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
    return page(W, H, s)


# 힘-시간 모식도: 272×220
GW, GH, L, R, T, B = 272, 220, 30, 258, 22, 196


def curve_pts(peak=1.0, rise=.35, n=60):
    """0→rise 구간 상승, 이후 하강하는 매끈한 곡선(개념용)."""
    import math
    pts = []
    for i in range(n + 1):
        t = i / n
        if t <= rise:
            v = math.sin(t / rise * math.pi / 2) ** 2
        else:
            v = math.cos((t - rise) / (1 - rise) * math.pi / 2) ** 1.6
        pts.append((L + 8 + (R - L - 16) * t, B - (B - T - 18) * v * peak))
    return pts


def path(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)


def axes():
    return (f'<line x1="{L}" y1="{T - 6}" x2="{L}" y2="{B}" stroke="{MUTED}" stroke-width="4" stroke-linecap="round"/>'
            f'<line x1="{L}" y1="{B}" x2="{R + 6}" y2="{B}" stroke="{MUTED}" stroke-width="4" stroke-linecap="round"/>')


def ft_peak():
    p = curve_pts()
    top = min(p, key=lambda q: q[1])
    s = axes() + f'<path d="{path(p)}" fill="none" stroke="{FAINT}" stroke-width="7" stroke-linejoin="round"/>'
    s += f'<line x1="{L}" x2="{top[0]:.1f}" y1="{top[1]:.1f}" y2="{top[1]:.1f}" stroke="{BLUE}" stroke-width="4" stroke-dasharray="8 7"/>'
    s += f'<circle cx="{top[0]:.1f}" cy="{top[1]:.1f}" r="13" fill="{BLUE}"/>'
    return page(GW, GH, s)


def ft_rate():
    p = curve_pts(rise=.22)
    k = next(i for i, q in enumerate(p) if q[1] == min(q[1] for q in p))
    s = axes() + f'<path d="{path(p)}" fill="none" stroke="{FAINT}" stroke-width="7" stroke-linejoin="round"/>'
    s += f'<path d="{path(p[:k + 1])}" fill="none" stroke="{BLUE}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'
    return page(GW, GH, s)


def ft_impulse():
    p = curve_pts(peak=.72, rise=.3)
    area = path(p) + f' L{p[-1][0]:.1f},{B} L{p[0][0]:.1f},{B} Z'
    s = axes() + f'<path d="{area}" fill="{WATER}"/>'
    s += f'<path d="{path(p)}" fill="none" stroke="{BLUE}" stroke-width="7" stroke-linejoin="round"/>'
    return page(GW, GH, s)


OUT.mkdir(exist_ok=True)
for name, fn in [('cups2', cups2), ('cups3', cups3), ('ft-peak', ft_peak), ('ft-rate', ft_rate), ('ft-impulse', ft_impulse)]:
    (OUT / f'{name}.html').write_text(fn(), encoding='utf-8')
print('ok')
