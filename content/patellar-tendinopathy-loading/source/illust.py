"""2·3장 물컵 비유 그림과 5장 힘-시간 개념 그래프를 HTML(인라인 SVG)로 만든다.
render_illust.cjs가 PNG(assets/illust/, 2배 해상도)로 렌더 → 카드에서는 <img>로 사용(PPTX에도 그림으로 들어감).
물컵은 2026-10-21~22 사용자 지시(물컵 그림, 담긴 것=훈련, 넘치는 것=통증)로 그린 비유 그림이다.
글자는 넣지 않고 labels.json 좌표로 카드 HTML에서 얹는다(PPTX에서 편집 가능).
힘-시간 곡선은 개념 설명용 모식도이며 실제 측정값이 아니다.
사용: python3 source/illust.py && node source/render_illust.cjs"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'illust'
INK, MUTED, BLUE, WATER, FAINT, GRID = '#121416', '#5e6570', '#0879d8', '#bfe0f7', '#c3ccd4', '#e3e9ee'


def page(w, h, svg):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:#fff}}svg{{display:block}}</style></head><body>'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{svg}</svg></body></html>')


DEFS = """<defs>
<linearGradient id="glass" x1="0" x2="1"><stop offset="0" stop-color="#e4eef5" stop-opacity=".9"/><stop offset=".45" stop-color="#f7fbfd" stop-opacity=".5"/><stop offset="1" stop-color="#dbe7f0" stop-opacity=".9"/></linearGradient>
<linearGradient id="shade" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".35" stop-color="#fff" stop-opacity="0"/><stop offset=".8" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".14"/></linearGradient>
<linearGradient id="pain" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ef6b72"/><stop offset="1" stop-color="#cc414a"/></linearGradient>
<radialGradient id="puddle"><stop offset="0" stop-color="#e2545c"/><stop offset="1" stop-color="#cc414a" stop-opacity=".85"/></radialGradient>
<filter id="blur" x="-30%" y="-100%" width="160%" height="300%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>"""
RIM, BASE_T, WALL = '#8fa3b2', 16, 7   # 유리 윤곽색, 바닥 두께, 벽 두께
LAYERS = ['#1f7fd0', '#4fa3e3', '#86c3ef', '#b7dcf6']  # 아래층부터 (진한 → 연한)
WATER2 = '#8cc8f0'


class Glass:
    """원근(위·아래 타원)이 있는 유리컵. 위 폭 w, 바닥 폭 0.78w, 높이 h, 바닥 중심 y=base."""

    def __init__(self, cx, base, w, h):
        self.cx, self.base, self.w, self.h, self.top = cx, base, w, h, base - h
        self.lb = base - BASE_T  # 액체 바닥

    def hw(self, y):  # 바깥 반폭
        k = (y - self.top) / self.h
        return self.w / 2 + (self.w * .39 - self.w / 2) * k

    def ry(self, y):
        return self.hw(y) * .16

    def band(self, y0, y1, fill):
        """y0(위)~y1(아래) 액체 층: 위·아래 모두 앞쪽 타원 호."""
        r0, r1 = self.hw(y0) - WALL, self.hw(y1) - WALL
        c = self.cx
        return (f'<path d="M{c - r0:.1f},{y0:.1f} A{r0:.1f},{self.ry(y0):.1f} 0 0 0 {c + r0:.1f},{y0:.1f} '
                f'L{c + r1:.1f},{y1:.1f} A{r1:.1f},{self.ry(y1):.1f} 0 0 1 {c - r1:.1f},{y1:.1f} Z" fill="{fill}"/>')

    def surface(self, y, fill, op=1):
        r = self.hw(y) - WALL
        return f'<ellipse cx="{self.cx}" cy="{y:.1f}" rx="{r:.1f}" ry="{self.ry(y):.1f}" fill="{fill}" opacity="{op}"/>'

    def back(self):
        c, t, b = self.cx, self.top, self.base
        rt, rb = self.w / 2, self.w * .39
        s = f'<ellipse cx="{c}" cy="{b + 8}" rx="{rb * 1.3:.1f}" ry="{self.ry(b) * 1.2:.1f}" fill="#33414d" opacity=".16" filter="url(#blur)"/>'
        s += (f'<path d="M{c - rt:.1f},{t} L{c - rb:.1f},{b} A{rb:.1f},{self.ry(b):.1f} 0 0 0 {c + rb:.1f},{b} L{c + rt:.1f},{t} '
              f'A{rt:.1f},{self.ry(t):.1f} 0 0 0 {c - rt:.1f},{t} Z" fill="url(#glass)"/>')
        # 두꺼운 유리 바닥
        s += self.band(self.lb, b - 2, '#e3edf4')
        return s

    def liquid(self, levels, colors, surface=True):
        """levels: 아래부터 각 층의 윗면 y. 위층부터 그려 아래층의 앞 호가 경계가 된다."""
        s = ''
        for y, col in reversed(list(zip(levels, colors))):
            s += self.band(y, self.lb, col)
        s += self.band(levels[-1], self.lb, 'url(#shade)')
        if surface:
            s += self.surface(levels[-1], '#ffffff', .45)
        return s

    def front(self):
        c, t, b = self.cx, self.top, self.base
        rt, rb = self.w / 2, self.w * .39
        s = (f'<path d="M{c - rt:.1f},{t} L{c - rb:.1f},{b} A{rb:.1f},{self.ry(b):.1f} 0 0 0 {c + rb:.1f},{b} L{c + rt:.1f},{t}" '
             f'fill="none" stroke="{RIM}" stroke-width="4" stroke-linejoin="round"/>')
        s += f'<ellipse cx="{c}" cy="{t}" rx="{rt:.1f}" ry="{self.ry(t):.1f}" fill="none" stroke="{RIM}" stroke-width="4"/>'
        s += f'<ellipse cx="{c}" cy="{t + 1}" rx="{rt - 5:.1f}" ry="{self.ry(t) - 4:.1f}" fill="none" stroke="#fff" stroke-width="2" opacity=".8"/>'
        # 반사광: 왼쪽 굵게, 오른쪽 가늘게
        x0, x1 = c - rt * .72, c - rb * .72
        s += (f'<path d="M{x0:.1f},{t + self.ry(t) + 14:.1f} L{x1:.1f},{b - 30:.1f}" stroke="#fff" stroke-width="{self.w * .05:.1f}" '
              f'stroke-linecap="round" opacity=".55"/>')
        x0, x1 = c + rt * .8, c + rb * .8
        s += (f'<path d="M{x0:.1f},{t + self.ry(t) + 22:.1f} L{x1:.1f},{b - 60:.1f}" stroke="#fff" stroke-width="{self.w * .02:.1f}" '
              f'stroke-linecap="round" opacity=".5"/>')
        return s


def layered(g, n_full, n):
    """컵 안쪽 높이를 n_full칸으로 나눠 n층을 채운다. 반환: (층 윗면 y 목록, 층 중심 y 목록)"""
    step = (g.lb - g.top) / n_full
    levels = [g.lb - step * (i + 1) for i in range(n)]
    centers = []
    for i in range(n):
        y_top, y_bot = levels[i], (g.lb if i == 0 else levels[i - 1])
        centers.append((y_top + y_bot) / 2 + (g.ry(y_top) + g.ry(y_bot)) / 2 * .7)
    return levels, centers


def drip(x, y0, y1, wd, fill='url(#pain)'):
    """위에서 아래로 흘러내린 방울: 둥근 줄기 + 아래 맺힌 방울"""
    return (f'<path d="M{x - wd / 2:.1f},{y0:.1f} L{x - wd / 2:.1f},{y1:.1f} A{wd / 2:.1f},{wd / 2:.1f} 0 0 0 {x + wd / 2:.1f},{y1:.1f} '
            f'L{x + wd / 2:.1f},{y0:.1f} Z" fill="{fill}"/><circle cx="{x:.1f}" cy="{y1 + wd * .15:.1f}" r="{wd * .78:.1f}" fill="#d64850"/>')


def pain_overflow(g):
    """빨간 '통증'이 가장자리 위로 부풀어 유리 앞·옆면을 타고 흘러 바닥에 고인다. 반환: (svg, 글자 중심)"""
    import math
    c, t, b, rt, rb = g.cx, g.top, g.base, g.w / 2, g.w * .39
    ryt = g.ry(t)
    # 바닥 웅덩이(겹친 타원 3개로 불규칙한 모양)
    s = (f'<ellipse cx="{c + 10}" cy="{b + 4}" rx="{rt * 1.12:.1f}" ry="{g.ry(b) * 1.25:.1f}" fill="#d64850"/>'
         f'<ellipse cx="{c - rt * .95:.1f}" cy="{b + 10}" rx="{rt * .32:.1f}" ry="{g.ry(b) * .6:.1f}" fill="#d64850"/>'
         f'<ellipse cx="{c + rt * 1.05:.1f}" cy="{b + 12}" rx="{rt * .26:.1f}" ry="{g.ry(b) * .5:.1f}" fill="#d64850"/>'
         f'<ellipse cx="{c - rt * .3:.1f}" cy="{b + 2}" rx="{rt * .35:.1f}" ry="5" fill="#fff" opacity=".25"/>')
    # 옆면을 타고 내려가는 줄기
    for side, wob in ((-1, 10), (1, -8)):
        x0, x1 = c + side * (rt + 2), c + side * (rb + 6)
        s += (f'<path d="M{x0:.1f},{t:.1f} C{x0 + side * 6:.1f},{t + g.h * .3:.1f} {x1 + side * wob:.1f},{t + g.h * .6:.1f} {x1:.1f},{b - 4:.1f}" '
              f'fill="none" stroke="url(#pain)" stroke-width="13" stroke-linecap="round"/>')
        s += f'<ellipse cx="{c + side * (rt * .86 + 8):.1f}" cy="{t + g.h * .46:.1f}" rx="10" ry="13" fill="#d64850"/>'
    # 앞면으로 흘러내린 방울들 (앞쪽 테두리 호에서 시작)
    for fx, ln, wd in ((-.86, 118, 20), (.84, 78, 18)):  # 가운데는 비움(훈련 글자 자리)
        x = c + rt * fx
        y0 = t + ryt * math.sqrt(1 - fx * fx)
        s += drip(x, y0 - 4, y0 + ln, wd)
    # 테두리 위로 부푼 표면 (앞쪽 테두리 호로 닫음)
    dome = 58
    s += (f'<path d="M{c - rt - 8:.1f},{t + 2:.1f} C{c - rt + 4:.1f},{t - dome * .9:.1f} {c - rt * .3:.1f},{t - dome:.1f} {c:.1f},{t - dome:.1f} '
          f'C{c + rt * .3:.1f},{t - dome:.1f} {c + rt - 4:.1f},{t - dome * .9:.1f} {c + rt + 8:.1f},{t + 2:.1f} '
          f'A{rt + 8:.1f},{ryt + 8:.1f} 0 0 1 {c - rt - 8:.1f},{t + 2:.1f} Z" fill="url(#pain)"/>')
    s += (f'<path d="M{c - rt * .66:.1f},{t - dome * .35:.1f} Q{c - rt * .45:.1f},{t - dome * .8:.1f} {c - rt * .1:.1f},{t - dome * .86:.1f}" '
          f'stroke="#fff" stroke-width="7" stroke-linecap="round" fill="none" opacity=".4"/>')
    # 튀는 방울
    for dx, dy, r in ((-1.12, -.9, 9), (-1.25, -.35, 6), (1.1, -.95, 8), (1.24, -.4, 6)):
        s += f'<circle cx="{c + rt * dx:.1f}" cy="{t + dome * dy:.1f}" r="{r}" fill="#e05860"/>'
    return s, (c, (t - dome + t + ryt + 8) / 2)


LABELS = {}


def cups2():
    W, H = 888, 420
    left, right = Glass(222, 372, 290, 290), Glass(666, 372, 290, 290)
    s = DEFS
    lv, lc = layered(left, 4, 2)
    s += left.back() + left.liquid(lv, LAYERS) + left.front()
    rv, rc = layered(right, 4, 4)
    pain, pc = pain_overflow(right)
    # 맨 위층은 빨간 넘침이 앞쪽 테두리까지 덮으므로, 보이는 띠(넘침 아래 ~ 아래층 경계) 가운데로 글자를 내린다
    rc[-1] = (right.top + right.ry(right.top) + 8 + rv[-2] + right.ry(rv[-2])) / 2
    s += right.back() + right.liquid(rv, LAYERS, surface=False) + right.front() + pain
    names = ['장거리', '템포', '인터벌', '무리한 대회']
    LABELS['cups2'] = {'layers': [(222, y, names[i], i) for i, y in enumerate(lc)] + [(666, y, names[i], i) for i, y in enumerate(rc)],
                       'pain': pc}
    return page(W, H, s)


def ghost(g):
    """이전 단계 컵 크기를 점선으로 겹쳐 그려 커진 정도를 보여준다."""
    c, t, b, rt, rb = g.cx, g.top, g.base, g.w / 2, g.w * .39
    return (f'<path d="M{c - rt:.1f},{t} L{c - rb:.1f},{b - 4} A{rb:.1f},{g.ry(b):.1f} 0 0 0 {c + rb:.1f},{b - 4} L{c + rt:.1f},{t}" fill="none" '
            f'stroke="#0a5fa8" stroke-width="4" stroke-dasharray="10 9" stroke-linecap="round" opacity=".8"/>'
            f'<ellipse cx="{c}" cy="{t}" rx="{rt:.1f}" ry="{g.ry(t):.1f}" fill="none" stroke="#0a5fa8" stroke-width="4" stroke-dasharray="10 9" opacity=".8"/>')


def cups3():
    W, H, base = 888, 420, 396
    sizes = [(94, 124, 140), (364, 214, 245), (716, 320, 360)]  # (cx, 위 폭, 높이)
    s = DEFS
    for i, (cx, w, h) in enumerate(sizes):
        g = Glass(cx, base, w, h)
        lvl = g.lb - (g.lb - g.top) * .62
        s += g.back() + g.liquid([lvl], [WATER2]) + g.front()
        if i:
            s += ghost(Glass(cx, base, sizes[i - 1][1], sizes[i - 1][2]))
    # 컵 위를 지나 오른쪽 위로 올라가는 성장 화살표
    pts = [(94, 222), (364, 120), (520, 62)]
    d = 'M' + ' L'.join(f'{x},{y}' for x, y in pts)
    s += f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2 16"/>'
    s += f'<path d="M{520 - 30},{62 - 1} L520,62 L{520 - 13},{62 + 27}" fill="none" stroke="{BLUE}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
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
import json
(OUT / 'labels.json').write_text(json.dumps(LABELS, ensure_ascii=False), encoding='utf-8')  # build.py가 글 위치로 사용
print('ok')
