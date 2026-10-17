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

.flow{{font-size:42px;font-weight:750;line-height:1.3;letter-spacing:-.03em}}
.arrow{{font-size:34px;font-weight:800;line-height:1.05;color:var(--blue)}}
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
    # 03 효과 — 얼굴 통증 척도 (de Vries 2016 Table 2 중앙값 ÷10)
    ('kind-effect', [
        '<h1 class="headline">진짜 스트랩 vs<br><span class="accent">가짜 테이프</span><br>실험해 봤습니다</h1>', gap(24),
        '<div class="photo" style="height:440px"><img src="../assets/charts/vas.png" alt="0~10 얼굴 통증 척도: 안 찼을 때 3.3에서 가짜 테이프 2.6, 진짜 스트랩 1.9로 감소" style="width:888px;left:0;top:0"></div>', gap(8),
        '<p class="note" style="font-size:32px;line-height:1.35">슬개건병증 선수 97명 · 한 다리 경사 스쿼트 10회 통증<br>가짜 테이프 = 힘줄을 누르지 않게 짧게 붙인 테이프</p>', gap(20),
        '<div class="box" style="padding:26px 40px;display:flex;flex-direction:column;gap:6px">'
        '<p class="flow">① 진짜 스트랩: <span class="accent">확실히 ↓</span></p>'
        '<p class="flow">② 가짜 테이프: 조금 ↓ (확실하진 않음)</p>'
        '<p class="flow">③ 스트랩 vs 가짜 테이프 → <span class="accent">큰 차이 없음</span></p></div>']),
    # 04 기전 가설 ① 흐름 + X선
    ('kind-mech1', [
        '<h1 class="headline">기전 가설 ①<br><span class="accent">힘줄이 덜 당겨진다?</span></h1>', gap(32),
        '<div class="photo" style="width:460px;height:400px;border-radius:16px"><img src="../assets/photos/xray-knee-lateral_Haggstrom_cc0_ppta.png" alt="무릎 옆모습 X선, 무릎뼈 축과 슬개건 사이 각도(PPTA) 표시" style="width:460px;left:0;top:0"></div>', gap(28),
        '<div class="list" style="gap:0">'
        '<p class="flow">슬개건 스트랩 착용</p><p class="arrow">↓</p>'
        '<p class="flow">슬개건에 국소 압박</p><p class="arrow">↓</p>'
        '<p class="flow">슬개골–슬개건 각도·유효 길이 변화</p>'
        '<p class="note" style="font-size:32px;line-height:1.3">각도 = PPTA (patella–patellar tendon angle)</p><p class="arrow">↓</p>'
        '<p class="flow accent">슬개건 변형률(strain) 감소 가능성</p></div>', gap(24),
        '<p class="body" style="font-size:42px">그런데 이것 때문에 통증이 줄었는지는 <span class="strong warn">아직 모름</span></p>']),
    # 05 이유 ② 감각과 기대
    ('kind-mech2', [
        '<h1 class="headline">부딪힌 팔꿈치를<br><span class="accent">문지르면</span> 덜 아픈 것처럼</h1>', gap(130),
        '<p class="key" style="font-weight:750">피부를 누르는 감각이<br><span class="accent">통증 신호를 덮을 수</span> 있습니다</p>', gap(88),
        '<p class="key" style="font-weight:750">여기에 <span class="accent">‘차면 덜 아파’</span><br>기대도 더해질 수 있습니다</p>', gap(130),
        '<div class="box" style="padding:44px 40px"><p class="note" style="color:var(--ink);font-size:38px"><span class="strong">논문 저자들의 해석</span><br>뭐든 붙이면 피부가 자극돼 통증 신호가 바뀐다<br>스트랩은 힘줄 압박이 조금 더 보탰을 수 있다</p></div>']),
    # 06 슬개건병증 통증 부위
    ('kind-who', [
        '<h1 class="headline"><span class="accent">슬개건병증</span>,<br>여기가 아프다면</h1>', gap(40),
        '<div class="photo" style="height:560px"><img src="../assets/photos/knee-downhill_Memphre_ccbysa30_marked.png" alt="내리막을 걷는 사람의 무릎, 무릎뼈 바로 아래에 빨간 원 표시" style="width:888px;left:0;top:0"></div>', gap(40),
        '<p class="body">점프·착지·내리막에서 아픈 자리.<br>스트랩을 차면 <span class="strong">단기 통증 감소</span>가 보고됐습니다.</p>', gap(20),
        '<p class="note">무릎뼈 주변·뒤가 아픈 슬개대퇴통증에는<br>가이드라인이 스트랩을 권하지 않습니다</p>']),
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
