"""러닝 듀티팩터 카드 HTML 생성: source/01.html ~ 10.html (tools/cardkit의 qa.js·layers.js 포함).
글은 h1/p, 굵기 500·650·700·750·800·850만, 사진은 overflow:hidden 크롭 안의 img.
사용: python content/running-duty-factor/source/build.py"""
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
    # 01 표지 — 러너 속마음 말풍선(밈)
    ('kind-cover', [
        '<h1 class="headline">접지,<br>짧을수록 <span class="accent">좋을까?</span></h1>', gap(48),
        photo('cover.jpg', 640, 960, -36, -2, '공중에 크게 뜬 러너',
              '<div class="bubble"><p>“접지 줄이라는데…<br>더 튀어야 하나?”</p></div>'), gap(44),
        '<p class="body">가민 숫자 2개로 보는 내 러닝 스타일<br><span class="strong accent">듀티팩터</span></p>']),
    # 02 정의
    ('kind-define', [
        '<h1 class="headline">한 걸음 중<br><span class="accent">땅에 붙어 있는</span><br>시간의 비율</h1>', gap(32),
        photo('s02_side.jpg', 260, 888, 0, -316, '한 발이 땅에 닿은 러너 측면'), gap(40),
        '<p class="body">한쪽 발이 닿았다가 다시 닿을 때까지를<br>100으로 보면, 그중 땅에 붙어 있는<br>비율이 <span class="strong">듀티팩터(DF)</span>입니다.</p>', gap(28),
        '<div class="box"><p class="body"><span class="strong accent">DF가 낮다</span> → 통통 튀며 공중에 오래</p>'
        '<p class="body"><span class="strong accent">DF가 높다</span> → 땅에 오래 붙어 가는 달리기</p></div>', gap(24),
        '<p class="note">같은 속도에서 비교합니다</p>']),
    # 03 케이던스 vs DF
    ('kind-cadence', [
        '<h1 class="headline">케이던스만 보면<br><span class="accent">절반</span>만 보입니다</h1>', gap(40),
        photo('s03_pair.jpg', 300, 888, 0, -262, '나란히 달리는 두 러너'), gap(36),
        '<p class="body">케이던스는 발을 <span class="strong">‘얼마나 자주’</span> 딛는지,<br>DF는 그중 땅에 머무는 <span class="strong">‘비율’</span>입니다</p>', gap(28),
        '<div class="box"><p class="body">똑같이 170spm이어도</p>'
        '<p class="item">접지 0.22초 → DF 약 <span class="accent">31%</span></p>'
        '<p class="item">접지 0.28초 → DF 약 <span class="accent">40%</span></p></div>', gap(28),
        '<p class="note">같은 케이던스라도 땅과 공중에 머무는<br>시간 배분이 다릅니다</p>']),
    # 04 가민 계산
    ('kind-calc', [
        '<h1 class="headline">가민으로<br><span class="accent">내 DF</span> 계산하기</h1>', gap(40),
        photo('s04_watch.jpg', 330, 888, 0, -130, '달리며 손목 워치를 보는 모습'), gap(40),
        '<div class="list" style="gap:14px"><p class="item">① 평균 지면 접촉 시간 (ms)</p>'
        '<p class="item">② 평균 러닝 회전수 (spm, 양발)</p></div>', gap(32),
        '<div class="box"><p class="key">DF(%) ≈ <span class="accent">① × ② ÷ 1200</span></p>'
        '<p class="body">예) 250 × 170 ÷ 1200 ≈ 35%</p></div>', gap(28),
        '<p class="note">페이스가 일정한 같은 랩의 값으로 계산한<br>근사치입니다 · 보폭은 필요 없어요</p>']),
    # 05 비교
    ('kind-compare', [
        '<h1 class="headline">내 DF는<br><span class="accent">높은 편</span>일까?</h1>', gap(36),
        '<p class="body">빨라질수록 DF는 자연스럽게 낮아집니다.<br><span class="strong">같은 페이스끼리</span> 비교하세요.</p>', gap(44),
        '<p class="note">러너 115명 평균 (트레드밀 측정)</p>', gap(20),
        '<div class="box" style="gap:26px;padding:44px 40px">' + row('6:40/km', '37.7%') + row('5:27/km', '34.7%')
        + row('4:37/km', '32.6%') + '</div>', gap(40),
        '<p class="key">‘높은 편 / 낮은 편’까지만</p>', gap(16),
        '<p class="body">정상 범위나 목표치가 아닙니다.<br>워치 값과 실험실 측정은 다를 수 있어요.</p>']),
    # 06 스타일 지도(밈)
    ('kind-styles', [
        '<h1 class="headline">완벽한 자세는<br><span class="accent">없다고..!!!!!</span></h1>', gap(40),
        photo('s06_group.jpg', 290, 888, 0, -150, '다양한 모습으로 함께 달리는 러너들'), gap(36),
        '<p class="body">DF와 케이던스(다리 길이 고려)를<br>두 축으로 그려 보면 다섯 방향으로<br>설명할 수 있습니다.</p>', gap(24),
        '<div class="box" style="gap:8px"><p class="item">튀는 쪽 Bounce · 붙는 쪽 Stick</p>'
        '<p class="item">잰걸음 쪽 Hop · 큰 걸음 쪽 Push</p><p class="item">가운데 Sit</p></div>', gap(24),
        '<p class="note">경계선도, 정답 위치도 없는 개념 지도입니다</p>']),
    # 07 이코노미
    ('kind-economy', [
        '<h1 class="headline">더 튀면<br>에너지도 <span class="accent">덜 쓸까?</span></h1>', gap(40),
        photo('s07_bounce.jpg', 420, 888, 0, -86, '높이 튀어 오른 러너'), gap(40),
        '<p class="body">같은 속도를 유지하는 데 드는 에너지<br>(러닝 이코노미)를 비교했더니</p>', gap(28),
        '<p class="key">DF가 낮은 러너와 높은 러너,<br><span class="accent">차이를 확인하지 못했습니다</span></p>', gap(28),
        '<p class="note">숙련 러너 40명 · 시속 10~14km<br>‘똑같다’를 증명한 것은 아닙니다</p>']),
    # 08 몸속 부하
    ('kind-load', [
        '<h1 class="headline">힘의 종류마다<br><span class="accent">결과가 달랐습니다</span></h1>', gap(24),
        '<p class="body">“덜 위아래로 움직이세요” 지시로<br>DF를 높였더니</p>', gap(8),
        '<p class="note">통증 없는 초보 여성 러너 19명 · 한 번의 실험</p>', gap(24),
        '<div class="box"><p class="item accent">낮아진 것</p>'
        '<p class="body">땅을 누르는 최대 힘<br>발목·무릎·엉덩이 관절에 걸리는 최대 힘<br>무릎·발목을 펴는 최대 회전력</p></div>', gap(16),
        '<div class="box"><p class="item">높아진 것</p><p class="body">엉덩이를 펴고 굽히는 최대 회전력</p></div>', gap(20),
        '<p class="note">관절에 걸리는 힘: 관절을 통해 전달되는 힘<br>회전력: 관절을 펴거나 굽히는 방향으로 도는 힘<br>몸속 힘은 촬영·지면반력으로 계산한 값</p>']),
    # 09 왜
    ('kind-why', [
        '<h1 class="headline">‘접지는 짧게’,<br>꼭 따라야 할까?</h1>', gap(40),
        photo('s09_check.jpg', 360, 888, 0, -110, '트레이너와 러너가 워치를 함께 보는 모습'), gap(40),
        '<p class="body">DF로 나눠 비교한 연구에서 통통 튀는 쪽이<br>에너지를 덜 쓴다는 결과는 나오지 않았습니다.<br>꼭 통통 뛸 필요는 없습니다.</p>', gap(32),
        '<p class="key">내 DF를 알아 두면<br>자세를 바꿀 때 <span class="accent">무엇이 함께<br>바뀌는지</span> 볼 수 있습니다</p>']),
    # 10 마무리
    ('kind-summary', [
        '<h1 class="headline">워치 숫자는<br>성적표가 아니라<br><span class="accent">단서</span>입니다</h1>', gap(40),
        photo('s10_smile.jpg', 490, 888, 0, -60, '워치를 보며 웃는 러너'), gap(44),
        '<div class="box"><p class="safety">수치가 바뀌었다고 좋아진 것은 아닙니다.<br>통증이 있다면 자세를 바꾸기 전에<br>전문가 평가를 먼저 받으세요.</p></div>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>러닝 듀티팩터 {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
