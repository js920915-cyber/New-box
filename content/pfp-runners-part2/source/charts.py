"""Powers 2014 Table 수치로 PFJ stress 그래프 2종을 HTML(인라인 SVG + Noto Sans KR)로 만든다.
render_charts.cjs가 PNG(assets/charts/)로 렌더 → 카드에서는 <img>로 사용(PPTX에도 그림으로 들어감).
원 Figure 4는 쓰지 않는다(JOSPT 저작권). 측정 각도 7곳에만 점, 점 사이는 직선(보간 없음)."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONT = (HERE / '../../../templates/fonts/NotoSansKR-VF.ttf').resolve().as_uri()
ANG = [0, 15, 30, 45, 60, 75, 90]
VR = [8.4, 5.6, 4.7, 4.2, 3.6, 2.6, 0.5]   # 발목 중량 무릎 펴기 (EXT-VR)
CR = [7.9, 5.6, 5.1, 5.0, 5.2, 6.0, 6.5]   # 고정 저항 기계 (EXT-CR, 동력계)
SQ = [0.3, 0.9, 1.9, 3.9, 6.7, 10.5, 12.3]  # 스쿼트
W, H = 888, 560
L, R, T, B = 92, 196, 40, 470  # 그림 영역
INK, MUTED, BLUE, GRID, FAINT = '#121416', '#5e6570', '#0879d8', '#e3e9ee', '#c3ccd4'


def X(a): return L + (R and (W - R - L)) * a / 90
def Y(v): return B - (B - T) * v / 13


def pts(vals, i0=0, i1=7):
    return ' '.join(f'{X(ANG[i]):.1f},{Y(vals[i]):.1f}' for i in range(i0, i1))


def axes():
    s = []
    for v in (0, 4, 8, 12):
        s.append(f'<line x1="{L}" x2="{W - R}" y1="{Y(v)}" y2="{Y(v)}" stroke="{GRID}" stroke-width="2"/>')
        s.append(f'<text x="{L - 18}" y="{Y(v) + 11}" text-anchor="end" font-size="30" fill="{MUTED}">{v}</text>')
    for a in (0, 45, 90):
        s.append(f'<text x="{X(a)}" y="{B + 48}" text-anchor="middle" font-size="32" font-weight="650" fill="{INK}">{a}°</text>')
    s.append(f'<text x="{L - 18}" y="{T - 8}" text-anchor="end" font-size="26" fill="{MUTED}">MPa</text>')
    s.append(f'<text x="{(L + W - R) / 2}" y="{B + 88}" text-anchor="middle" font-size="28" fill="{MUTED}">무릎 굽힘 각도 →</text>')
    return s


def dots(vals, color, i0=0, i1=7, r=8):
    return [f'<circle cx="{X(ANG[i]):.1f}" cy="{Y(vals[i]):.1f}" r="{r}" fill="{color}"/>' for i in range(i0, i1)]


def label(y, text, color, weight=750):
    return f'<text x="{W - R + 22}" y="{y + 11}" font-size="32" font-weight="{weight}" fill="{color}">{text}</text>'


def page(svg):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>@font-face{{font-family:"Noto Sans KR";src:url("{FONT}");font-weight:100 900}}'
            f'html,body{{margin:0;background:#fff}}svg{{display:block;font-family:"Noto Sans KR"}}</style></head><body>'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{svg}</svg></body></html>')


def chart_all():
    s = axes()
    s.append(f'<line x1="{X(45)}" x2="{X(45)}" y1="{T}" y2="{B}" stroke="{FAINT}" stroke-width="2" stroke-dasharray="6 8"/>')
    s.append(f'<polyline points="{pts(CR)}" fill="none" stroke="{MUTED}" stroke-width="5" stroke-dasharray="14 10"/>')
    s += dots(CR, MUTED, r=7)
    s.append(f'<polyline points="{pts(VR)}" fill="none" stroke="{BLUE}" stroke-width="7"/>')
    s += dots(VR, BLUE)
    s.append(f'<polyline points="{pts(SQ)}" fill="none" stroke="{INK}" stroke-width="7"/>')
    s += dots(SQ, INK)
    s.append(label(Y(12.3), '스쿼트', INK))
    s.append(label(Y(6.5), '고정 저항', MUTED, 650))
    s.append(label(Y(0.5), '발목 중량', BLUE))
    return page(''.join(s))


def chart_combo():
    s = axes()
    # 4 MPa 기준선
    s.append(f'<line x1="{L}" x2="{W - R}" y1="{Y(4)}" y2="{Y(4)}" stroke="{BLUE}" stroke-width="3" stroke-dasharray="10 8"/>')
    s.append(f'<text x="{W - R + 22}" y="{Y(4) + 11}" font-size="30" font-weight="750" fill="{BLUE}">4 MPa</text>')
    s.append(f'<polyline points="{pts(SQ, 3, 7)}" fill="none" stroke="{FAINT}" stroke-width="5"/>')
    s.append(f'<polyline points="{pts(VR, 0, 4)}" fill="none" stroke="{FAINT}" stroke-width="5"/>')
    s.append(f'<polyline points="{pts(CR)}" fill="none" stroke="{FAINT}" stroke-width="4" stroke-dasharray="14 10"/>')
    s.append(f'<polyline points="{pts(SQ, 0, 4)}" fill="none" stroke="{INK}" stroke-width="9"/>')
    s += dots(SQ, INK, 0, 4, 9)
    s.append(f'<polyline points="{pts(VR, 3, 7)}" fill="none" stroke="{BLUE}" stroke-width="9"/>')
    s += dots(VR, BLUE, 3, 7, 9)
    s.append(f'<text x="{X(22.5)}" y="{Y(7.4)}" text-anchor="middle" font-size="34" font-weight="800" fill="{INK}">스쿼트</text>')
    s.append(f'<text x="{X(64)}" y="{Y(0.9)}" text-anchor="middle" font-size="34" font-weight="800" fill="{BLUE}">무릎 펴기</text>')
    return page(''.join(s))


out = HERE / 'charts'
out.mkdir(exist_ok=True)
(out / 'chart-all.html').write_text(chart_all(), encoding='utf-8')
(out / 'chart-combo.html').write_text(chart_combo(), encoding='utf-8')
print('charts html ok')
