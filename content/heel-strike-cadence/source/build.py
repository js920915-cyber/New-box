"""힐스트라이크·케이던스 카드 HTML 생성: source/01.html ~ 06.html (tools/cardkit의 qa.js·layers.js 포함).
근거: Patoz 2026 Sports Med Open 12:149 (전문 정독). 04장 그래프는 원문 Fig. 1 크롭 그대로(다시 그리지 않음).
사용: python3 content/heel-strike-cadence/source/build.py"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parents[2] / 'tools/cardkit'
FONT = '../../../templates/fonts/NotoSansKR-VF.ttf'
SCRIPTS = ''.join(f'<script>{(KIT / n).read_text(encoding="utf-8")}</script>' for n in ('qa.js', 'layers.js'))

CSS = f"""
@font-face{{font-family:'Noto Sans KR';src:url('{FONT}');font-weight:100 900}}
:root{{--ink:#121416;--muted:#5e6570;--blue:#0879d8;--red:#cc414a;--tint:#f0f7fc}}
*{{box-sizing:border-box}} html,body{{margin:0;padding:0;background:#fff}}
.card{{position:relative;width:1080px;height:1350px;padding:104px 96px 98px;overflow:hidden;background:#fff;
 font-family:'Noto Sans KR',sans-serif;color:var(--ink);text-align:center;display:flex;flex-direction:column;align-items:center}}
.card-frame{{position:absolute;inset:0;pointer-events:none}}
h1,p{{margin:0;text-align:center}}
.headline{{font-size:84px;font-weight:850;line-height:1.2;letter-spacing:-.035em}}
.kind-cover .headline{{font-size:88px;line-height:1.18}}
.body{{font-size:44px;font-weight:500;line-height:1.42;letter-spacing:-.02em}}
.strong{{font-weight:750}}
.key{{font-size:56px;font-weight:800;line-height:1.3;letter-spacing:-.03em}}
.item{{font-size:48px;font-weight:800;line-height:1.3;letter-spacing:-.03em}}
.note{{font-size:36px;font-weight:500;line-height:1.4;color:var(--muted);letter-spacing:-.02em}}
.safety{{font-size:38px;font-weight:700;line-height:1.42;letter-spacing:-.02em}}
.accent{{color:var(--blue)}} .warn{{color:var(--red)}}
.photo{{position:relative;overflow:hidden;width:888px}}
.photo img{{position:absolute;display:block}}
.fig{{background:#fff}}
.slot{{width:888px;border-radius:20px;background:var(--tint);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px}}
.slot .tag{{font-size:36px;font-weight:700;color:var(--blue);line-height:1.3}}
.slot .guide{{font-size:36px;font-weight:500;color:var(--muted);line-height:1.42}}
.list{{display:flex;flex-direction:column;align-items:center;gap:30px}}
.pair{{display:flex;flex-direction:column;align-items:center;gap:6px}}
.box{{background:var(--tint);border-radius:20px;padding:30px 40px;width:888px}}
"""
FRAME = ('<svg class="card-frame" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">'
         '<rect x="35" y="35" width="1010" height="1280" rx="28" fill="none" stroke="#D0DCE5" stroke-width="2"/></svg>')


def photo(src, h, iw, ix, iy, alt):
    """보이는 창 888×h, 이미지 폭 iw, 창 기준 위치(ix, iy) → 크롭"""
    return (f'<div class="photo" style="height:{h}px"><img src="../assets/photos/{src}" alt="{alt}" '
            f'style="width:{iw}px;left:{ix}px;top:{iy}px"></div>')


def pair(head, sub, cls='item'):
    sub_cls = 'body' if cls == 'key' else 'note'
    return f'<div class="pair"><p class="{cls}">{head}</p><p class="{sub_cls}" style="color:var(--muted)">{sub}</p></div>'


def gap(px):
    return f'<div style="height:{px}px;flex:none"></div>'


def figure(src, w, h, alt):
    """원문 Figure 크롭 PNG를 그대로 배치(수정 없음). 888 폭 창 가운데."""
    return (f'<div class="photo fig" style="height:{h}px"><img src="../assets/figures/{src}" alt="{alt}" '
            f'style="width:{w}px;left:{(888 - w) // 2}px;top:0"></div>')


def bpair(head, sub):
    """핵심 의미를 가진 설명은 본문 크기(44px)로 둔다."""
    return f'<div class="pair"><p class="item">{head}</p><p class="body" style="color:var(--muted)">{sub}</p></div>'


CARDS = [
    # 01 표지
    ('kind-cover', [
        '<h1 class="headline">뒤꿈치 착지,<br>정말 <span class="accent">부상</span>을<br>부를까요?</h1>', gap(40),
        photo('cover-elite-marathon_AngelLite_pdm.jpg', 580, 888, 0, -150, '도로 마라톤에서 나란히 달리는 세 선수 옆모습'), gap(40),
        '<p class="body">‘분당 180보’까지, 러닝의 오래된<br>믿음 세 가지를 다시 봅니다</p>']),
    # 02 뒤꿈치 착지는 흔하다
    ('kind-common', [
        '<h1 class="headline">뒤꿈치 착지는<br><span class="accent">흔한 착지</span>입니다</h1>', gap(40),
        photo('road-race-start_PeterMooney_ccby20.jpg', 540, 900, -6, -30, '도로 달리기 대회 출발 직후 달리는 시민 러너들'), gap(40),
        '<p class="body">장거리 러너 대부분이 뒤꿈치로<br>착지합니다. 뒤꿈치 착지가 충격 지표를<br>늘 더 키우지 않았고, 부상 위험을<br><span class="strong">높인다는 근거도 확인되지 않았습니다.</span></p>']),
    # 03 착지를 바꾸면?
    ('kind-impact', [
        '<h1 class="headline">앞꿈치로 바꾸면<br>더 <span class="accent">안전</span>할까요?</h1>', gap(40),
        photo('running-styles_ChrisHunkeler_ccbysa20.jpg', 420, 1000, -56, -330, '발가락 신발을 신은 남성과 러닝화를 신은 여성이 달리는 하체'), gap(40),
        '<p class="body">바닥에서 재는 충격과 뼈·힘줄이<br>실제로 받는 부하는 같지 않습니다.<br>착지를 바꾸면 부하가 줄기보다<br><span class="strong">다른 곳으로 옮겨갈 수 있습니다.</span></p>', gap(20),
        '<p class="note">착지 변경은 특정 부위의 부하를 옮길<br>이유가 있을 때만 고려합니다</p>']),
    # 04 원문 Fig. 1
    ('kind-figure', [
        '<h1 class="headline">‘분당 180보’는<br><span class="accent">모두의 정답</span>이 아닙니다</h1>', gap(36),
        figure('fig1_patoz2026_cadence_speed.png', 860, 592, '원문 Fig. 1: 달리기 속도별 케이던스, 연구별 평균값 산점도'), gap(16),
        '<p class="note">원문 Fig. 1 · 점 하나 = 연구·조건 하나의 평균<br>가로: 달리기 속도(km/h) · 세로: 분당 걸음 수</p>', gap(28),
        '<p class="body">속도가 빠를수록 대체로 올라가고,<br><span class="strong">가장 효율적인 값도 사람마다 다릅니다.</span></p>']),
    # 05 케이던스 처방
    ('kind-cadence', [
        '<h1 class="headline">케이던스 올리기,<br>모두에게 <span class="accent">약</span>일까요?</h1>', gap(48),
        '<div class="list" style="gap:36px">'
        + bpair('바로 바뀌는 값은 있습니다', '같은 속도에서 걸음 수를 늘리면<br>일부 충격·관절 부하가 달라질 수 있습니다')
        + bpair('반응은 사람마다 다릅니다', '크기와 방향이 제각각이고<br>다른 관절로 부하가 옮겨갈 수 있습니다')
        + bpair('부상 감소는 확인되지 않았습니다', '부상이 줄거나 기록이 좋아진다는<br>일관된 근거는 아직 없습니다') + '</div>', gap(48),
        '<div class="box"><p class="safety">무릎 앞 통증(PFP) 러너처럼<br>임상 근거가 있을 때는 시도해 볼 수 있습니다</p></div>']),
    # 06 요약·판단
    ('kind-summary', [
        '<h1 class="headline">주법을 바꾸기 전,<br><span class="accent">세 가지</span>를 묻습니다</h1>', gap(56),
        '<div class="list" style="gap:40px">'
        + pair('통증과 관련 있나요?', '통증·기능·기록상 바꿀 이유가 없으면<br>원래 주법을 유지합니다', 'key')
        + pair('조직이 버티고 있나요?', '부하가 회복·적응 능력을 넘는지 봅니다', 'key')
        + pair('바꿀 준비가 됐나요?', '새 움직임을 익힐 몸·감각의 여유를 봅니다', 'key') + '</div>', gap(52),
        '<p class="safety">바꾼다면 조금씩, 통증·편안함·기능으로<br>판단합니다. <span class="warn">통증이 커지면 멈추고</span><br>담당 트레이너와 다시 조정하세요.</p>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>힐스트라이크 {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
