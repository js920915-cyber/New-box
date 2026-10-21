"""슬개건병증 부하 카드 HTML 생성: source/01.html ~ 07.html (tools/cardkit의 qa.js·layers.js 포함).
글은 h1/p, 굵기 500·650·700·750·800·850만, 사진·그림은 overflow:hidden 크롭 안의 img.
4장 막대그래프와 7장 통증 척도는 div 배경(→ PPTX 실제 도형)과 p(→ 편집 가능한 글)로 만든다.
사용: python3 content/patellar-tendinopathy-loading/source/build.py"""
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
.key{{font-size:52px;font-weight:800;line-height:1.3;letter-spacing:-.03em}}
.item{{font-size:44px;font-weight:800;line-height:1.3;letter-spacing:-.03em}}
.note{{font-size:36px;font-weight:500;line-height:1.4;color:var(--muted);letter-spacing:-.02em}}
.src{{font-size:30px;font-weight:500;line-height:1.35;color:var(--muted);letter-spacing:-.01em}}
.accent{{color:var(--blue)}} .warn{{color:var(--red)}}
.photo{{position:relative;overflow:hidden;width:888px;flex:none}}
.card>*{{flex-shrink:0}}
.photo img{{position:absolute;display:block}}
.cols{{display:flex;width:888px}}
.col{{flex:1;display:flex;flex-direction:column;align-items:center}}
.bars{{width:888px;display:flex;flex-direction:column;gap:18px}}
.row{{display:flex;align-items:center;height:60px}}
.row .name{{width:372px;flex:none;font-size:36px;font-weight:650;line-height:1.3;letter-spacing:-.03em}}
.row .track{{flex:1;display:flex;align-items:center;gap:16px;height:64px}}
.row .bar{{height:52px;border-radius:8px;background:#c9d9e6}}
.row .val{{font-size:38px;font-weight:750;line-height:1.3;width:104px;flex:none}}
.row.hi .bar{{background:var(--blue)}}
.scale{{display:flex;gap:6px;width:888px}}
.scale .n{{flex:1;height:72px;border-radius:8px;background:#e8edf1;display:flex;align-items:center;justify-content:center}}
.scale .n.ok{{background:#cfe6f8}}
.scale .n p{{font-size:32px;font-weight:700;line-height:1}}
.pop{{position:relative;width:888px}}
.chip{{position:absolute;background:var(--blue);color:#fff;font-size:36px;font-weight:750;line-height:1.3;letter-spacing:-.03em;padding:6px 18px;border-radius:12px}}
.badge{{position:absolute;left:328px;top:-16px;background:var(--red);color:#fff;font-size:40px;font-weight:800;line-height:1.3;letter-spacing:-.03em;padding:8px 26px;border-radius:40px}}
.checks{{display:flex;flex-direction:column;align-items:center;gap:26px}}
"""
FRAME = ('<svg class="card-frame" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">'
         '<rect x="35" y="35" width="1010" height="1280" rx="28" fill="none" stroke="#D0DCE5" stroke-width="2"/></svg>')


def photo(src, w, h, iw, ix, iy, alt, folder='photos'):
    """보이는 창 w×h, 이미지 폭 iw, 창 기준 위치(ix, iy) → 크롭"""
    return (f'<div class="photo" style="width:{w}px;height:{h}px"><img src="../assets/{folder}/{src}" alt="{alt}" '
            f'style="width:{iw}px;left:{ix}px;top:{iy}px"></div>')


def illust(src, w, h, alt):
    return photo(src, w, h, w, 0, 0, alt, 'illust')


def chip(text, x, y):
    """넘치는 컵 위·옆에 얹는 훈련 단어 박스(PPTX에서 도형+글자)"""
    return f'<p class="chip" style="left:{x}px;top:{y}px">{text}</p>'


def gap(px):
    return f'<div style="height:{px}px;flex:none"></div>'


def src_line(text):
    return f'<p class="src">{text}</p>'


# Scattone Silva 2024 초록 수치 (patellar tendon loading index)
PTLI = [('양발 60° 스쿼트', 0.224), ('불가리안 스쿼트', 0.406), ('양발 풀 스쿼트', 0.428),
        ('한발 반동 점프', 0.711), ('한발 디클라인 스쿼트', 0.747)]
BAR_MAX = 390  # 0.8 → 약 470px


def bars():
    rows = []
    for name, v in PTLI:
        rows.append(f'<div class="row{" hi" if v > .7 else ""}"><p class="name">{name}</p><div class="track">'
                    f'<div class="bar" style="width:{round(v / .75 * BAR_MAX)}px"></div><p class="val">{v:.3f}</p></div></div>')
    return '<div class="bars">' + ''.join(rows) + '</div>'


def scale():
    cells = ''.join(f'<div class="n{" ok" if i <= 3 else ""}"><p>{i}</p></div>' for i in range(11))
    return f'<div class="scale">{cells}</div>'


def ft(col, img, head, sub):
    return (f'<div class="col">{illust(img, 272, 220, head + " 힘-시간 모식도")}{gap(16)}'
            f'<p class="item" style="font-size:40px">{head}</p>{gap(4)}<p class="note">{sub}</p></div>')


CARDS = [
    # 01 표지
    ('kind-cover', [
        '<h1 class="headline">슬개건병증,<br>무조건 쉬면 <span class="accent">좋아질까?</span></h1>', gap(44),
        photo('cover-box-jump_nenad53_ccby20.jpg', 888, 740, 888, 0, -330, '박스 점프 후 무릎을 굽혀 착지하는 선수'), gap(36),
        '<p class="body">아픈 힘줄에 다시 <span class="strong">운동이 필요한 이유</span></p>']),
    # 02 물컵: 부하 > 능력
    ('kind-cup', [
        '<h1 class="headline">힘줄에도<br>감당할 수 있는<br><span class="accent">부하</span>가 있습니다</h1>', gap(28),
        '<div class="pop">' + illust('cups2.png', 888, 310, '적당히 찬 물컵과 훈련이 몰려 넘치는 물컵')
        + chip('무리한 대회', 551, 30) + chip('템포', 612, -20) + chip('인터벌', 446, 112) + chip('장거리', 746, 156)
        + '<p class="badge">앗! 통증?!</p></div>', gap(16),
        '<div class="cols"><div class="col"><p class="note">컵 = 감당할 수 있는 능력<br>물 = 운동 부하</p></div>'
        '<div class="col"><p class="note">훈련이 한꺼번에<br><span class="accent strong">갑자기</span> 몰리면</p></div></div>', gap(36),
        '<p class="body">운동량이나 강도가 갑자기 늘면<br>감당 능력을 넘어설 수 있습니다.</p>', gap(28),
        '<p class="item">문제는 운동 자체보다<br><span class="accent">갑작스러운 증가</span>일 수 있습니다</p>', gap(24),
        src_line('참고: Cook et al., Br J Sports Med 2016')]),
    # 03 물컵: 점진적 부하
    ('kind-grow', [
        '<h1 class="headline">힘줄 재활의 핵심은<br><span class="accent">점진적인 부하</span>입니다</h1>', gap(40),
        illust('cups3.png', 888, 420, '작은 컵에서 큰 컵으로, 물도 넘치지 않게 조금씩 늘어나는 그림'), gap(12),
        '<p class="note">컵이 커지는 것 = 감당 능력이 늘어나는 것</p>', gap(40),
        '<p class="body">힘줄은 부하에 적응하는 조직입니다.<br>감당 가능한 운동부터 단계적으로!</p>', gap(36),
        '<p class="item">무조건 쉬기보다,<br><span class="accent">감당 가능한 부하</span>부터</p>', gap(24),
        src_line('참고: Cook 2016 · Kongsgaard 2009 · Breda 2021')]),
    # 04 운동별 부하 지수
    ('kind-bars', [
        '<h1 class="headline">운동마다 힘줄이<br>받는 <span class="accent">부하</span>는 다릅니다</h1>', gap(32),
        '<p class="body">스쿼트부터 점프까지, 운동마다<br>힘의 크기와 증가 속도가 다릅니다.</p>', gap(40),
        '<p class="note">슬개건 부하 지수 (건강한 성인 20명)</p>', gap(14),
        bars(), gap(32),
        '<p class="item">어떤 운동이냐에 따라<br><span class="accent">부하의 특성</span>이 달라집니다</p>', gap(12),
        '<p class="note">지수가 높다고 위험한 운동은 아닙니다</p>', gap(20),
        src_line('출처: Scattone Silva et al., Med Sci Sports Exerc 2024')]),
    # 05 강도 결정 요소 3가지
    ('kind-three', [
        '<h1 class="headline">무게만이 운동 강도를<br><span class="accent">결정하지 않습니다</span></h1>', gap(32),
        '<p class="body">힘줄이 받는 자극은 힘의 크기,<br>증가 속도, 지속 시간에 따라 달라집니다.</p>', gap(44),
        '<div class="cols" style="gap:36px">'
        + ft(1, 'ft-peak.png', '힘의 크기', '얼마나<br>큰 힘?')
        + ft(2, 'ft-rate.png', '증가 속도', '얼마나<br>빠르게 커지나?')
        + ft(3, 'ft-impulse.png', '누적 부하', '시간 동안<br>얼마나 쌓이나?') + '</div>', gap(12),
        '<p class="note">가로 = 시간, 세로 = 힘 (개념 그림)</p>', gap(40),
        '<p class="item">무게뿐 아니라 <span class="accent">힘이 커지는 속도</span>와<br>지속 시간도 함께 봅니다</p>', gap(20),
        src_line('참고: Scattone Silva et al., Med Sci Sports Exerc 2024')]),
    # 06 근력 → 빠른 힘
    ('kind-pair', [
        '<h1 class="headline">강한 힘에서<br><span class="accent">빠른 힘</span>까지!</h1>', gap(32),
        '<p class="body">근력을 회복한 뒤에는 점프·착지처럼<br>빠르고 반복적인 부하에도 적응합니다.</p>', gap(36),
        '<div class="cols" style="gap:24px"><div class="col">'
        + photo('barbell-squat_ThoroughlyReviewed_ccby20.jpg', 432, 404, 608, -110, 0, '바벨을 메고 스쿼트하는 여성')
        + gap(16) + '<p class="item">천천히, 높은 힘</p><p class="note">최대 근력 · 저항운동</p></div><div class="col">'
        + photo('box-jump-air_nenad53_ccby20.jpg', 432, 404, 500, -60, -190, '박스 위로 점프하는 선수')
        + gap(16) + '<p class="item">빠르게, 반복적으로</p><p class="note">빠른 부하 · 스포츠 동작</p></div></div>', gap(36),
        '<p class="item">근력이 좋아져도 점프 능력이<br><span class="accent">저절로</span> 돌아오지는 않습니다</p>', gap(20),
        src_line('참고: Breda et al., Br J Sports Med 2021')]),
    # 07 강도 올리는 시점 + 결론
    ('kind-when', [
        '<h1 class="headline">그럼 운동 강도는<br><span class="accent">언제</span> 높여야 할까요?</h1>', gap(48),
        '<div class="checks"><p class="body">① 지금 운동을 안정적으로 하는가?</p>'
        '<p class="body">② 운동 중 통증이 관리 가능한가?</p>'
        '<p class="body">③ 다음 날 증상이 나빠지지 않는가?</p></div>', gap(52),
        scale(), gap(18),
        '<p class="note">연구 예시: 한발 스쿼트 통증 <span class="accent strong">3/10 이하</span>,<br>한 단계 최소 1주 수행 후 다음 단계</p>', gap(48),
        '<p class="item">중량·범위·속도·반복량을 <span class="accent">조금씩 ↑</span></p>', gap(56),
        '<p class="key">재활의 목표는 통증 감소를 넘어<br><span class="accent">다시 뛰고 점프하는 것</span>입니다</p>', gap(18),
        src_line('참고: Breda 2021 (모든 사람의 기준은 아님)')]),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>슬개건병증 {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
