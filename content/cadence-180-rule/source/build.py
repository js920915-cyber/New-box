"""케이던스 180 규칙 카드 HTML 생성: source/01.html ~ 07.html (tools/cardkit의 qa.js·layers.js 포함).
근거: Patoz 2026 Sports Med Open 12:149 (Belief 2), van Oeveren 2017 PLoS ONE (전문 정독).
03장 그래프는 Patoz 2026 원문 Fig. 1 크롭 그대로(다시 그리지 않음).
사용: python3 content/cadence-180-rule/source/build.py"""
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
.photo{{position:relative;overflow:hidden;width:888px;flex:none}}
.photo img{{position:absolute;display:block}}
.fig{{background:#fff}}
.slot{{width:888px;border-radius:20px;background:var(--tint);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px}}
.slot .tag{{font-size:36px;font-weight:700;color:var(--blue);line-height:1.3}}
.slot .guide{{font-size:36px;font-weight:500;color:var(--muted);line-height:1.42}}
.list{{display:flex;flex-direction:column;align-items:center;gap:30px}}
.pair{{display:flex;flex-direction:column;align-items:center;gap:6px}}
.big{{font-size:144px;font-weight:850;line-height:1.1;letter-spacing:-.04em;color:var(--blue)}}
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



def figure(src, w, h, alt):
    """원문 Figure 크롭 PNG를 그대로 배치(수정 없음). 888 폭 창 가운데."""
    return (f'<div class="photo fig" style="height:{h}px"><img src="../assets/figures/{src}" alt="{alt}" '
            f'style="width:{w}px;left:{(888 - w) // 2}px;top:0"></div>')


def bpair(head, sub):
    """핵심 의미를 가진 설명은 본문 크기(44px)로 둔다."""
    return f'<div class="pair"><p class="item">{head}</p><p class="body" style="color:var(--muted)">{sub}</p></div>'


def kpair(head, sub):
    return f'<div class="pair"><p class="key">{head}</p><p class="body" style="color:var(--muted)">{sub}</p></div>'

CARDS = [
    # 01 표지
    ('kind-cover', [
        '<h1 class="headline">분당 180보,<br>꼭 <span class="accent">맞춰야</span><br>할까요?</h1>', gap(40),
        photo('cover-race-runners_PeterMooney_ccby20.jpg', 580, 900, -6, -20, '도로 대회에서 힘껏 달리는 두 시민 러너'), gap(40),
        '<p class="body">‘케이던스 180’은 어디서 왔고<br>연구는 무엇을 말할까요?</p>']),
    # 02 출처 — Daniels 1984 올림픽 관찰 (V.O2 2018 회고)
    ('kind-origin', [
        '<h1 class="headline">180은 <span class="accent">올림픽 선수</span>를<br>세어 본 숫자입니다</h1>', gap(36),
        photo('cover-elite-marathon_AngelLite_pdm.jpg', 360, 888, 0, -170, '도로 경기에서 달리는 엘리트 선수 세 명'), gap(36),
        '<p class="body">1984년 LA 올림픽, 잭 대니얼스 코치가<br>경기 중인 엘리트 선수 약 47명의<br>걸음 수를 세어 보니<br><span class="strong">180보 미만은 단 1명</span>이었습니다.</p>', gap(36),
        '<div class="box"><p class="item">실험으로 찾은 최적값이 아니라<br>엘리트 경기의 관찰값입니다</p></div>']),
    # 03 원문 Fig. 1 — 대체로 속도에 의존
    ('kind-figure', [
        '<h1 class="headline">케이던스는 대체로<br><span class="accent">속도</span>를 따라갑니다</h1>', gap(28),
        figure('fig1_patoz2026_cadence_speed.png', 820, 564, '원문 Fig. 1: 달리기 속도별 케이던스, 연구별 평균값 산점도'), gap(12),
        '<p class="note">원문 Fig. 1 · 점 하나 = 연구·조건 하나의 평균<br>가로: 달리기 속도(km/h) · 세로: 분당 걸음 수</p>', gap(24),
        '<p class="body">느리거나 중간 속도에서는 주로 보폭이,<br>빠를수록 케이던스가<br><span class="strong">속도를 끌어올리는 몫이 커집니다.</span></p>']),
    # 04 영향 요인
    ('kind-factors', [
        '<h1 class="headline">몸·신발·노면도<br>케이던스를 <span class="accent">바꿉니다</span></h1>', gap(36),
        photo('barefoot-sand-run_NewtownGrafitti_ccby20.jpg', 300, 888, 0, -150, '해변 모래 위를 맨발로 달리는 러너들'), gap(36),
        '<div class="list" style="gap:28px">'
        + bpair('다리가 길거나 체중이 많으면', '성인 러너의 케이던스가 더 낮은 경향')
        + bpair('맨발·미니멀 신발이면', '신발을 신을 때보다 대체로 높아집니다')
        + bpair('잔디·모래처럼 푹신한 바닥이면', '안정성을 지키려 높아지는 경우가 많습니다') + '</div>', gap(44),
        '<p class="item">케이던스는 <span class="accent">조절 전략의 일부</span>입니다</p>']),
    # 05 van Oeveren 2017
    ('kind-number', [
        '<h1 class="headline">심박이 가장 낮았던<br><span class="accent">케이던스</span>는?</h1>', gap(40),
        '<p class="body">초보 러너 12명이 트레드밀에서<br>걸음 수를 바꿔 가며 달렸습니다</p>', gap(36),
        '<p class="big">분당 약 166보</p>', gap(8),
        '<p class="note">83 stride(1 stride = 2걸음)</p>', gap(44),
        '<p class="body">180보보다 낮았습니다. 그래도 연구진은<br><span class="strong">이 값도 모두에게 적용하지 말고</span><br><span class="strong">개인별로 정하라</span>고 결론 내렸습니다.</p>', gap(48),
        '<div class="box"><p class="safety">심박으로 추정한 값 · 초보 12명 ·<br>시속 약 8.6~10.4km 범위의 결과입니다</p></div>']),
    # 06 제약조건의 결과 · 완만한 최적 구간
    ('kind-nudge', [
        '<h1 class="headline">케이던스는<br>여러 조건이 만든 <span class="accent">결과</span></h1>', gap(36),
        '<p class="body">러너는 힘든 정도·협응·달리는 상황이<br>균형을 이루는 범위로 모입니다.</p>', gap(40),
        '<div class="box"><p class="key">최적은 한 점이 아니라<br><span class="accent">완만한 구간</span>입니다</p></div>', gap(48),
        '<div class="list" style="gap:40px">'
        + kpair('<span class="accent">신중한 소폭</span> 조절은 도움', '평소 리듬에서 조금 올리면 일부 러너는<br>에너지·부하 면에서 이득을 볼 수 있습니다')
        + kpair('<span class="accent">일률적 강요</span>는 역효과 위험', '몸의 자기조절을 흐트러뜨려<br>에너지·부하 부담을 키울 수 있습니다') + '</div>']),
    # 07 요약
    ('kind-summary', [
        '<h1 class="headline">180 대신<br><span class="accent">내 숫자</span>에서 시작합니다</h1>', gap(56),
        '<div class="list" style="gap:40px">'
        + kpair('먼저 평소 케이던스 확인', '같은 속도·같은 길에서 재야 비교됩니다')
        + kpair('바꾼다면 평소 값에서 조금씩', '정해진 180이 아니라 내 기준에서')
        + kpair('몸의 반응으로 판단', '통증·편안함·기능을 함께 봅니다') + '</div>', gap(48),
        '<div class="box"><p class="safety">무릎 앞 통증(PFP) 러너처럼 임상 근거가<br>있으면 케이던스 조정을 시도해 볼 수 있습니다</p></div>', gap(44),
        '<p class="safety"><span class="warn">통증이 생기거나 커지면 멈추고</span><br>담당 트레이너와 다시 조정하세요.</p>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>케이던스 180 {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
