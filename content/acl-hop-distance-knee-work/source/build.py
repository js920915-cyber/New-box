"""ACL 홉 거리 vs 무릎 일 카드 HTML 생성: source/01.html ~ 06.html (tools/cardkit의 qa.js·layers.js 포함).
글은 h1/p, 굵기 500·650·700·750·800·850만. 그래프는 이미지가 아니라 div(막대·선 → PPTX 도형)와 p(눈금·값 → PPTX 글 상자)로 만든다.
수치 출처: Kotsifaki A et al. BJSM 2022 Table 1·2, Abstract/Discussion(69%). 원 Figure 2·3은 쓰지 않는다(No commercial re-use).
사용: python3 content/acl-hop-distance-knee-work/source/build.py"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parents[2] / 'tools/cardkit'
FONT = '../../../templates/fonts/NotoSansKR-VF.ttf'
SCRIPTS = ''.join(f'<script>{(KIT / n).read_text(encoding="utf-8")}</script>' for n in ('qa.js', 'layers.js'))

INK, MUTED, BLUE, RED, TINT = '#121416', '#5e6570', '#0879d8', '#cc414a', '#f0f7fc'
GREY, TRACK, HIP, ANKLE = '#a7b0b8', '#edf1f4', '#cfd6dc', '#5e6570'

CSS = f"""
@font-face{{font-family:'Noto Sans KR';src:url('{FONT}');font-weight:100 900}}
:root{{--ink:{INK};--muted:{MUTED};--blue:{BLUE};--red:{RED};--tint:{TINT}}}
*{{box-sizing:border-box}} html,body{{margin:0;padding:0;background:#fff}}
.card{{position:relative;width:1080px;height:1350px;padding:104px 96px 98px;overflow:hidden;background:#fff;
 font-family:'Noto Sans KR',sans-serif;color:var(--ink);text-align:center;display:flex;flex-direction:column;align-items:center}}
.card-frame{{position:absolute;inset:0;pointer-events:none}}
h1,p{{margin:0;text-align:center}}
.headline{{font-size:84px;font-weight:850;line-height:1.2;letter-spacing:-.035em}}
.kind-cover .headline{{font-size:88px;line-height:1.18}}
.body{{font-size:44px;font-weight:500;line-height:1.42;letter-spacing:-.02em}}
.strong{{font-weight:750}}
.sub{{font-size:48px;font-weight:700;line-height:1.3;letter-spacing:-.02em}}
.key{{font-size:56px;font-weight:800;line-height:1.3;letter-spacing:-.03em}}
.item{{font-size:48px;font-weight:800;line-height:1.3;letter-spacing:-.03em}}
.note{{font-size:36px;font-weight:500;line-height:1.4;color:var(--muted);letter-spacing:-.02em}}
.note-ink{{font-size:36px;font-weight:650;line-height:1.4;letter-spacing:-.02em}}
.accent{{color:var(--blue)}} .warn{{color:var(--red)}}
.slot{{border-radius:20px;background:var(--tint);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;flex:none}}
.slot .tag{{font-size:36px;font-weight:700;color:var(--blue);line-height:1.3}}
.slot .guide{{font-size:36px;font-weight:500;color:var(--muted);line-height:1.42}}
.chart{{position:relative;width:888px;flex:none}}
.chart .a{{position:absolute;margin:0;white-space:nowrap}}
.lab{{font-size:40px;font-weight:750;line-height:1.3;letter-spacing:-.02em}}
.tick{{font-size:32px;font-weight:500;line-height:1.3;color:var(--muted)}}
.val{{font-size:52px;font-weight:850;line-height:1.15;letter-spacing:-.02em}}
.sd{{font-size:34px;font-weight:650;line-height:1.3;color:var(--muted)}}
.box{{background:var(--tint);border-radius:20px;width:888px;flex:none}}
.cols{{display:flex;justify-content:center}}
.col{{width:264px;display:flex;flex-direction:column;align-items:center;gap:6px}}
.big{{font-size:56px;font-weight:850;line-height:1.2;letter-spacing:-.03em;color:var(--blue)}}
.duo{{display:flex;justify-content:space-between;align-items:center;width:888px;flex:none}}
.person{{width:404px;display:flex;flex-direction:column;align-items:center;gap:18px}}
.name{{font-size:40px;font-weight:800;line-height:1.3;letter-spacing:-.02em}}
.times{{font-size:48px;font-weight:500;line-height:1.3;color:var(--muted);margin-bottom:76px}}
"""
FRAME = ('<svg class="card-frame" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">'
         '<rect x="35" y="35" width="1010" height="1280" rx="28" fill="none" stroke="#D0DCE5" stroke-width="2"/></svg>')


def gap(px):
    return f'<div style="height:{px}px;flex:none"></div>'


def rect(x, y, w, h, color, radius=0):
    r = f';border-radius:{radius}px' if radius else ''
    return f'<div style="position:absolute;left:{x:.1f}px;top:{y:.1f}px;width:{w:.1f}px;height:{h:.1f}px;background:{color}{r}"></div>'


def at(text, cx, top, w, cls, style=''):
    """가운데 정렬 글: 중심 x(cx), 위 y(top), 상자 폭 w"""
    return f'<p class="a {cls}" style="left:{cx - w / 2:.1f}px;top:{top:.1f}px;width:{w}px;{style}">{text}</p>'


def slot(h, tag, guide, w=888):
    return f'<div class="slot" style="width:{w}px;height:{h}px"><p class="tag">{tag}</p><p class="guide">{guide}</p></div>'


def chart_lsi():
    """02: 같은 0~100% 축의 가로 막대 2개 (홉 거리 LSI 97%, 도약 시 무릎 일 LSI 69%)"""
    W, BH = 888, 88
    rows = [('홉 거리 LSI', 97, BLUE, 0), ('도약 시 무릎 관절 일 LSI', 69, RED, 200)]
    s = []
    for label, v, color, y in rows:
        s.append(at(label, W / 2, y, W, 'lab'))
        s.append(rect(0, y + 62, W, BH, TRACK))
        s.append(rect(0, y + 62, W * v / 100, BH, color))
        s.append(at(f'{v}%', W * v / 100 - 74, y + 62 + (BH - 60) / 2, 140, 'val', 'color:#fff'))
    base = 200 + 62 + BH + 14
    s.append(rect(0, base, W, 2, '#d0dce5'))
    for t, x, cx in (('0', 0, 12), ('50', W / 2 - 1, W / 2), ('100%', W - 2, W - 48)):  # 글이 안전 영역 밖으로 나가지 않게 끝 눈금 글은 안쪽으로
        s.append(rect(x, base, 2, 12, '#d0dce5'))
        s.append(at(t, cx, base + 16, 96, 'tick'))
    return f'<div class="chart" style="height:{base + 58}px">{"".join(s)}</div>'


def chart_contrib():
    """03: 도약 시 무릎 관절 일 기여율 막대 3개 + 평균·표준편차 + 수술측–비수술측 p<0.001"""
    S, Y0 = 18, 540  # 1% = 18px, 기준선 y
    bars = [('수술측', 9.7, 3.9, RED, 148), ('비수술측', 13.5, 4.0, BLUE, 444), ('대조군', 11.9, 4.2, GREY, 740)]
    s, tops = [], []
    for name, m, sd, color, cx in bars:
        s.append(rect(cx - 100, Y0 - m * S, 200, m * S, color))
        hi, lo = Y0 - (m + sd) * S, Y0 - (m - sd) * S
        s.append(rect(cx - 2, hi, 4, lo - hi, INK))
        s.append(rect(cx - 24, hi - 2, 48, 4, INK))
        s.append(rect(cx - 24, lo - 2, 48, 4, INK))
        top = hi - 14 - 104
        tops.append(top)
        s.append(at(f'{m}%', cx, top, 220, 'val', f'color:{"#7d858d" if color == GREY else color}'))
        s.append(at(f'±{sd}', cx, top + 60, 220, 'sd'))
        s.append(at(name, cx, Y0 + 18, 260, 'lab'))
    s.append(rect(0, Y0, 888, 3, INK))
    # 유의 표시: 수술측–비수술측만 (수술측–대조군 p=0.03은 보정 기준 p<0.017 미충족 → 표시 안 함)
    yb = tops[1] - 22
    s.append(rect(148, yb, 296, 3, INK))
    s.append(rect(148 - 1.5, yb, 3, tops[0] - 12 - yb, INK))
    s.append(rect(444 - 1.5, yb, 3, tops[1] - 8 - yb, INK))
    s.append(at('p &lt; 0.001', 296, yb - 50, 260, 'lab', 'font-size:36px'))
    return f'<div class="chart" style="height:{Y0 + 18 + 52}px">{"".join(s)}</div>'


def chart_stack():
    """04: 수술측 도약 시 관절별 일 기여율 100% 누적 막대 (고관절 49.7 · 무릎 9.7 · 발목 40.6)"""
    H, TOP, X, BW = 440, 64, 150, 240
    segs = [('고관절', 49.7, HIP, INK, 'item'), ('무릎', 9.7, RED, RED, 'key'), ('발목', 40.6, ANKLE, INK, 'item')]
    s = [at('수술측 다리 · 도약할 때 관절별 몫', 444, 0, 888, 'note-ink', f'color:{MUTED}')]
    y = TOP
    for name, v, fill, color, cls in segs:
        h = H * v / 100
        s.append(rect(X, y, BW, h, fill))
        lh = 73 if cls == 'key' else 62
        # 이름표는 막대 오른쪽에 붙여 둔다(글 상자 폭 auto → 왼쪽 시작점 고정, 정렬 값은 center 유지)
        s.append(f'<p class="a {cls}" style="left:{X + BW + 36}px;top:{y + h / 2 - lh / 2:.1f}px;color:{color}' + (';font-weight:850' if cls == 'key' else '') + f'">{name} {v}%</p>')
        y += h
    return f'<div class="chart" style="height:{TOP + H}px">{"".join(s)}</div>'


CARDS = [
    # 01 표지
    ('kind-cover', [
        '<h1 class="headline">점프 거리가 같으면<br><span class="accent">무릎</span>도 회복된 걸까?</h1>', gap(48),
        slot(680, '사진 넣는 자리', '한국인 성인 선수 · 한 발 멀리뛰기<br>옆에서 전신 · 도약 직후 공중 장면'), gap(48),
        '<p class="sub">ACL 재활에서 놓치기 쉬운 평가</p>']),
    # 02 핵심 결과
    ('kind-lsi', [
        '<h1 class="headline">점프 거리는 <span class="accent">97%</span><br>무릎이 수행한 일은 <span class="warn">69%</span></h1>', gap(24),
        '<p class="note">LSI: 수술한 다리 ÷ 반대쪽 다리 × 100</p>', gap(56),
        chart_lsi(), gap(56),
        '<p class="body">Aspetar 연구진(2022)이 측정한<br><span class="strong">ACL 재건술 후 남성 선수 26명</span>,<br>모두 스포츠 복귀 승인을 받은 상태였습니다.</p>', gap(28),
        '<p class="note">69%는 근력이나 무릎 기능 전체가 아니라<br>도약할 때 무릎이 한 ‘일’의 좌우 비율입니다.</p>']),
    # 03 무릎 기여율 비교
    ('kind-contrib', [
        '<h1 class="headline">비슷한 점프 거리,<br><span class="accent">다른 무릎의 기여</span></h1>', gap(20),
        '<p class="note">도약 시 무릎 관절 일 기여율 (세 관절 합 중 무릎 몫)</p>', gap(28),
        chart_contrib(), gap(28),
        '<p class="body">수술한 무릎은 반대쪽보다 <span class="strong">덜 기여</span>했습니다.</p>', gap(12),
        '<p class="note">막대 = 평균, 세로선 = ±표준편차<br>앞 장의 69%(좌우 비율)와는 다른 지표입니다</p>']),
    # 04 왜 차이가 생겼나
    ('kind-stack', [
        '<h1 class="headline">점프 거리는 <span class="accent">무릎만</span><br>결정하지 않습니다</h1>', gap(16),
        '<p class="sub" style="font-weight:650">고관절과 발목이 큰 역할을 합니다</p>', gap(40),
        chart_stack(), gap(40),
        '<p class="body">무릎 몫이 줄고 고관절 몫이 커지며<br><span class="strong">비슷한 거리</span>를 낼 수 있습니다.</p>', gap(20),
        '<p class="note">이 연구의 한 발 멀리뛰기 도약 구간 결과이며,<br>홉 테스트마다 관절 비율은 다를 수 있습니다.</p>']),
    # 05 Aspetar 가이드라인
    ('kind-guide', [
        '<h1 class="headline">그래서 Aspetar는<br><span class="accent">점프의 역학</span>까지<br>살펴봅니다</h1>', gap(40),
        '<div class="box" style="padding:36px 40px 40px">'
        '<p class="note-ink" style="color:var(--blue);font-weight:700">Aspetar ACL 재활 가이드라인 (2023)</p>' + gap(10)
        + '<p class="item">고관절 · 무릎 · 발목의</p>' + gap(26)
        + '<div class="cols">'
        + '<div class="col"><p class="big">각도</p><p class="note">얼마나<br>굽히고 펴는지</p></div>'
        + '<div class="col"><p class="big">모멘트</p><p class="note">관절을<br>돌리는 힘</p></div>'
        + '<div class="col"><p class="big">일(Work)</p><p class="note">관절이 만들고<br>흡수한 에너지</p></div>'
        + '</div></div>', gap(44),
        '<p class="body">수직·수평 점프에서 절대값과<br><span class="strong">좌우 대칭성</span>을 함께 회복하도록 제안합니다.</p>', gap(32),
        '<p class="note">전문 선수의 복귀 평가를 위한 제안이며,<br>재부상 예방이 검증된 기준은 아닙니다.</p>']),
    # 06 강사 소개
    ('kind-lecture', [
        '<h1 class="headline">이 가이드라인에 참여한<br><span class="accent">ACL 재활 전문가</span>를<br>만납니다</h1>', gap(40),
        '<div class="duo">'
        '<div class="person">' + slot(340, '사진 넣는 자리', '승인받은<br>프로필 사진', 404) + '<p class="name">Andreas Bjerregaard</p></div>'
        '<p class="times">×</p>'
        '<div class="person">' + slot(340, '사진 넣는 자리', '승인받은<br>프로필 사진', 404) + '<p class="name">조인혁</p></div>'
        '</div>', gap(28),
        '<p class="note-ink">Andreas · 2023 Aspetar ACL 재활 임상진료지침 공동저자</p>',
        '<p class="note">전 Aspetar ACL Rehabilitation Team 물리치료사</p>', gap(40),
        '<p class="sub accent" style="font-size:40px">R스포츠 아카데미</p>', gap(4),
        '<p class="key">ACL 재활 전문가 초청 강의</p>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>ACL 홉 거리 {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
