"""PFP 2탄 카드 HTML 생성: source/01.html ~ 09.html (tools/cardkit의 qa.js·layers.js 포함).
글은 h1/p, 굵기 500·650·700·750·800·850만, 사진은 overflow:hidden 크롭 안의 img.
사용: python3 content/pfp-runners-part2/source/build.py"""
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
.photo{{position:relative;overflow:hidden;width:888px}}
.photo img{{position:absolute;display:block}}
.chart{{width:888px;height:560px;display:block}}
.slot{{width:888px;border-radius:20px;background:var(--tint);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px}}
.slot .tag{{font-size:36px;font-weight:700;color:var(--blue);line-height:1.3}}
.slot .guide{{font-size:36px;font-weight:500;color:var(--muted);line-height:1.42}}
.list{{display:flex;flex-direction:column;align-items:center;gap:30px}}
.pair{{display:flex;flex-direction:column;align-items:center;gap:6px}}
.box{{background:var(--tint);border-radius:20px;padding:30px 40px;width:888px}}
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


WHY_CARD =     ('kind-why', [
        '<h1 class="headline">무릎 앞 통증,<br><span class="accent">왜</span> 생길까요?</h1>', gap(44),
        '<div class="box"><p class="key">무릎뼈 관절 압박<br>= 누르는 힘 ÷ 닿는 면적</p></div>', gap(48),
        '<div class="list" style="gap:32px">'
        + pair('누르는 힘이 커질 때', '무릎을 굽힌 채 버티는 부하가<br>갑자기 늘 때')
        + pair('닿는 면적이 작아질 때', '무릎뼈 정렬, 허벅지가 안으로<br>모이는 움직임 등') + '</div>', gap(44),
        '<p class="body">견딜 수 있는 수준을 넘는 압박이 반복되면<br>주변 조직이 예민해져 아플 수 있습니다.</p>', gap(16),
        '<p class="note">어느 조직이 아픈지는 아직 정확히 모릅니다</p>'])

CARDS = [
    # 01 표지
    ('kind-cover', [
        '<h1 class="headline">스쿼트 vs<br>레그 익스텐션,<br><span class="accent">무릎</span>에 덜 부담인 건?</h1>', gap(44),
        photo('cover-trx-squat_PTPioneer_ccby20.jpg', 520, 888, 0, -52, 'TRX 끈을 잡고 스쿼트하는 여성 옆모습'), gap(44),
        '<p class="body">정답은 운동 이름이 아니라<br><span class="strong">‘무릎 각도’</span>에 있습니다</p>']),
    # 02 비교 설계
    ('kind-setup', [
        '<h1 class="headline">같은 근육을 써도<br><span class="accent">무릎 압박</span>은 다릅니다</h1>', gap(36),
        '<p class="body">1탄에서 근거가 확인된 위험 요인은<br>허벅지 앞(무릎 폄) 근력 약화였죠.</p>', gap(52),
        '<div class="list">' + pair('스쿼트', '발이 바닥에 고정 · CKC')
        + pair('발목 중량 무릎 펴기', '의자에 앉아 발목에 중량 · OKC')
        + pair('고정 저항 기계 무릎 펴기', '연구용 동력계 · OKC') + '</div>', gap(52),
        '<p class="body">건강한 성인 10명이 세 운동을<br>같은 근육 활성도로 맞추고<br>0~90°에서 무릎뼈 압박을 비교했습니다.</p>']),
    # 03 그래프
    ('kind-chart', [
        '<h1 class="headline">각도에 따라<br>압박이 <span class="accent">뒤집힙니다</span></h1>', gap(52),
        '<div class="photo" style="height:560px"><img class="chart" src="../assets/charts/chart-all.png" alt="무릎 각도별 무릎뼈 관절 압박 그래프" style="left:0;top:0"></div>', gap(56),
        '<p class="body">깊게 굽힐수록 스쿼트, 펼수록<br>발목 중량 무릎 펴기의 압박이 컸고<br><span class="strong">45°에서는 차이가 없었습니다.</span></p>']),
    # 04 조합 규칙
    ('kind-rule', [
        '<h1 class="headline">얕게는 스쿼트,<br>깊게는 <span class="accent">무릎 펴기</span></h1>', gap(40),
        '<div class="photo" style="height:560px"><img class="chart" src="../assets/charts/chart-combo.png" alt="스쿼트 0~45도와 무릎 펴기 45~90도 조합 그래프" style="left:0;top:0"></div>', gap(40),
        '<p class="body">스쿼트는 0~45°, 무릎 펴기는 90~45°.<br>이 조합에서 압박이<br><span class="strong">약 4 MPa 이하</span>였습니다.</p>', gap(16),
        '<p class="note">4 MPa: 계단을 오르내릴 때 보고된 최대치 수준</p>']),
    # 05 한계
    ('kind-limits', [
        '<h1 class="headline">그대로 처방하기 전에<br><span class="accent">알아둘 것</span></h1>', gap(52),
        '<div class="list" style="gap:36px">'
        + pair('통증 없는 성인 10명', 'PFP가 있으면 접촉 면적이 작아<br>압박이 더 클 수 있습니다')
        + pair('모델로 계산한 추정값', '올라오는 구간만 계산했고<br>직접 잰 값이 아닙니다')
        + pair('고정 저항 기계는 전 구간 4 MPa 이상', '연구용 장비라 헬스장 기계와<br>같다고 볼 수 없습니다') + '</div>', gap(48),
        '<div class="box"><p class="safety">각도는 출발점입니다.<br>운동 중·다음 날 통증 반응으로<br>범위와 무게를 조절하세요.</p></div>']),
    # 06 스쿼트 45°
    ('kind-squat', [
        '<h1 class="headline">스쿼트는<br><span class="accent">무릎 45°</span>까지</h1>', gap(40),
        photo('mini-squat_BaoBaoLeung_ccbysa40.jpg', 560, 940, -34, -36, '무릎을 살짝 굽힌 미니 스쿼트 옆모습'), gap(40),
        '<p class="body">무릎을 깊게 굽히지 않는<br>얕은 범위에서 시작합니다.</p>', gap(20),
        '<p class="note">높은 박스에 엉덩이가 닿을 때까지만.<br>박스 높이는 사람마다 45°에 맞춰 조정</p>']),
    # 07 무릎 펴기 90→45 (사진 자리)
    ('kind-ext', [
        '<h1 class="headline">무릎 펴기는<br><span class="accent">90°→45°</span>까지</h1>', gap(40),
        '<div class="slot" style="height:580px"><p class="tag">사진 넣는 자리</p>'
        '<p class="guide">의자에 앉아 발목에 중량 · 옆모습<br>무릎 90°에서 시작 → 45°에서 멈춤</p></div>', gap(40),
        '<p class="body">발목에 중량을 달고 앉아서<br>무릎 45°에서 멈춥니다.</p>', gap(20),
        '<p class="item">다리를 끝까지 펴지 않습니다</p>']),
    # 08 싱글 레그 데드리프트
    ('kind-sldl', [
        '<h1 class="headline">움직임은<br><span class="accent">한 발</span>로 연습합니다</h1>', gap(40),
        photo('one-leg-deadlift_bepositivelyfit_ccbysa20.jpg', 480, 920, -10, -60, '케틀벨을 든 싱글 레그 데드리프트 옆모습'), gap(36),
        '<p class="item">싱글 레그 데드리프트</p>', gap(12),
        '<p class="body">엉덩이가 먼저 뒤로, 골반은 수평<br>무릎은 둘째 발가락 방향</p>', gap(16),
        '<p class="note">1탄의 몸통 기울어짐·허벅지가 안으로<br>모이는 움직임을 한 발로 조절합니다</p>']),
    # 09 요약
    ('kind-summary', [
        '<h1 class="headline">무릎 앞이 아픈 러너,<br><span class="accent">이렇게 시작</span>합니다</h1>', gap(76),
        '<div class="list" style="gap:52px">'
        + pair('얕게는 <span class="accent">스쿼트</span>', '무릎 0~45° 범위', 'key')
        + pair('깊게는 <span class="accent">무릎 펴기</span>', '발목 중량, 90°에서 45°까지', 'key')
        + pair('조절은 <span class="accent">한 발</span>로', '싱글 레그 데드리프트', 'key') + '</div>', gap(72),
        '<p class="safety warn">통증이 커지거나 다음 날까지 남으면<br>범위·무게를 줄이고 담당 트레이너와<br>조정하세요.</p>']),
]



def write_cards(cards, out):
    for i, (kind, parts) in enumerate(cards, 1):
        html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>PFP 2탄 {i:02d}</title><style>{CSS}</style></head>'
                f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
        (out / f'{i:02d}.html').write_text(html, encoding='utf-8')
    print(f'{len(cards)} cards')


if __name__ == '__main__':
    write_cards(CARDS, HERE)
