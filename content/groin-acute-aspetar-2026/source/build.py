"""급성 서혜부 손상 — 아스페타 방식 카드 HTML 생성: source/01.html ~ 08.html (tools/cardkit의 qa.js·layers.js 포함).
글은 h1/p, 굵기 500·650·700·750·800·850만, 사진은 overflow:hidden 크롭 안의 img.
근거: research/claims.md (Power 외 2026, Aspetar Sports Med J 15(TT40):498–505)
사용: python3 content/groin-acute-aspetar-2026/source/build.py"""
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
.item{{font-size:46px;font-weight:800;line-height:1.3;letter-spacing:-.03em}}
.sub{{font-size:38px;font-weight:500;line-height:1.4;color:var(--muted);letter-spacing:-.02em}}
.label{{font-size:36px;font-weight:700;line-height:1.3;color:var(--blue);letter-spacing:-.01em}}
.note{{font-size:36px;font-weight:500;line-height:1.4;color:var(--muted);letter-spacing:-.02em}}
.safety{{font-size:38px;font-weight:700;line-height:1.42;letter-spacing:-.02em}}
.accent{{color:var(--blue)}} .warn{{color:var(--red)}}
.photo{{position:relative;overflow:hidden;width:888px}}
.photo img{{position:absolute;display:block}}
.list{{display:flex;flex-direction:column;align-items:center;gap:30px}}
.pair{{display:flex;flex-direction:column;align-items:center;gap:6px}}
.box{{background:var(--tint);border-radius:20px;padding:40px 40px;width:888px;display:flex;flex-direction:column;align-items:center;gap:10px}}

.chips{{display:flex;flex-wrap:wrap;justify-content:center;gap:16px;max-width:888px}}
.chip{{background:var(--tint);border-radius:999px;padding:16px 36px}}
.chip p{{font-size:40px;font-weight:750;line-height:1.3;letter-spacing:-.02em}}
.chip.white{{background:#fff}}
.chip.blue{{background:var(--blue)}} .chip.blue p{{color:#fff}}
.chip.red p{{color:var(--red)}}
.chip.big p{{font-size:48px;font-weight:800}}
.arrowrow{{display:flex;align-items:center;justify-content:center;gap:20px}}
.arrow{{font-size:52px;font-weight:800;color:var(--muted);line-height:1}}
.tile{{background:var(--tint);border-radius:24px;padding:34px 36px;width:888px;display:flex;align-items:center;gap:28px}}
.num{{width:84px;height:84px;border-radius:42px;background:var(--blue);display:flex;align-items:center;justify-content:center;flex:none}}
.num.gray{{background:var(--muted)}}
.num p{{color:#fff;font-size:44px;font-weight:850;line-height:1}}
.tiletext{{flex:1;font-size:46px;font-weight:800;line-height:1.3;letter-spacing:-.03em}}
.bar{{border-radius:18px;background:var(--tint);height:100px;display:flex;align-items:center;justify-content:center}}
.bar p{{font-size:42px;font-weight:800;line-height:1.2;letter-spacing:-.02em}}
.bar .kr{{font-weight:500;color:var(--muted)}}
.bar.blue{{background:var(--blue)}} .bar.blue p,.bar.blue .kr{{color:#fff}}
.stairs{{display:flex;align-items:flex-end;gap:12px}}
.step{{width:213px;border-radius:18px 18px 0 0;background:var(--tint);display:flex;flex-direction:column;align-items:center;padding-top:26px;gap:4px}}
.step p{{font-size:40px;font-weight:750;line-height:1.3;letter-spacing:-.02em}}
.step .n{{font-size:36px;font-weight:700;color:var(--blue)}}
.step.blue{{background:var(--blue)}} .step.blue p,.step.blue .n{{color:#fff}}
.chain{{display:flex;align-items:center;gap:8px}}
.link{{width:248px;border-radius:20px;background:var(--tint);padding:24px 6px;display:flex;flex-direction:column;align-items:center;gap:6px}}
.link .t{{font-size:40px;font-weight:800;line-height:1.25;letter-spacing:-.02em}}
.link .s{{font-size:36px;font-weight:500;color:var(--muted);line-height:1.3;letter-spacing:-.02em}}
.link.blue{{background:var(--blue)}} .link.blue p{{color:#fff}}
.cols{{display:flex;gap:18px;width:888px}}
.col{{flex:1;background:var(--tint);border-radius:24px;padding:44px 12px;display:flex;flex-direction:column;align-items:center;gap:18px}}
.col .t{{font-size:46px;font-weight:850;line-height:1.2;letter-spacing:-.03em}}
.col .s{{font-size:36px;font-weight:500;color:var(--muted);line-height:1.4;letter-spacing:-.02em}}
.layer{{border-radius:20px;background:var(--tint);padding:24px 20px;display:flex;flex-direction:column;align-items:center;gap:4px}}
.layer .t{{font-size:44px;font-weight:800;line-height:1.25;letter-spacing:-.02em}}
.layer .s{{font-size:36px;font-weight:500;color:var(--muted);line-height:1.3}}
.layer.blue{{background:var(--blue)}} .layer.blue p{{color:#fff}}
.track{{display:flex;gap:12px}}
.stop{{width:138px;display:flex;flex-direction:column;align-items:center;gap:10px}}
.stop .who{{font-size:36px;font-weight:750;color:var(--blue);line-height:1.3}}
.stop .spacer{{height:94px}}
.dot{{width:96px;height:96px;border-radius:48px;background:var(--tint);display:flex;align-items:center;justify-content:center}}
.dot p{{font-size:44px;font-weight:850;color:var(--muted);line-height:1}}
.dot.on{{background:var(--blue)}} .dot.on p{{color:#fff}}
.stat{{background:var(--tint);border-radius:24px;padding:30px 36px;width:888px;display:flex;align-items:center;gap:24px}}
.stat .big{{width:330px;flex:none;font-size:68px;font-weight:850;color:var(--blue);line-height:1.1;letter-spacing:-.03em}}
.stat .txt{{flex:1;font-size:42px;font-weight:700;line-height:1.35;letter-spacing:-.02em}}
"""
FRAME = ('<svg class="card-frame" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">'
         '<rect x="35" y="35" width="1010" height="1280" rx="28" fill="none" stroke="#D0DCE5" stroke-width="2"/></svg>')


def photo(src, h, iw, ix, iy, alt):
    """보이는 창 888×h, 이미지 폭 iw, 창 기준 위치(ix, iy) → 크롭"""
    return (f'<div class="photo" style="height:{h}px"><img src="../assets/photos/{src}" alt="{alt}" '
            f'style="width:{iw}px;left:{ix}px;top:{iy}px"></div>')


def pair(head, sub, cls='item', sub_cls='sub'):
    return f'<div class="pair"><p class="{cls}">{head}</p><p class="{sub_cls}">{sub}</p></div>'


def step(label, head, sub=None):
    s = f'<p class="label">{label}</p><p class="item">{head}</p>'
    if sub:
        s += f'<p class="sub">{sub}</p>'
    return f'<div class="pair">{s}</div>'


def gap(px):
    return f'<div style="height:{px}px;flex:none"></div>'


def chips(items, extra=''):
    return '<div class="chips">' + ''.join(f'<div class="chip {c or extra}"><p>{t}</p></div>' for t, c in items) + '</div>'


def arrowrow(a, b):
    return (f'<div class="arrowrow"><div class="chip big"><p>{a}</p></div><p class="arrow">→</p>'
            f'<div class="chip big blue"><p>{b}</p></div></div>')


def tile(n, text, numcls=''):
    return f'<div class="tile"><div class="num {numcls}"><p>{n}</p></div><p class="tiletext">{text}</p></div>'



CARDS = [
    # 01 표지
    ('kind-cover', [
        '<h1 class="headline">급성 내전근 부상,<br>복귀는 <span class="accent">날짜</span>가 아니라<br>기준으로</h1>', gap(44),
        photo('cover-shot-windup_RickDikeman_ccbysa30.jpg', 560, 888, 0, -180, '슈팅 직전 다리를 뒤로 크게 뺀 축구 선수'), gap(44),
        '<p class="body">아스페타 2026<br>급성 서혜부 손상 재활 경로</p>']),
    # 02 결손 + 원칙
    ('kind-why', [
        '<h1 class="headline">통증이 사라져도<br><span class="accent">결손은 남기 쉽습니다</span></h1>', gap(56),
        chips([('근력', ''), ('가동범위', ''), ('운동 조절', '')], 'big'), gap(18),
        '<p class="note">흔히 통증보다 오래 남는 결손</p>', gap(80),
        '<p class="label">그래서 아스페타의 3원칙</p>', gap(24),
        '<div class="list" style="gap:26px">' + tile(1, '종목 요구에서 거꾸로 설계') + tile(2, '평가로 개인 맞춤')
        + tile(3, '날짜가 아니라 <span class="accent">기준</span>으로') + '</div>']),
    # 03 6단계 막대
    ('kind-phases', [
        '<h1 class="headline">재활은 6단계,<br><span class="accent">복귀 뒤</span>까지</h1>', gap(48),
        '<div class="list" style="gap:18px">'
        + '<div class="bar" style="width:540px"><p>Foundation <span class="kr">회복 기초</span></p></div>'
        + '<div class="bar" style="width:610px"><p>Reload <span class="kr">근력 재건</span></p></div>'
        + '<div class="bar" style="width:740px"><p>Accumulation <span class="kr">달리기↑ · 킥 시작</span></p></div>'
        + '<div class="bar" style="width:790px"><p>Transition <span class="kr">고속·필드</span></p></div>'
        + '<div class="bar" style="width:840px"><p>Simulation <span class="kr">경기 재현</span></p></div>'
        + '<p class="label">▼ 복귀</p>'
        + '<div class="bar blue" style="width:888px"><p>Resilience <span class="kr">복귀 후 관리</span></p></div>' + '</div>', gap(48),
        '<p class="body">기간이 아니라 <span class="strong">기준을 넘어야</span> 다음 단계로</p>']),
    # 04 근력
    ('kind-strength', [
        '<h1 class="headline">근력은<br>이 순서로 <span class="accent">올립니다</span></h1>', gap(44),
        '<p class="label">검사</p>', gap(12), arrowrow('등척성', '원심성'), gap(12),
        '<p class="note">원심성은 늦게 회복 · 마지막까지 좌우 비교</p>', gap(32),
        '<p class="label">근육 길이 · 속도</p>', gap(12), arrowrow('짧게·느리게', '길게·빠르게'), gap(32),
        '<p class="label">함께 올리는 4갈래</p>', gap(12),
        chips([('내전근', ''), ('고관절 굴곡근', ''), ('복합 운동', ''), ('보조근', '')]), gap(32),
        '<div class="box"><p class="key">“어디에서 느껴지나요?”</p><p class="sub">목표 근육에 부하가 가는지 선수에게 확인</p></div>']),
    # 05 달리기 계단
    ('kind-running', [
        '<h1 class="headline">달리기는 <span class="accent">직선</span>에서<br>경기 장면까지</h1>', gap(72),
        '<div class="stairs">'
        + '<div class="step" style="height:290px"><p class="n">1</p><p>드릴<br>조깅</p></div>'
        + '<div class="step" style="height:390px"><p class="n">2</p><p>12 km/h<br>이상 직선</p></div>'
        + '<div class="step" style="height:490px"><p class="n">3</p><p>곡선<br>달리기</p></div>'
        + '<div class="step blue" style="height:590px"><p class="n">4</p><p>경기 최악<br>1·5분<br>100%↑</p></div>'
        + '</div>', gap(56),
        '<p class="body">곡선은 고강도 직선을<br><span class="strong">증상 없이 견딘 뒤</span> 따로 시작</p>']),
    # 06 킥 사슬
    ('kind-kick', [
        '<h1 class="headline">킥은 <span class="accent">각도</span> 먼저,<br>속도는 나중에</h1>', gap(36),
        photo('kick-shot_USMC-KeeganJones_pd.jpg', 440, 888, 0, -140, '골키퍼 앞에서 슈팅하는 축구 선수'), gap(40),
        '<div class="chain">'
        + '<div class="link"><p class="t">케이블 킥</p><p class="s">Accumulation</p></div><p class="arrow">→</p>'
        + '<div class="link"><p class="t">공 킥</p><p class="s">Transition</p></div><p class="arrow">→</p>'
        + '<div class="link blue"><p class="t">최대 강도</p><p class="s">Simulation</p></div>'
        + '</div>', gap(36),
        chips([('크로스바디·발리는 이틀 연속 ×', 'red')]), gap(24),
        '<p class="note">손상 기전이 킥과 닮아 단계적으로 노출합니다</p>']),
    # 07 통증 신호등
    ('kind-pain', [
        '<h1 class="headline">통증은 금지선이 아니라<br><span class="accent">안내선</span>입니다</h1>', gap(28),
        '<p class="sub">운동 중 · 운동 후 · 24시간 반응을 나눠 봅니다</p>', gap(64),
        '<div class="box" style="gap:26px;padding:48px 40px"><p class="key accent">진행</p>'
        + chips([('운동 중 가벼운 통증', 'white'), ('24시간 안에 회복', 'white'), ('동작 유지', 'white')]) + '</div>', gap(40),
        '<div class="box" style="gap:26px;padding:48px 40px"><p class="key warn">일시적으로 부하 조정</p>'
        + chips([('안정 시 통증 ↑', 'white'), ('눌렀을 때 통증 ↑', 'white'), ('움직임 제한 ↑', 'white')]) + '</div>']),
    # 08 요약
    ('kind-summary', [
        '<h1 class="headline">복귀는 한 번의 검사로<br><span class="accent">정하지 않습니다</span></h1>', gap(64),
        '<div class="list" style="gap:26px">' + tile('×', '검사 하나로 결정', 'gray') + tile('×', '근력만 보고 결정', 'gray')
        + tile('✓', '복귀 뒤에도 관리') + '</div>', gap(28),
        '<p class="sub">임상 · 운동 조절 · 필드 · 실험실 결과를 함께</p>', gap(64),
        '<p class="safety">고정 프로토콜이 아닌 판단의 틀입니다.<br>손상 유형마다 경과가 다를 수 있습니다.</p>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>급성 서혜부 {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
