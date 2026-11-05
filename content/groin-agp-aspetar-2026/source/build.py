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


CARDS = [
    # 01 표지
    ('kind-cover', [
        '<h1 class="headline">오래된 서혜부 통증,<br>‘어디’보다 <span class="accent">‘왜’</span>를<br>찾습니다</h1>', gap(44),
        photo('cover-match-sprint_PattayaPatrol_ccbysa40.jpg', 540, 1705, -664, -225, '야간 경기에서 공을 몰고 달리는 선수와 따라붙는 수비수'), gap(44),
        '<p class="body">아스페타 2026 ‘운동선수 서혜부 통증<br>재활 경로’를 정리했습니다</p>']),
    # 02 시간표 없음
    ('kind-timeline', [
        '<h1 class="headline">치유 <span class="accent">시간표</span>가<br>없는 통증입니다</h1>', gap(52),
        '<p class="body">뚜렷한 부상 순간 없이 생길 때가 많고<br>예측 가능한 치유 일정을 따르지 않습니다.<br>급성 부상이 덜 회복된 채 복귀한 뒤<br>생기기도 합니다.</p>', gap(64),
        '<p class="key">그래서 시작 단계도<br><span class="accent">사람마다</span> 다릅니다</p>', gap(20),
        '<p class="sub">평가에 따라 Foundation부터, 또는 그 뒤<br>단계부터 시작하고 기준을 넘어야 진행합니다</p>', gap(64),
        '<div class="box"><p class="safety">레드 플래그를 배제하고 보존 치료가 맞다고<br>확인한 뒤 적용하는 경로입니다</p></div>']),
    # 03 3기둥
    ('kind-pillars', [
        '<h1 class="headline">아픈 곳보다<br><span class="accent">과부하의 이유</span></h1>', gap(36),
        '<p class="body">진단이 겹치고, 통증 위치·양상·영상으로<br>구조를 가려내기 어렵기 때문입니다</p>', gap(48),
        '<div class="list" style="gap:30px">'
        + pair('조직 능력', '지금 견딜 수 있는 부하 · 자극 민감도')
        + pair('생체역학', '부하가 몸에 어떻게 나뉘고 조절되는지')
        + pair('훈련 부하', '얼마나 했고, 어떻게 바뀌었고, 얼마나 회복했는지') + '</div>', gap(48),
        '<div class="box"><p class="body"><span class="strong">쉬면 나은 것처럼 보입니다.</span><br>부하를 뺀 덕분일 뿐, 원인은<br>다음 종목 부하에서 다시 드러납니다</p></div>']),
    # 04 매일 검사
    ('kind-daily', [
        '<h1 class="headline">매일 재는 것은<br><span class="accent">두 가지</span></h1>', gap(64),
        '<div class="box" style="padding:52px 40px;gap:18px"><p class="item">내전근 압박 검사</p><p class="sub">고관절 굴곡 0° · 45° · 90°<br>(0°는 코펜하겐 변형 포함)</p>'
        '<p class="body">통증·힘이 전날보다 나빠지면<br>부하가 과했거나 원인이 남았다는 신호</p></div>', gap(48),
        '<div class="box" style="padding:52px 40px;gap:18px"><p class="item">고관절 내회전, 두 자세로</p><p class="sub">누운 자세 · 엎드린 자세</p>'
        '<p class="body">자세마다 다르면 연부조직·신경근 제한,<br>둘 다 줄면 관절 제한 가능성</p></div>']),
    # 05 관문
    ('kind-gates', [
        '<h1 class="headline">다음 단계로 가는<br><span class="accent">관문</span></h1>', gap(24),
        '<p class="sub">주 2회 검사로 판단합니다</p>', gap(28),
        '<div class="box"><p class="label">직선 달리기 전</p><p class="item">변형 토마스 자세에서<br>crossover 통증 없음</p></div>', gap(24),
        '<div class="box"><p class="label">방향 전환 · 킥 전</p>'
        '<p class="body">같은 쪽 저항 고관절 굴곡 통증 없음</p>'
        '<p class="body">긴 지렛대 crossbody 검사 통증 없음</p>'
        '<p class="body">바깥 범위 스트레칭·저항 반응 개선</p>'
        '<p class="body"><span class="strong">내전근 힘 좌우 비율(LSI) 80% 이상</span></p></div>', gap(24),
        '<p class="note">crossbody 검사는 복부 관여가 크면<br>가장 늦게 정상화되는 경우가 많습니다</p>']),
    # 06 운동 조절
    ('kind-control', [
        '<h1 class="headline">처음에는 근력보다<br><span class="accent">운동 조절</span></h1>', gap(52),
        '<p class="body">급성 부상과 달리, 초기 단계는<br>운동 조절 비중이 큽니다</p>', gap(72),
        '<div class="list" style="gap:44px">'
        + pair('아픈 곳만 반복해서 부하 주지 않기', '과부하 원인을 그대로 두면<br>능력보다 증상이 이어질 수 있습니다')
        + pair('자극 민감도가 높으면', '직접 내전근 부하는<br>처음에 비중을 낮출 수 있습니다')
        + pair('검사가 정상화되고 부하를 견디면', '근력 · 달리기 · 폭발력 · 종목 동작으로<br>무게를 옮깁니다') + '</div>']),
    # 07 3층 평가
    ('kind-layers', [
        '<h1 class="headline">같은 결손을<br><span class="accent">세 층</span>에서 봅니다</h1>', gap(48),
        '<div class="list" style="gap:36px">'
        + step('단독 검사', '고관절 외전·외회전 조절', '요추골반 위치, 고관절-골반-흉곽 분리')
        + step('복합 동작', '한발 스쿼트에서 골반 떨어짐')
        + step('역동적 과제', '달리기 중 골반 떨어짐', '컷에서는 흉곽 위치 변화로') + '</div>', gap(48),
        '<div class="box"><p class="body">층마다 결과가 다르면<br><span class="strong accent">종목 요구가 가장 높은 과제</span>의<br>소견을 가장 무겁게 봅니다</p></div>']),
    # 08 복귀 후
    ('kind-resilience', [
        '<h1 class="headline">복귀한 뒤에도<br><span class="accent">재활은 이어집니다</span></h1>', gap(28),
        '<p class="sub">Resilience 단계 · NBA 현장 관점 사례</p>', gap(48),
        '<div class="list" style="gap:40px">'
        + pair('경기 부하의 70~80%로 시작', '단계마다 낮춘 목표로 시작해<br>강도·접촉이 갑자기 늘어나는 것에 대비', 'key')
        + pair('힘든 운동은 힘든 훈련 날에', '고부하 운동일과 고부하 종목일을 맞춰<br>회복일을 지킵니다', 'key')
        + pair('48~72시간 뒤 반응까지', '힘든 세션 뒤 늦게 나타나는 증상을 확인', 'key') + '</div>', gap(48),
        '<p class="body">워밍업과 훈련 뒤 ‘톱오프’ 운동으로<br>재활 목표를 유지합니다</p>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>서혜부 통증 AGP {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
