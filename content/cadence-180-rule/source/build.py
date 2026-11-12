"""나만의 템포(케이던스 자기조직화) 카드 HTML 생성: source/01.html ~ 08.html (tools/cardkit의 qa.js·layers.js 포함).
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
        '<h1 class="headline">당신의 러닝 <span class="accent">템포</span>,<br>누가 정했나요?</h1>', gap(40),
        photo('cover-race-runners_PeterMooney_ccby20.jpg', 640, 960, -36, -10, '도로 대회에서 힘껏 달리는 두 시민 러너'), gap(40),
        '<p class="body">케이던스(분당 걸음 수)는<br>달리기의 템포입니다</p>']),
    # 02 180의 기원 — Daniels 1984
    ('kind-origin', [
        '<h1 class="headline">180은 <span class="accent">올림픽 선수</span>의<br>템포였습니다</h1>', gap(36),
        photo('cover-elite-marathon_AngelLite_pdm.jpg', 360, 888, 0, -170, '도로 경기에서 달리는 엘리트 선수 세 명'), gap(36),
        '<p class="body">1984년 LA 올림픽, 잭 대니얼스 코치가<br>경기 중인 엘리트 선수 약 47명의<br>걸음 수를 세어 보니<br><span class="strong">180보 미만은 단 1명</span>이었습니다.</p>', gap(36),
        '<div class="box"><p class="item">실험으로 찾은 최적값이 아니라<br>엘리트 경기의 관찰값입니다</p></div>']),
    # 03 자기조직화
    ('kind-self', [
        '<h1 class="headline">템포는<br>내 <span class="accent">몸이 만듭니다</span></h1>', gap(36),
        photo('club-runners_PeterMooney_ccby20.jpg', 380, 888, 0, -40, '도로 대회에서 각자의 리듬으로 달리는 두 러너'), gap(40),
        '<p class="body">달리기를 반복하면서 몸은<br>에너지·부하·편안함이 균형을 이루는<br><span class="strong">템포를 스스로 찾아갑니다.</span></p>', gap(40),
        '<div class="box"><p class="item">이것을 <span class="accent">자기조직화</span>라고 합니다</p>'
        '<p class="note">self-organization</p></div>']),
    # 04 다른 게 정상 — 원문 Fig. 1
    ('kind-figure', [
        '<h1 class="headline">그래서 사람마다<br><span class="accent">다른 게 정상</span>입니다</h1>', gap(28),
        figure('fig1_patoz2026_cadence_speed.png', 820, 564, '원문 Fig. 1: 달리기 속도별 케이던스, 연구별 평균값 산점도'), gap(12),
        '<p class="note">원문 Fig. 1 · 점 하나 = 연구·조건 하나의 평균<br>가로: 달리기 속도(km/h) · 세로: 분당 걸음 수</p>', gap(24),
        '<p class="body">속도·체형·신발·노면에 따라 다르고<br><span class="strong">모양은 달라도 효율은 비슷합니다.</span></p>']),
    # 05 시간이 걸린다 — 숙련/초보
    ('kind-learn', [
        '<h1 class="headline">템포를 찾는 데는<br><span class="accent">시간</span>이 걸립니다</h1>', gap(84),
        '<div class="list" style="gap:68px">'
        + kpair('숙련 러너는', '오래 달리며 몸이 찾아낸<br>최적 템포 근처로 달리는 경향')
        + kpair('초보 러너는', '아직 몸이 템포를 찾는 중이라<br>최적보다 낮게 달리는 경향') + '</div>', gap(88),
        '<div class="box"><p class="key">반복해서 달리며<br>몸은 <span class="accent">내 템포</span>를 다듬어 갑니다</p></div>']),
    # 06 남의 템포 강요
    ('kind-imposed', [
        '<h1 class="headline">남의 템포를<br><span class="accent">강요</span>하면?</h1>', gap(48),
        '<div class="list" style="gap:36px">'
        + kpair('더 힘들어질 수 있습니다', '내 템포에서 크게 벗어나면<br>에너지와 힘든 느낌이 커지는 경향')
        + kpair('부담이 옮겨갈 수 있습니다', '다른 관절에서 보상이 생길 수 있습니다')
        + kpair('몸이 찾은 균형이 흐트러집니다', '일률적 처방은 자기조직화를<br>방해할 위험이 있습니다') + '</div>', gap(48),
        '<div class="box"><p class="item">정답은 한 점이 아니라<br>내 템포 근처의 편한 범위</p></div>']),
    # 07 PFP 조율 (숫자 없이)
    ('kind-pfp', [
        '<h1 class="headline">그래도 살짝<br><span class="accent">조율</span>할 때가 있습니다</h1>', gap(44),
        '<div class="box"><p class="body">무릎 앞이 아픈 러너는<br>평소 템포를 조금 올려 조정해 보면<br><span class="strong">달릴 때 통증이 줄었다</span>는 연구가 있습니다.</p></div>', gap(52),
        '<div class="list" style="gap:40px">'
        + kpair('180이 아니라 내 템포에서', '평소보다 조금만 올립니다')
        + kpair('근력·부하 관리와 함께', '템포 조정만으로 해결하지 않습니다')
        + kpair('통증 반응을 보며 천천히', '너무 빨리 바꾸면 종아리·아킬레스가<br>불편할 수 있습니다') + '</div>']),
    # 08 나만의 템포
    ('kind-summary', [
        '<h1 class="headline">남의 템포 말고,<br><span class="accent">나만의 템포</span></h1>', gap(72),
        '<div class="list" style="gap:48px">'
        + kpair('내 템포부터 알기', '같은 속도·같은 길에서 재 봅니다')
        + kpair('바꾼다면 조금씩', '내 템포에서 출발해 반응을 봅니다') + '</div>', gap(64),
        '<div class="box"><p class="key">평균과 다르다고<br><span class="accent">틀린 것은 아닙니다</span></p></div>', gap(64),
        '<p class="safety"><span class="warn">통증이 생기거나 커지면 멈추고</span><br>담당 트레이너와 다시 조정하세요.</p>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>나만의 템포 {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
