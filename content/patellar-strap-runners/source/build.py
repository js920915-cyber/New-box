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
        '<h1 class="headline">무릎에 <span class="accent">띠 하나</span><br>감았을 뿐인데<br>왜 덜 아플까요?</h1>', gap(44),
        photo('cover-marathon_equinoxefr_ccby20.jpg', 520, 888, 0, -300, '도로 마라톤에서 무리 지어 달리는 러너들'), gap(44),
        '<p class="body">효과는 진짜입니다.<br>다만 <span class="strong">이유가 생각과 다릅니다.</span></p>']),
    # 02 이게 뭐예요? (사진 자리)
    ('kind-what', [
        '<h1 class="headline">무릎뼈 <span class="accent">바로 아래</span>를<br>꾹 누르는 띠</h1>', gap(40),
        '<div class="slot" style="height:580px"><p class="tag">사진 넣는 자리</p>'
        '<p class="guide">스트랩을 찬 무릎 · 정면 또는 옆모습<br>띠가 무릎뼈 바로 아래 힘줄 위를 지나게</p></div>', gap(44),
        '<p class="body">무릎뼈와 정강이를 잇는 <span class="strong">힘줄</span> 위를<br>지나갑니다. 점프·착지에서 이 힘줄이<br>아픈 ‘점퍼 무릎’에서 주로 연구됐습니다.</p>']),
    # 03 효과 — VAS 화살표
    ('kind-effect', [
        '<h1 class="headline">차면 덜 아팠습니다<br>그런데 <span class="accent">가짜 테이프</span>도요</h1>', gap(64),
        '<p class="body">운동선수 97명 · 한 다리 경사 스쿼트 통증</p>', gap(44),
        '<div class="photo" style="height:400px"><img src="../assets/charts/vas.png" alt="0~100mm 통증 척도에서 14mm 감소를 나타낸 화살표" style="width:888px;left:0;top:0"></div>', gap(8),
        '<p class="note">안 찼을 때보다 줄어든 폭 (화살표 길이만 실제 비율)</p>', gap(64),
        '<div class="box"><p class="body">아무 힘도 주지 않는 가짜 테이프와<br>비교하면 <span class="strong">뚜렷한 차이가 없었습니다.</span></p></div>']),
    # 04 이유 ① 덜 당겨진다
    ('kind-mech1', [
        '<h1 class="headline">고무줄 중간을<br><span class="accent">손가락으로 누르면</span></h1>', gap(112),
        '<p class="key">아래쪽이 덜 늘어나죠.</p>', gap(48),
        '<p class="body">스트랩이 힘줄을 누르면 각도와 길이가<br>바뀌어, 아픈 부위가 <span class="strong">덜 당겨진다고</span><br><span class="strong">계산</span>됐습니다.</p>', gap(48),
        '<p class="note">X선 사진 20명 기반 모델. 달리기 분석 모델에서도<br>허벅지 앞 근육 힘이 줄었다는 계산 결과</p>', gap(96),
        '<div class="box" style="padding:56px 40px"><p class="safety">둘 다 계산값입니다.<br>통증이 줄어드는 걸 직접 잰 건 아닙니다.</p></div>']),
    # 05 이유 ② 감각과 기대
    ('kind-mech2', [
        '<h1 class="headline">부딪힌 팔꿈치를<br><span class="accent">문지르면</span> 덜 아픈 것처럼</h1>', gap(130),
        '<p class="key" style="font-weight:750">피부를 누르는 감각이<br><span class="accent">통증 신호를 덮을 수</span> 있습니다</p>', gap(88),
        '<p class="key" style="font-weight:750">여기에 <span class="accent">‘차면 덜 아파’</span><br>기대도 더해집니다</p>', gap(130),
        '<div class="box" style="padding:44px 40px"><p class="note" style="color:var(--ink);font-size:38px">가짜 테이프 결과로 추정한 가능성입니다.<br>실제로 잰 감각은 ‘무릎 위치 감각’ 하나,<br>원래 감각이 떨어진 선수에서만 좋아졌습니다.</p></div>']),
    # 06 아픈 자리로 구분
    ('kind-who', [
        '<h1 class="headline"><span class="accent">어디가</span> 아픈지가<br>먼저입니다</h1>', gap(110),
        '<div class="list" style="gap:90px">'
        + pair('<span class="accent">써볼 만함</span> · 무릎뼈 아래', '점프·착지·내리막에서 아플 때', 'key')
        + pair('<span class="warn">권하지 않음</span> · 무릎뼈 주변·뒤', '러너에게 흔한 통증, 가이드라인 비권고', 'key')
        + pair('<span class="warn">근거 부족</span> · 예방용', '안 아픈데 미리 찰 때', 'key')
        + '</div>', gap(84),
        '<p class="note">정확한 구분은 평가가 필요합니다</p>']),
    # 07 차라리 운동
    ('kind-exercise', [
        '<h1 class="headline">힘줄은<br><span class="accent">쓰면서</span> 튼튼해집니다</h1>', gap(48),
        photo('mini-squat_BaoBaoLeung_ccbysa40.jpg', 600, 900, -6, 0, '무릎을 살짝 굽힌 미니 스쿼트 옆모습'), gap(48),
        '<p class="body">무게를 조금씩 올린 힘줄 운동 24주,<br>기능 점수 <span class="strong accent">+28점</span> (기존 운동 +18점)</p>', gap(20),
        '<p class="note">무릎뼈 주변 통증 → 엉덩이 + 허벅지 근력 운동을 함께</p>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>슬개골 스트랩 {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
