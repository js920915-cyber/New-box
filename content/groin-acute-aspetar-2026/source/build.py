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
        '<h1 class="headline">급성 내전근 부상,<br>복귀는 <span class="accent">날짜</span>가 아니라<br>기준으로</h1>', gap(44),
        photo('cover-shot-windup_RickDikeman_ccbysa30.jpg', 560, 888, 0, -180, '슈팅 직전 다리를 뒤로 크게 뺀 축구 선수'), gap(44),
        '<p class="body">아스페타가 2026년에 공개한<br>급성 서혜부 손상 재활 경로를 정리했습니다</p>']),
    # 02 왜 + 원칙
    ('kind-why', [
        '<h1 class="headline">통증이 사라져도<br><span class="accent">결손은 남기 쉽습니다</span></h1>', gap(48),
        '<p class="body">근력·가동범위·운동 조절 결손은<br>흔히 통증보다 오래 남습니다.<br>기간 기준 진행은 재발을<br>일관되게 줄이지 못했습니다.</p>', gap(56),
        '<p class="label">아스페타 경로의 3가지 원칙</p>', gap(28),
        '<div class="list" style="gap:44px">'
        + pair('끝에서 거꾸로 설계', '종목 요구를 단계별 목표로 나눕니다')
        + pair('평가로 개인 맞춤', '검사 결과가 운동 선택과 진행을 정합니다')
        + pair('기간이 아니라 <span class="accent">기준</span>', '임상·필드·실험실 측정을 넘어야 진행') + '</div>']),
    # 03 6단계
    ('kind-phases', [
        '<h1 class="headline">재활은 6단계,<br><span class="accent">복귀 뒤</span>까지 갑니다</h1>', gap(40),
        '<div class="list" style="gap:16px">'
        + pair('Foundation · 기초', '조직 관리 · 일상 동작 · 운동 조절 기초')
        + pair('Reload · 재부하', '범위 전체 근력 · 좌우 대칭 · 달리기 드릴')
        + pair('Accumulation · 누적', '달리기 양·강도 · 케이블 킥 · 방향 전환 시작')
        + pair('Transition · 전환', '고속 달리기 · 고강도 드릴 · 필드로 연결')
        + pair('Simulation · 실전 재현', '최악 시나리오 · 최대 강도 킥 · 반응형 방향 전환')
        + pair('<span class="accent">Resilience · 복귀 후</span>', '남은 수행 목표 · 재발 위험 줄이기') + '</div>', gap(36),
        '<p class="body">기간이 아니라 <span class="strong">기준을 넘어야</span> 다음 단계로</p>']),
    # 04 근력
    ('kind-strength', [
        '<h1 class="headline">근력은 <span class="accent">재는 순서</span>도<br>정해져 있습니다</h1>', gap(44),
        '<div class="list" style="gap:32px">'
        + pair('등척성 → 원심성', '안쪽·바깥쪽 범위 모두 잽니다. 원심성은 늦게<br>회복돼 등척성이 정상이어도 좌우 차이가 보입니다')
        + pair('짧은 길이 → 긴 길이·빠른 속도', '부상 기전에 가까운 조건까지<br>단계적으로 부하를 올립니다')
        + pair('“어디에서 느껴지나요?”', '선수가 짚는 부위로 목표 조직에<br>부하가 가는지 확인합니다') + '</div>', gap(44),
        '<div class="box"><p class="body">내전근만이 아니라<br><span class="strong">고관절 굴곡근 · 복합 운동 · 보조근</span>까지<br>네 갈래로 함께 올립니다</p></div>']),
    # 05 달리기
    ('kind-running', [
        '<h1 class="headline">달리기는 <span class="accent">직선</span>에서<br>경기 장면까지</h1>', gap(48),
        '<div class="list" style="gap:30px">'
        + step('Reload', '달리기 드릴 · 느린 조깅')
        + step('Accumulation', '‘진짜 달리기’ 시작', '최대 속도 40% 초과 또는 12 km/h')
        + step('Transition', '곡선 달리기는 따로', '안쪽 다리 부하가 커서, 고강도 직선을<br>증상 없이 견딘 뒤 시작')
        + step('Simulation', '경기 최악 1분·5분을 100% 이상', '본인 경기 데이터 기준') + '</div>', gap(48),
        '<p class="body">달리기 <span class="strong">동작과 노출량</span>은 함께 올립니다</p>']),
    # 06 킥
    ('kind-kick', [
        '<h1 class="headline">킥은 <span class="accent">각도</span> 먼저,<br>속도는 나중에</h1>', gap(36),
        photo('kick-shot_USMC-KeeganJones_pd.jpg', 420, 888, 0, -150, '골키퍼 앞에서 슈팅하는 축구 선수'), gap(36),
        '<p class="body">손상 기전이 킥 동작과 닮았기 때문입니다</p>', gap(6),
        '<p class="note">고관절 신전·외전·외회전 + 빠른 근육 신장</p>', gap(32),
        '<div class="list" style="gap:24px">'
        + pair('Accumulation에 케이블 킥부터', '앞 · 45° · 인사이드 · 크로스바디 · 발리')
        + '<p class="item">크로스바디·발리는 이틀 연속 하지 않기</p>'
        + '<p class="item">최대 강도 킥은 <span class="accent">Simulation</span>에서</p>' + '</div>']),
    # 07 통증 규칙
    ('kind-pain', [
        '<h1 class="headline">통증은 금지선이 아니라<br><span class="accent">안내선</span>입니다</h1>', gap(48),
        '<p class="body">운동 중 · 운동 후 · 24시간 반응을<br>나눠서 봅니다</p>', gap(64),
        '<div class="box"><p class="item accent">진행</p><p class="body">단계에 맞는 운동 중 가벼운 통증이<br>24시간 안에 가라앉고<br>동작이 무너지지 않으면</p></div>', gap(40),
        '<div class="box"><p class="item warn">일시적으로 부하 조정</p><p class="body">안정 시 통증, 눌렀을 때 통증,<br>움직임 제한이 늘어나면</p></div>']),
    # 08 요약
    ('kind-summary', [
        '<h1 class="headline">복귀는 한 번의 검사로<br><span class="accent">정하지 않습니다</span></h1>', gap(56),
        '<div class="list" style="gap:44px">'
        + pair('검사 하나로 정하지 않기', '임상 · 실험실 · 운동 조절 · 필드 결과를<br>함께 봅니다', 'key')
        + pair('근력만 보지 않기', '근력 회복이 운동 조절·생체역학 결손을<br>가릴 수 있습니다', 'key')
        + pair('복귀 뒤에도 <span class="accent">Resilience</span>', '근력 유지가 목표면<br>필드 훈련 직후에 배치합니다', 'key') + '</div>', gap(52),
        '<p class="safety">고정된 프로토콜이 아니라 판단의 틀입니다.<br>손상 유형마다 경과가 다를 수 있습니다.</p>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>급성 서혜부 {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
