"""러너 슬개골 스트랩 카드 HTML 생성: source/01.html ~ 08.html (tools/cardkit의 qa.js·layers.js 포함).
글은 h1/p, 굵기 500·650·700·750·800·850만, 사진은 overflow:hidden 크롭 안의 img.
사용: python3 content/patellar-strap-runners/source/build.py"""
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
.big{{font-size:144px;font-weight:850;line-height:1.08;letter-spacing:-.04em;color:var(--blue)}}
.note{{font-size:36px;font-weight:500;line-height:1.4;color:var(--muted);letter-spacing:-.02em}}
.safety{{font-size:38px;font-weight:700;line-height:1.42;letter-spacing:-.02em}}
.accent{{color:var(--blue)}} .warn{{color:var(--red)}}
.photo{{position:relative;overflow:hidden;width:888px}}
.photo img{{position:absolute;display:block}}
.slot{{width:888px;border-radius:20px;background:var(--tint);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px}}
.slot .tag{{font-size:36px;font-weight:700;color:var(--blue);line-height:1.3}}
.slot .guide{{font-size:36px;font-weight:500;color:var(--muted);line-height:1.42}}
.list{{display:flex;flex-direction:column;align-items:center;gap:40px}}
.pair{{display:flex;flex-direction:column;align-items:center;gap:8px}}
.box{{background:var(--tint);border-radius:20px;padding:32px 40px;width:888px}}
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


CARDS = [
    # 01 표지
    ('kind-cover', [
        '<h1 class="headline">러너 무릎의<br><span class="accent">슬개골 스트랩</span>,<br>왜 덜 아플까요?</h1>', gap(44),
        photo('cover-marathon_equinoxefr_ccby20.jpg', 520, 888, 0, -300, '도로 마라톤에서 무리 지어 달리는 러너들'), gap(44),
        '<p class="body">효과가 있는 사람과 기전,<br>그리고 <span class="strong">차라리 해야 할 운동</span>까지</p>']),
    # 02 무엇·왜 (사진 자리)
    ('kind-what', [
        '<h1 class="headline">무릎뼈 바로 아래<br><span class="accent">힘줄 위</span>를 감는 띠</h1>', gap(40),
        '<div class="slot" style="height:500px"><p class="tag">사진 넣는 자리</p>'
        '<p class="guide">스트랩을 찬 무릎 · 정면 또는 옆모습<br>띠가 무릎뼈 바로 아래 힘줄 위를 지나게</p></div>', gap(44),
        '<p class="body">무릎 앞이 아플 때 덜 아프게<br>달리려고 찹니다. 연구는 주로<br><span class="strong">무릎뼈 아래 힘줄 통증</span>에서 했습니다.</p>', gap(20),
        '<p class="note">슬개건병증, ‘점퍼 무릎’으로도 불립니다</p>']),
    # 03 효과 (de Vries 2016 RCT)
    ('kind-effect', [
        '<h1 class="headline">통증은 줄었습니다,<br><span class="accent">가짜 테이프</span>도요</h1>', gap(72),
        '<p class="body">무릎뼈 아래 힘줄 통증이 있는<br>운동선수 97명, 한 다리 경사 스쿼트</p>', gap(60),
        '<p class="big" style="font-size:160px">−14mm</p>', gap(12),
        '<p class="note">스트랩 착용 시 통증 감소<br>(0~100mm 척도, 착용하지 않았을 때 대비)</p>', gap(80),
        '<div class="box"><p class="body">스트랩·스포츠 테이프 모두<br><span class="strong">가짜 테이프보다 낫지 않았고,</span><br>효과는 단기 결과만 확인됐습니다.</p></div>']),
    # 04 기전 ① 역학
    ('kind-mech1', [
        '<h1 class="headline">기전 가설 ①<br><span class="accent">힘줄이 덜 당겨진다</span></h1>', gap(92),
        '<div class="list" style="gap:64px">'
        + pair('무릎뼈–힘줄 각도·길이 변화', '남성 20명 X선 사진으로 만든 모델:<br>대부분 통증 부위 변형률이 낮게 계산', 'key')
        + pair('허벅지 앞 근육 힘 감소', '건강한 18명 달리기 분석 모델:<br>넙다리네갈래근 최대·누적 힘 감소', 'key')
        + '</div>', gap(72),
        '<div class="box" style="padding:40px"><p class="safety">둘 다 계산으로 얻은 값입니다.<br>통증 감소나 힘줄 회복을<br>직접 보여 준 결과는 아닙니다.</p></div>']),
    # 05 기전 ② 감각·기대
    ('kind-mech2', [
        '<h1 class="headline">기전 가설 ②<br><span class="accent">감각과 기대</span></h1>', gap(100),
        '<div class="list" style="gap:64px">'
        + pair('가짜 테이프도 비슷하게 감소', '힘줄을 누르지 않는 테이프와<br>통증 차이가 뚜렷하지 않았습니다', 'key')
        + pair('무릎 위치 감각', '감각이 떨어져 있던 선수에서만<br>무릎 각도 맞추기가 정확해졌습니다', 'key')
        + '</div>', gap(80),
        '<p class="body">피부를 누르는 감각 신호와<br>‘덜 아플 것’이라는 기대가<br><span class="strong">함께 작용했을 가능성</span>이 있습니다.</p>']),
    # 06 누구에게
    ('kind-who', [
        '<h1 class="headline">효과가 보고된 사람은<br><span class="accent">따로 있습니다</span></h1>', gap(88),
        '<div class="list" style="gap:76px">'
        + pair('<span class="accent">써볼 만함</span> · 무릎뼈 아래', '점프·착지에서 아픈 힘줄 통증<br>→ 착용 중 단기 통증 감소 보고', 'key')
        + pair('<span class="warn">권하지 않음</span> · 무릎뼈 주변', '러너에게 가장 흔한 슬개대퇴통증<br>→ 가이드라인: 스트랩·보조기 비권고', 'key')
        + pair('<span class="warn">근거 부족</span> · 예방 목적', '아프지 않은데 미리 차는 경우', 'key')
        + '</div>', gap(64),
        '<p class="note">대부분 소규모·단기 연구라 개인 반응을 보고 판단합니다</p>']),
    # 07 차라리 운동
    ('kind-exercise', [
        '<h1 class="headline">차라리 <span class="accent">운동</span>에<br>시간을 쓰세요</h1>', gap(32),
        photo('mini-squat_BaoBaoLeung_ccbysa40.jpg', 520, 790, 49, -4, '무릎을 살짝 굽힌 미니 스쿼트 옆모습'), gap(36),
        '<div class="list" style="gap:36px">'
        + pair('무릎뼈 아래 힘줄 통증', '점진적 힘줄 부하 운동 24주 뒤 기능 점수<br>+28점 (기존 편심 운동 +18점)')
        + pair('무릎뼈 주변 통증', '엉덩관절 + 무릎 근력 운동을 함께')
        + '</div>']),
    # 08 요약
    ('kind-summary', [
        '<h1 class="headline">스트랩은 <span class="accent">진통 보조</span>,<br>회복은 운동</h1>', gap(92),
        '<div class="list" style="gap:64px">'
        + pair('찬다면 <span class="accent">무릎뼈 아래</span> 통증에', '운동 프로그램과 함께, 단기 보조로', 'key')
        + pair('덜 아픈 이유는 <span class="accent">여러 가지</span>', '힘줄 당김·근육 힘·감각과 기대', 'key')
        + pair('힘줄을 바꾸는 건 <span class="accent">부하</span>', '점진적 근력·힘줄 부하 운동', 'key')
        + '</div>', gap(80),
        '<p class="safety warn" style="font-size:40px">붓기·밤 통증·무릎이 빠지는 느낌이 있으면<br>스트랩보다 진료가 먼저입니다.</p>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>슬개골 스트랩 {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
