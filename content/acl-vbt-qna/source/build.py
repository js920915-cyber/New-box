"""ACL 재활 VBT 문답 카드 HTML 생성: source/01.html ~ 07.html (tools/cardkit의 qa.js·layers.js 포함).
좌(나: 조진솔 PT)·우(Andreas) 얼굴 + 말풍선 문답. 글은 h1/p, 굵기 500·650·700·750·800·850만,
사진은 overflow:hidden 크롭 안의 img, 말풍선은 background-color(→ PPTX 둥근 사각형).
사용: python3 content/acl-vbt-qna/source/build.py"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parents[2] / 'tools/cardkit'
FONT = '../../../templates/fonts/NotoSansKR-VF.ttf'
SCRIPTS = ''.join(f'<script>{(KIT / n).read_text(encoding="utf-8")}</script>' for n in ('qa.js', 'layers.js'))

CSS = f"""
@font-face{{font-family:'Noto Sans KR';src:url('{FONT}');font-weight:100 900}}
:root{{--ink:#121416;--muted:#5e6570;--blue:#0879d8;--red:#cc414a;--tint:#f0f7fc;--gray:#f2f4f6}}
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
.name{{font-size:36px;font-weight:700;line-height:1.3;letter-spacing:-.02em}}
.safety{{font-size:38px;font-weight:700;line-height:1.42;letter-spacing:-.02em}}
.big{{font-size:128px;font-weight:850;line-height:1.08;letter-spacing:-.04em}}
.accent{{color:var(--blue)}}
.photo{{position:relative;overflow:hidden;width:888px}}
.photo img{{position:absolute;display:block}}
/* 문답 */
.chat{{width:888px;display:flex;flex-direction:column;gap:36px}}
.row{{display:flex;align-items:flex-start;gap:24px;width:888px}}
.row.me{{flex-direction:row}} .row.you{{flex-direction:row-reverse}}
.who{{width:184px;flex:none;display:flex;flex-direction:column;align-items:center;gap:10px}}
.face{{position:relative;overflow:hidden;width:168px;height:168px}}
.face img{{position:absolute;left:0;top:0;width:168px;height:168px;display:block}}
.bubble{{flex:1;border-radius:40px;padding:38px 36px;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:168px}}
.me .bubble{{background:var(--gray)}} .you .bubble{{background:var(--tint)}}
.q{{font-size:52px;font-weight:750;line-height:1.34;letter-spacing:-.03em}}
.a{{font-size:56px;font-weight:800;line-height:1.32;letter-spacing:-.03em}}
/* 하단 근거 블록 */
.pairs{{display:flex;flex-direction:column;align-items:center;gap:52px}}
.pair{{display:flex;flex-direction:column;align-items:center;gap:8px}}
.cmp{{display:flex;justify-content:center;gap:24px;width:888px}}
.cmp .col{{width:432px;border-radius:28px;padding:40px 0 44px;display:flex;flex-direction:column;align-items:center;gap:6px}}
.cmp .col.base{{background:var(--gray)}} .cmp .col.day{{background:var(--tint)}}
.rule{{width:888px;border-top:2px solid #d0dce5;height:0;flex:none}}
.duo{{display:flex;justify-content:center;gap:48px;width:888px}}
.duo .who{{width:420px}}
.duo .face{{width:180px;height:180px}} .duo .face img{{width:180px;height:180px}}
.promo{{display:flex;flex-direction:column;align-items:center;gap:12px}}
"""
FRAME = ('<svg class="card-frame" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">'
         '<rect x="35" y="35" width="1010" height="1280" rx="28" fill="none" stroke="#D0DCE5" stroke-width="2"/></svg>')

ME = ('face_jinsol.png', '조진솔 PT')
YOU = ('face_andreas.png', 'Andreas')


def face(src, alt):
    return f'<div class="face"><img src="../assets/photos/{src}" alt="{alt}"></div>'


def row(side, text):
    src, name = ME if side == 'me' else YOU
    cls = 'q' if side == 'me' else 'a'
    return (f'<div class="row {side}"><div class="who">{face(src, name + " 얼굴")}<p class="name">{name}</p></div>'
            f'<div class="bubble"><p class="{cls}">{text}</p></div></div>')


def chat(q, a):
    return f'<div class="chat">{row("me", q)}{row("you", a)}</div>'


def pair(head, sub, cls='item', sub_cls='body'):
    return f'<div class="pair"><p class="{cls}">{head}</p><p class="{sub_cls}">{sub}</p></div>'


def gap(px):
    return f'<div style="height:{px}px;flex:none"></div>'


CARDS = [
    # 01 표지
    ('kind-cover', [
        '<h1 class="headline">ACL 재활,<br><span class="accent">무게만</span> 보면<br>될까요?</h1>', gap(40),
        '<div class="photo" style="height:440px"><img src="../assets/photos/cover-barbell-squat_USMC-Salazar_pd.jpg" '
        'alt="랙에서 바벨 백스쿼트를 하는 사람 정면" style="width:888px;left:0;top:-90px"></div>', gap(44),
        '<div class="duo">'
        f'<div class="who">{face(*ME)}<p class="name">조진솔 PT가 묻고</p></div>'
        f'<div class="who">{face(*YOU)}<p class="name">Andreas가 답합니다</p></div>'
        '</div>']),
    # 02 Q1
    ('kind-q1', [
        chat('ACL 수술 후, 스쿼트는<br>몇 kg부터 해야 할까요?', '<span class="accent">무게만으로는</span><br>충분하지 않습니다.'), gap(72),
        '<div class="rule"></div>', gap(64),
        '<div class="pairs">'
        + pair('그날 낼 수 있는 힘이 다릅니다', '피로·수면·회복·증상에 따라<br>같은 사람도 날마다 달라질 수 있습니다')
        + pair('최대 무게를 매번 잴 수 없습니다', '수술 후 초기에는 1RM 측정이<br>적절하지 않을 수 있습니다') + '</div>']),
    # 03 Q2 — 같은 60kg, 다른 속도
    ('kind-q2', [
        chat('같은 60kg도<br>다르게 봐야 한다고요?', '네. 같은 무게라도<br><span class="accent">움직이는 속도</span>는<br>달라질 수 있죠.'), gap(60),
        '<div class="cmp">'
        '<div class="col base"><p class="note">평소 · 60kg</p><p class="key" style="font-size:64px">0.80 m/s</p></div>'
        '<div class="col day"><p class="note">다른 날 · 60kg</p><p class="key accent" style="font-size:64px">0.65 m/s</p></div>'
        '</div>', gap(44),
        '<p class="body">꼭 약해졌다는 뜻은 아니지만<br>컨디션을 확인하고 계획을<br><span class="strong">조정할 이유</span>가 됩니다.</p>']),
    # 04 Q3 — 강도와 피로
    ('kind-q3', [
        chat('그런데 속도가<br>왜 중요한가요?', '운동 <span class="accent">강도</span>와 <span class="accent">피로</span><br>변화를 파악하는 데<br>도움이 되기 때문입니다.'), gap(64),
        '<div class="pairs">'
        + pair('강도: 무거울수록 대체로 느려집니다', '속도로 최대 무게 대비<br>몇 %인지(상대 강도)를 추정합니다')
        + pair('피로: 반복할수록 느려집니다', '예: 첫 회 0.80 → 여섯째 0.64 m/s<br>세트 안에서 속도가 20% 줄었습니다') + '</div>']),
    # 05 Q4 — VBT
    ('kind-q4', [
        chat('그럼 속도로 운동 강도를<br>조절할 수 있나요?', '네. 그게 바로<br><span class="accent">VBT, 속도 기반<br>훈련</span>입니다.'), gap(56),
        '<p class="body">들어 올리는 속도(m/s)를 재서<br>운동을 처방하고 확인하는 방법</p>', gap(48),
        '<div class="pairs" style="gap:36px">'
        + pair('무게는 목표 속도로', '%1RM 대신 목표 속도에 맞는 무게')
        + pair('반복 수는 속도 감소로', '속도가 20% 줄면 세트 종료(예시)') + '</div>']),
    # 06 Q5 — ACL 재활
    ('kind-q5', [
        chat('ACL 재활에도<br>활용할 수 있나요?', '환자의 상태와 훈련 목표에<br>맞춰 <span class="accent">부하를 조절</span>하는 데<br>활용할 수 있죠.'), gap(48),
        '<div class="pairs" style="gap:28px">'
        + pair('매 세션 같은 무게로 확인', '같은 무게 스쿼트 3×5, 최대한 빠르게<br>지난 세션 속도와 비교합니다', 'item', 'note')
        + pair('눈에 띄게 느려지면 계획을 바꿉니다', '강도 낮은 운동으로 바꾸거나<br>무게를 줄여 목표 속도에 맞춥니다', 'item', 'note') + '</div>', gap(36),
        '<p class="safety">속도는 통증·부기·움직임과 함께 봅니다.<br>수술별 제한과 증상이 먼저입니다.</p>']),
    # 07 마지막 화면
    ('kind-end', [
        '<h1 class="headline">같은 무게가 항상<br>같은 훈련 자극을<br><span class="accent">의미하지는 않습니다</span></h1>', gap(72),
        '<div class="face" style="width:260px;height:260px"><img src="../assets/photos/face_andreas.png" alt="Andreas 얼굴" style="width:260px;height:260px"></div>', gap(36),
        '<div class="promo">'
        '<p class="item">ACL 재활에서 VBT를 활용하는 이유</p>'
        '<p class="body">Andreas Bjerregaard</p>'
        '<p class="note">2027 Criteria-Based ACL Rehab Workshop</p>'
        '</div>', gap(72),
        '<p class="key">사전 웨비나에서<br>더 자세히 알아보세요.</p>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>ACL VBT 문답 {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
