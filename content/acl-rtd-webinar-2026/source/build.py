"""ACL 근력만으로는 부족한 이유(사전 웨비나 홍보 1편) 카드 HTML 생성: source/01.html ~ 06.html.
tools/cardkit의 qa.js·layers.js 포함. 글은 h1/p, 굵기 500·650·700·750·800·850만, 사진은 overflow:hidden 크롭 안의 img.
03 그래프는 div 막대(배경색 → PPTX 실제 도형) + p 라벨(편집 가능한 글)로 만든다. 수치: Werner 2026 Table 5.
사용: python3 content/acl-rtd-webinar-2026/source/build.py"""
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
.big{{font-size:144px;font-weight:850;line-height:1.08;letter-spacing:-.04em}}
.note{{font-size:36px;font-weight:500;line-height:1.4;color:var(--muted);letter-spacing:-.02em}}
.accent{{color:var(--blue)}}
.photo{{position:relative;overflow:hidden;width:888px;border-radius:0}}
.photo img{{position:absolute;display:block}}
.slot{{width:888px;border-radius:20px;background:var(--tint);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px}}
.slot .tag{{font-size:36px;font-weight:700;color:var(--blue);line-height:1.3}}
.slot .guide{{font-size:36px;font-weight:500;color:var(--muted);line-height:1.42}}
.list{{display:flex;flex-direction:column;align-items:center}}
.box{{background:var(--tint);border-radius:20px;padding:36px 40px;width:888px;display:flex;flex-direction:column;align-items:center}}
.bars{{position:relative;width:888px;display:flex;flex-direction:column;gap:30px;padding-top:58px}}
.bar-row{{display:flex;flex-direction:column;align-items:center;gap:12px}}
.bar-label{{font-size:40px;font-weight:650;line-height:1.3;letter-spacing:-.02em}}
.bar-label .v{{font-weight:850}}
.track{{position:relative;width:888px;height:56px;background:var(--tint);border-radius:10px}}
.fill{{position:absolute;left:0;top:0;height:56px;border-radius:10px}}
.ref{{position:absolute;top:58px;bottom:0;width:3px;background:var(--ink)}}
.ref-label{{position:absolute;top:0;font-size:36px;font-weight:700;line-height:1.3;white-space:nowrap}}
"""
FRAME = ('<svg class="card-frame" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">'
         '<rect x="35" y="35" width="1010" height="1280" rx="28" fill="none" stroke="#D0DCE5" stroke-width="2"/></svg>')
PHOTOS = HERE.parent / 'assets/photos'


def photo(src, h, iw, ix, iy, alt, slot_guide):
    """보이는 창 888×h, 이미지 폭 iw, 창 기준 위치(ix, iy) → 크롭. 파일이 없으면 사진 자리."""
    if not (PHOTOS / src).exists():
        return (f'<div class="slot" style="height:{h}px"><p class="tag">사진 넣는 자리</p>'
                f'<p class="guide">{slot_guide}</p></div>')
    return (f'<div class="photo" style="height:{h}px"><img src="../assets/photos/{src}" alt="{alt}" '
            f'style="width:{iw}px;left:{ix}px;top:{iy}px"></div>')


def gap(px):
    return f'<div style="height:{px}px;flex:none"></div>'


def bar(label, value, color):
    w = round(888 * float(value) / 100)
    return (f'<div class="bar-row"><p class="bar-label">{label} <span class="v" style="color:{color}">{value}%</span></p>'
            f'<div class="track"><div class="fill" style="width:{w}px;background:{color}"></div></div></div>')


REF_X = round(888 * 0.9)
CHART = ('<div class="bars">'
         f'<div class="ref" style="left:{REF_X - 1}px"></div>'
         f'<p class="ref-label" style="left:{REF_X}px;transform:translateX(-50%)">기준 90%</p>'
         + bar('최대 근력', '92.4', '#8a96a3')
         + bar('힘을 올리는 속도 (0.1~0.2초)', '79.1', 'var(--blue)')
         + bar('한발 점프의 무릎 파워', '76.4', 'var(--blue)')
         + '</div>')

CARDS = [
    # 01 표지
    ('kind-cover', [
        '<h1 class="headline">ACL 수술 후,<br>근력만 회복하면<br><span class="accent">충분</span>할까요?</h1>', gap(48),
        photo('cover.jpg', 520, 1421, -222, -416, '공을 몰며 방향을 바꾸는 선수의 다리', '방향을 바꾸거나 착지하는 선수<br>역동적인 장면 · 가로'), gap(48),
        '<p class="body">근력 좌우 차이가 줄었다면,<br>복귀 준비도 끝난 걸까요?</p>']),
    # 02 연구 대상
    ('kind-study', [
        '<h1 class="headline">복귀 테스트를<br>모두 통과한 선수</h1>', gap(44),
        '<p class="big accent" style="font-size:168px">53명</p>', gap(56),
        '<p class="body">근력검사와 한발 홉 테스트에서<br>좌우 대칭 90% 이상,<br>무릎 기능 설문도 90% 이상이었습니다.</p>', gap(72),
        '<p class="key">그런데 실험실 장비로<br>다시 측정하자 차이가 보였습니다</p>', gap(56),
        '<p class="note">방향전환이 많은 종목 선수<br>평균 17세 · 수술 후 평균 10.5개월</p>']),
    # 03 핵심 데이터
    ('kind-chart', [
        '<h1 class="headline">근력은 92.4%,<br>힘을 올리는 속도는<br><span class="accent">79.1%</span></h1>', gap(40),
        CHART, gap(56),
        '<p class="body">근력 회복만으로는 보이지 않는<br>차이가 있었습니다.</p>', gap(24),
        '<p class="note">좌우 대칭성(수술한 다리 ÷ 반대 다리) 집단 평균<br>세 값은 서로 다른 검사의 결과입니다</p>']),
    # 04 핵심 메시지
    ('kind-key', [
        '<h1 class="headline">큰 힘과<br><span class="accent">빠른 힘</span>은 다릅니다</h1>', gap(64),
        '<p class="key">큰 힘 · 최대 근력</p>', gap(8),
        '<p class="body" style="color:var(--muted)">얼마나 큰 힘을 낼 수 있는가</p>', gap(40),
        '<div style="width:888px;border-top:2px solid #d0dce5;flex:none"></div>', gap(40),
        '<p class="key accent">빠른 힘 · 힘을 올리는 속도</p>', gap(8),
        '<p class="body" style="color:var(--muted)">힘을 내기 시작한 뒤 0.1~0.2초 사이<br>얼마나 빨리 힘을 올리는가</p>', gap(64),
        '<p class="body">점프·착지·방향전환처럼 짧은 순간에는<br>힘을 빠르게 내는 능력이 필요합니다.</p>', gap(32),
        '<p class="body strong">연구진은 빠른 힘 발휘를<br>재활 전 과정에서 개선하자고 제안합니다.</p>']),
    # 05 다음 단계 기준
    ('kind-next', [
        '<h1 class="headline">다음 단계는<br>무엇으로 정할까요?</h1>', gap(40),
        photo('next.jpg', 360, 888, 0, -232, '달리기 훈련을 하는 선수들', '달리기·방향전환 훈련 장면 · 가로'), gap(40),
        '<div class="list" style="gap:18px">'
        '<p class="item">근력을 더 키울까?</p>'
        '<p class="item">점프·파워를 시작할까?</p>'
        '<p class="item">달리기·방향전환은 언제?</p></div>', gap(44),
        '<div class="box"><p class="body">수술 후 시간은 필요하지만<br>그것만으로는 충분하지 않습니다.<br>'
        '<span class="strong accent">객관적인 평가 기준</span>이 함께 필요합니다.</p></div>']),
    # 06 사전 웨비나
    ('kind-promo', [
        '<h1 class="headline">ACL 재활,<br>다음 단계를<br><span class="accent">결정하는 기준</span></h1>', gap(36),
        '<p class="body">근력 회복 이후 무엇을 평가하고<br>어떤 기준으로 진행할까요?</p>', gap(48),
        '<div class="box">'
        '<p class="note" style="color:var(--ink);font-weight:650">2027 Criteria Based ACL Rehab Workshop<br>사전 웨비나</p>', gap(18),
        '<p class="key">12.7(월) 오후 9시 · Zoom</p>', gap(18),
        '<p class="body">1차 Andreas Bjerregaard<br>Aspetar ACL 재활 가이드라인 공저자</p>', gap(10),
        '<p class="note">영어 강의 · 통역 제공 · 60분</p></div>', gap(48),
        '<p class="key accent">신청은 프로필 링크에서</p>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>ACL 사전 웨비나 {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
