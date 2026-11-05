"""운동선수 서혜부 통증(AGP) — 아스페타 방식 카드 HTML 생성: source/01.html ~ 08.html (tools/cardkit의 qa.js·layers.js 포함).
글은 h1/p, 굵기 500·650·700·750·800·850만, 사진은 overflow:hidden 크롭 안의 img.
근거: research/claims.md (Palladino 외 2026, Aspetar Sports Med J 15(TT40):506–513)
사용: python3 content/groin-agp-aspetar-2026/source/build.py"""
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
.col{{flex:1;background:var(--tint);border-radius:24px;padding:44px 12px;height:440px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px}}
.col .t{{font-size:46px;font-weight:850;line-height:1.2;letter-spacing:-.03em}}
.col .s{{font-size:36px;font-weight:500;color:var(--muted);line-height:1.4;letter-spacing:-.02em}}
.layer{{border-radius:20px;background:var(--tint);padding:34px 20px;display:flex;flex-direction:column;align-items:center;gap:4px}}
.layer .t{{font-size:44px;font-weight:800;line-height:1.25;letter-spacing:-.02em}}
.layer .s{{font-size:36px;font-weight:500;color:var(--muted);line-height:1.3}}
.layer.blue{{background:var(--blue)}} .layer.blue p{{color:#fff}}
.track{{display:flex;gap:12px}}
.stop{{width:138px;display:flex;flex-direction:column;align-items:center;gap:10px}}
.stop .who{{font-size:36px;font-weight:750;color:var(--blue);line-height:1.3}}
.stop .spacer{{height:47px}}
.dot{{width:96px;height:96px;border-radius:48px;background:var(--tint);display:flex;align-items:center;justify-content:center}}
.dot p{{font-size:44px;font-weight:850;color:var(--muted);line-height:1}}
.dot.on{{background:var(--blue)}} .dot.on p{{color:#fff}}
.stat{{background:var(--tint);border-radius:24px;padding:42px 36px;width:888px;display:flex;align-items:center;gap:24px}}
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
        '<h1 class="headline">오래된 서혜부 통증,<br>‘어디’보다 <span class="accent">‘왜’</span>를<br>찾습니다</h1>', gap(44),
        photo('cover-match-sprint_PattayaPatrol_ccbysa40.jpg', 540, 1705, -664, -225, '야간 경기에서 공을 몰고 달리는 선수와 따라붙는 수비수'), gap(44),
        '<p class="body">아스페타 2026<br>운동선수 서혜부 통증 재활 경로</p>']),
    # 02 시간표 없음 → 시작점 개인별
    ('kind-timeline', [
        '<h1 class="headline">치유 <span class="accent">시간표</span>가<br>없는 통증입니다</h1>', gap(44),
        chips([('뚜렷한 부상 순간 없음', ''), ('예측되는 치유 일정 없음', '')]), gap(72),
        '<p class="key">그래서 시작 단계도 <span class="accent">사람마다</span></p>', gap(28),
        '<div class="track">'
        + '<div class="stop"><p class="who">선수 A</p><div class="dot on"><p>1</p></div></div>'
        + '<div class="stop"><div class="spacer"></div><div class="dot"><p>2</p></div></div>'
        + '<div class="stop"><p class="who">선수 B</p><div class="dot on"><p>3</p></div></div>'
        + '<div class="stop"><div class="spacer"></div><div class="dot"><p>4</p></div></div>'
        + '<div class="stop"><div class="spacer"></div><div class="dot"><p>5</p></div></div>'
        + '<div class="stop"><div class="spacer"></div><div class="dot"><p>6</p></div></div>'
        + '</div>', gap(20),
        '<p class="note">예시 · 평가로 시작점을 정하고, 기준을 넘어야 진행</p>', gap(56),
        '<div class="box"><p class="safety">레드 플래그를 배제하고<br>보존 치료가 맞을 때 적용합니다</p></div>']),
    # 03 3기둥
    ('kind-pillars', [
        '<h1 class="headline">아픈 곳보다<br><span class="accent">과부하의 이유</span></h1>', gap(72),
        '<div class="cols">'
        + '<div class="col"><p class="t">조직 능력</p><p class="s">지금 견딜 수<br>있는 부하</p></div>'
        + '<div class="col"><p class="t">생체역학</p><p class="s">부하가 나뉘고<br>조절되는 방식</p></div>'
        + '<div class="col"><p class="t">훈련 부하</p><p class="s">양·변화·회복</p></div>'
        + '</div>', gap(72),
        '<div class="box" style="padding:48px 40px"><p class="body"><span class="strong">쉬면 나아 보여도</span><br>원인은 다음 종목 부하에서<br>다시 드러납니다</p></div>']),
    # 04 매일 검사
    ('kind-daily', [
        '<h1 class="headline">매일 재는 것<br><span class="accent">두 가지</span></h1>', gap(64),
        '<div class="box" style="gap:26px;padding:56px 40px"><p class="key">내전근 압박 검사</p>'
        + chips([('0°', 'white'), ('45°', 'white'), ('90°', 'white')], 'big')
        + '<p class="sub">고관절 굴곡 각도 · 0°는 코펜하겐 변형 포함</p></div>', gap(48),
        '<div class="box" style="gap:26px;padding:56px 40px"><p class="key">고관절 내회전</p>'
        + chips([('누운 자세', 'white'), ('엎드린 자세', 'white')], 'big')
        + '<p class="body">한 자세만 ↓ <span class="strong">연부조직·신경근</span><br>둘 다 ↓ <span class="strong">관절</span> 가능성</p></div>']),
    # 05 관문
    ('kind-gates', [
        '<h1 class="headline">다음 단계로 가는<br><span class="accent">관문</span></h1>', gap(24),
        '<p class="sub">주 2회 검사로 판단</p>', gap(36),
        '<div class="box" style="gap:18px">' + chips([('관문 1 · 직선 달리기 전', 'blue')])
        + '<p class="item">변형 토마스 자세<br>crossover 통증 없음</p></div>', gap(28),
        '<div class="box" style="gap:10px">' + chips([('관문 2 · 방향 전환 · 킥 전', 'blue')]) + gap(6)
        + '<p class="body">✓ 같은 쪽 저항 고관절 굴곡 통증 없음</p>'
        + '<p class="body">✓ 긴 지렛대 crossbody 검사 통증 없음</p>'
        + '<p class="body">✓ 바깥 범위 스트레칭·저항 반응 개선</p>'
        + '<p class="body"><span class="strong">✓ 내전근 힘 좌우 비율(LSI) ≥80%</span></p></div>']),
    # 06 운동 조절 먼저
    ('kind-control', [
        '<h1 class="headline">처음에는 근력보다<br><span class="accent">운동 조절</span></h1>', gap(52),
        '<div class="box" style="gap:18px;padding:40px 40px"><p class="label">초기</p>'
        + chips([('운동 조절', 'blue')], 'big') + '<p class="sub">아픈 곳만 반복해서 부하 주기 ×</p></div>', gap(16),
        '<p class="arrow">↓</p>', gap(8),
        '<p class="sub">통증 유발 검사 정상화 + 부하를 견디면</p>', gap(24),
        '<div class="box" style="gap:18px;padding:40px 40px"><p class="label">다음</p>'
        + chips([('근력', 'white'), ('달리기', 'white'), ('폭발력', 'white'), ('종목 동작', 'white')]) + '</div>', gap(36),
        '<p class="note">자극 민감도가 높으면<br>직접 내전근 부하는 처음에 낮출 수 있음</p>']),
    # 07 세 층
    ('kind-layers', [
        '<h1 class="headline">같은 결손을<br><span class="accent">세 층</span>에서 봅니다</h1>', gap(64),
        '<div class="list" style="gap:22px">'
        + '<div class="layer" style="width:600px"><p class="t">단독 검사</p><p class="s">고관절 조절 · 골반·흉곽 분리</p></div>'
        + '<div class="layer" style="width:744px"><p class="t">복합 동작</p><p class="s">한발 스쿼트 골반 떨어짐</p></div>'
        + '<div class="layer blue" style="width:888px"><p class="t">역동적 과제</p><p class="s">달리기 골반 떨어짐 · 컷 흉곽 변화</p></div>'
        + '</div>', gap(72),
        '<p class="key">결과가 다르면<br><span class="accent">종목 요구가 가장 높은</span> 층 우선</p>']),
    # 08 복귀 뒤 수치
    ('kind-resilience', [
        '<h1 class="headline">복귀한 뒤에도<br><span class="accent">재활은 이어집니다</span></h1>', gap(24),
        '<p class="sub">Resilience 단계 · NBA 현장 관점 사례</p>', gap(44),
        '<div class="list" style="gap:22px">'
        + '<div class="stat"><p class="big">70–80%</p><p class="txt">경기 부하의 이 수준으로<br>각 단계 시작</p></div>'
        + '<div class="stat"><p class="big">같은 날</p><p class="txt">고부하 운동일 =<br>고부하 훈련일</p></div>'
        + '<div class="stat"><p class="big">48–72h</p><p class="txt">늦게 나오는<br>반응까지 확인</p></div>'
        + '</div>', gap(40),
        '<p class="body">워밍업 · 훈련 뒤 ‘톱오프’ 운동으로 유지</p>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>서혜부 통증 AGP {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
