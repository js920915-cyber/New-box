"""달리기 자세 카드 HTML 생성: source/01.html ~ 10.html (tools/cardkit의 qa.js·layers.js 포함).
글은 h1/p, 굵기 500·650·700·750·800·850만, 사진은 overflow:hidden 크롭 안의 img.
사용: python content/running-form-change/source/build.py"""
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
.photo{{position:relative;overflow:hidden;width:888px;border-radius:20px;flex:none}}
.photo img{{position:absolute;display:block}}
.bubble{{position:absolute;right:24px;top:24px;background:#fff;border-radius:24px;padding:18px 30px}}
.bubble p{{font-size:40px;font-weight:750;line-height:1.32;letter-spacing:-.03em}}
.list{{display:flex;flex-direction:column;align-items:center;gap:30px}}
.pair{{display:flex;flex-direction:column;align-items:center;gap:6px}}
.box{{background:var(--tint);border-radius:20px;padding:30px 40px;width:888px;display:flex;flex-direction:column;align-items:center;gap:12px}}
.row{{display:flex;justify-content:center;align-items:baseline;gap:48px}}
.center{{justify-content:center;padding-bottom:20px}}
.big{{font-size:72px;font-weight:850;line-height:1.15;letter-spacing:-.03em}}
"""
FRAME = ('<svg class="card-frame" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">'
         '<rect x="35" y="35" width="1010" height="1280" rx="28" fill="none" stroke="#D0DCE5" stroke-width="2"/></svg>')


def photo(src, h, iw, ix, iy, alt, extra=''):
    """보이는 창 888×h, 이미지 폭 iw, 창 기준 위치(ix, iy) → 크롭"""
    return (f'<div class="photo" style="height:{h}px"><img src="../assets/photos/{src}" alt="{alt}" '
            f'style="width:{iw}px;left:{ix}px;top:{iy}px">{extra}</div>')


def gap(px):
    return f'<div style="height:{px}px;flex:none"></div>'


def row(pace, val):
    return f'<div class="row"><p class="item">{pace}</p><p class="big accent">{val}</p></div>'


CARDS = [
    # 01 표지 — 유튜브 자세 따라 하다 당황한 러너(밈)
    ('kind-cover', [
        '<h1 class="headline">달리기 자세,<br><span class="accent">무작정</span> 배우지 마세요</h1>', gap(48),
        photo('cover.jpg', 640, 960, -36, 0, '영상 속 자세를 어색하게 따라 하는 러너',
              '<div class="bubble"><p>“영상에서<br>이렇게 뛰라던데…”</p></div>'), gap(44),
        '<p class="body">자세를 바꾸기 전에<br><span class="strong accent">꼭 확인할 것</span></p>']),
    # 02 문제
    ('kind-problem', [
        '<h1 class="headline">‘정답 자세’에는<br><span class="accent">내 몸</span>이 빠져 있습니다</h1>', gap(40),
        photo('s02_group.jpg', 470, 888, 0, -40, '나이와 체형이 다른 러너 네 명'), gap(40),
        '<p class="body">근력, 평소 달리는 양, 다친 이력,<br>달리는 스타일은 사람마다 다릅니다.</p>', gap(24),
        '<p class="key">같은 자세가 모두에게<br><span class="accent">같은 결과</span>를 주지는 않습니다</p>']),
    # 03 연구 설계
    ('kind-design', [
        '<h1 class="headline">자세를 바꾸면<br>어떻게 될까?</h1>', gap(28),
        '<p class="note">홍콩 초보 러너 연구 (무작위 대조 시험)</p>', gap(36),
        '<p class="body">달리기 2년 미만, 최근 6개월 부상 없고<br><span class="strong">착지 충격이 큰</span> 러너 390명을<br>무작위로 두 그룹으로 나눴습니다</p>', gap(36),
        '<div class="box"><p class="item accent">재훈련 그룹</p>'
        '<p class="body">트레드밀 화면의 충격 그래프를 보며<br>“더 부드럽게 착지하세요” · 2주 8회</p></div>', gap(20),
        '<div class="box"><p class="item">비교 그룹</p><p class="body">같은 시간, 그냥 달리기</p></div>', gap(32),
        '<p class="note">이후 1년 동안 부상을 추적했습니다</p>']),
    # 04 결과①
    ('kind-result1 center', [
        '<h1 class="headline">충격은 줄었고,<br>부상도 <span class="accent">적었습니다</span></h1>', gap(40),
        '<p class="body">재훈련 그룹은 착지 충격<br>(착지 순간 힘이 올라가는 속도)이<br>크게 줄었습니다</p>', gap(48),
        '<p class="note">1년 동안 부상을 겪은 비율</p>', gap(20),
        '<div class="box" style="gap:26px;padding:44px 40px">'
        '<div class="row"><p class="item">재훈련 그룹</p><p class="big accent">16%</p></div>'
        '<div class="row"><p class="item">비교 그룹</p><p class="big">38%</p></div></div>', gap(40),
        '<p class="note">끝까지 추적한 320명 기준</p>']),
    # 05 결과② — 부상 종류
    ('kind-result2', [
        '<h1 class="headline">그런데 <span class="warn">다른 곳</span>에서<br>부상이 나왔습니다</h1>', gap(32),
        photo('s05_calf.jpg', 330, 888, 0, -140, '종아리 뒤쪽을 잡고 멈춘 러너'), gap(32),
        '<div class="box"><p class="body">재훈련 그룹에서만</p>'
        '<p class="item"><span class="warn">아킬레스건염 5건 · 종아리 염좌 5건</span></p>'
        '<p class="body">비교 그룹은 0건<br>(대신 족저근막염·무릎 앞쪽 통증이 많았음)</p></div>', gap(20),
        '<p class="note">연구진은 착지를 바꾸면서 종아리 부담이<br>커졌을 가능성을 제시했습니다<br>(실제 착지 변화·원인은 확인 안 됨)</p>']),
    # 06 메시지 (여기부터 센터 제안)
    ('kind-message center', [
        '<p class="note">여기부터는 센터의 제안입니다</p>', gap(28),
        '<h1 class="headline">줄어드는 부상이 있어도<br><span class="warn">새로운 부상</span>이<br>생길 수 있습니다</h1>', gap(48),
        '<p class="body">자세를 바꾸면 몸이 받는 부담도<br>함께 달라질 수 있습니다.</p>', gap(40),
        '<div class="box"><p class="key">바꾸기 전에<br><span class="accent">내 몸이 버틸 준비</span>가<br>됐는지 먼저 확인하세요</p></div>']),
    # 07 확인 ① ②
    ('kind-check12 center', [
        '<h1 class="headline">바꾸기 전<br><span class="accent">확인할 것</span></h1>', gap(48),
        '<div class="box"><p class="item accent">① 왜 바꾸나요?</p>'
        '<p class="body">통증? 기록? 편안함?<br>무엇으로 좋아졌는지 판단할지도<br>미리 정하세요</p></div>', gap(28),
        '<div class="box"><p class="item accent">② 지금 얼마나 달리나요?</p>'
        '<p class="body">주간 거리, 달린 기간<br>최근에 늘린 거리·속도<br>최근에 바꾼 신발</p></div>']),
    # 08 확인 ③
    ('kind-check3', [
        '<h1 class="headline">③ 내 몸은<br><span class="accent">준비</span>됐나요?</h1>', gap(40),
        photo('s08_assess.jpg', 584, 888, 0, -8, '트레이너가 한 발 뒤꿈치 들기를 확인하는 모습'), gap(40),
        '<p class="body">다친 이력, 근력(예: 종아리),<br>착지 패턴, 러닝 스타일</p>', gap(24),
        '<p class="note">모든 검사가 필요한 건 아닙니다.<br>바꾸려는 자세에 필요한 것만 확인하세요.</p>']),
    # 09 확인 ④ 천천히
    ('kind-slow', [
        '<h1 class="headline">④ 바꿀 땐<br>한 번에 하나,<br><span class="accent">천천히</span></h1>', gap(40),
        photo('s09_easy.jpg', 480, 888, 0, -50, '편안하게 천천히 달리는 러너'), gap(40),
        '<p class="body">짧은 구간부터 조금씩 늘리고<br>새로 생기는 <span class="strong">통증·피로</span>를 살피세요</p>', gap(24),
        '<p class="note">위 연구에서도 2주 동안 15분→30분으로<br>늘려 갔습니다(모두에게 맞는 기간은 아닙니다)</p>']),
    # 10 정리
    ('kind-summary', [
        '<h1 class="headline">자세는 따라 하는 게<br>아니라 내 몸에 맞게<br><span class="accent">다듬는 것</span>입니다</h1>', gap(40),
        photo('s10_smile.jpg', 460, 888, 0, -60, '달리기를 마치고 웃는 러너'), gap(44),
        '<div class="box"><p class="safety">통증이 있거나 부상이 반복된다면<br>자세를 바꾸기 전에<br>원인 평가를 먼저 받으세요.</p></div>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>달리기 자세 {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
