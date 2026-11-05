"""러닝 자세 개인화 카드 HTML 생성: source/01.html ~ 12.html (tools/cardkit의 qa.js·layers.js 포함).
근거: Gindre 2026 Sports Med 56:2121 (CC BY 4.0) 한 편. 글은 h1/p, 굵기 500·650·700·750·800·850만,
사진은 overflow:hidden 크롭 안의 img, 선은 border-top div(→ PPTX 선 도형). 인라인 SVG 없음.
사용: python3 content/running-form-pimp/source/build.py"""
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
.num{{font-size:144px;font-weight:850;line-height:1.08;letter-spacing:-.04em;color:var(--blue)}}
.accent{{color:var(--blue)}} .warn{{color:var(--red)}}
.photo{{position:relative;overflow:hidden;width:888px;flex:none}}
.photo img{{position:absolute;display:block}}
.row{{display:flex;justify-content:center;gap:24px;width:888px}}
.col{{display:flex;flex-direction:column;align-items:center;gap:14px}}
.map{{position:relative;width:888px;flex:none}}
.slot{{background:var(--tint);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;flex:none;padding:0 20px}}
.slot .stag{{font-size:36px;font-weight:700;color:var(--blue);line-height:1.3}}
.slot .guide{{font-size:36px;font-weight:500;color:var(--muted);line-height:1.42}}
.map .tag{{position:absolute;width:290px;display:flex;flex-direction:column;gap:2px}}
.map .tag.l{{left:0;align-items:center}} .map .tag.r{{right:0;align-items:center}}
.map .t{{font-size:40px;font-weight:800;line-height:1.25;letter-spacing:-.03em;color:var(--blue)}}
.map .d{{font-size:36px;font-weight:500;line-height:1.35;letter-spacing:-.02em;color:var(--ink)}}
.map .ln{{position:absolute;height:0;border-top:3px solid #9fb3c4}}
.map .dot{{position:absolute;width:16px;height:16px;border-radius:8px;background:var(--blue)}}
"""
FRAME = ('<svg class="card-frame" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">'
         '<rect x="35" y="35" width="1010" height="1280" rx="28" fill="none" stroke="#D0DCE5" stroke-width="2"/></svg>')


def photo(src, h, iw, ix, iy, alt, w=888, radius=0, folder='photos'):
    """보이는 창 w×h, 이미지 폭 iw, 창 기준 위치(ix, iy) → 크롭"""
    r = f';border-radius:{radius}px' if radius else ''
    return (f'<div class="photo" style="width:{w}px;height:{h}px{r}"><img src="../assets/{folder}/{src}" alt="{alt}" '
            f'style="width:{iw}px;left:{ix}px;top:{iy}px"></div>')


def gap(px):
    return f'<div style="height:{px}px;flex:none"></div>'


def tag(side, top, t, d):
    return f'<div class="tag {side}" style="top:{top}px"><p class="t">{t}</p><p class="d">{d}</p></div>'


def line(x, y, w):
    return f'<div class="ln" style="left:{x}px;top:{y}px;width:{w}px"></div>'


def dot(x, y):
    return f'<div class="dot" style="left:{x - 8}px;top:{y - 8}px"></div>'


P = {}  # 사진 설정: build_photos.json 대신 여기서 관리 (파일, 창 높이, 이미지 폭, 위치)
exec((HERE / 'photos.py').read_text(encoding='utf-8'), P)


def slot(h, guide, w=888, radius=20):
    return (f'<div class="slot" style="width:{w}px;height:{h}px;border-radius:{radius}px">'
            f'<p class="stag">사진 넣는 자리</p><p class="guide">{guide}</p></div>')


def ph(key, **kw):
    v = P['PHOTOS'].get(key)
    if v is None:
        h, guide = P['SLOTS'][key]
        return slot(h, guide, w=kw.get('w', 888), radius=kw.get('radius') or 20)
    f, h, iw, ix, iy, alt = v
    return photo(f, h, iw, ix, iy, alt, **kw)


def ability_map():
    """11 능력 지도: 가운데 러너 사진 + 좌우 라벨, 가로선으로 몸 부위와 연결"""
    H = P['MAP_H']
    pw = P['MAP_W']                      # 가운데 사진 창 폭
    px = (888 - pw) // 2                 # 사진 창 왼쪽
    if P['MAP_PHOTO']:
        f, iw, ix, iy, alt = P['MAP_PHOTO']
        parts = [f'<div class="photo" style="position:absolute;left:{px}px;top:0;width:{pw}px;height:{H}px;border-radius:24px">'
                 f'<img src="../assets/photos/{f}" alt="{alt}" style="width:{iw}px;left:{ix}px;top:{iy}px"></div>']
    else:
        # 자리 안내 글은 라벨 선 사이 빈 칸(선 92·202·312 사이)에 한 줄씩 둔다
        parts = [f'<div class="slot" style="position:absolute;left:{px}px;top:0;width:{pw}px;height:{H}px;border-radius:24px"></div>',
                 f'<p class="stag" style="position:absolute;left:{px}px;width:{pw}px;top:{P["MAP_SLOT_TOP"][0]}px;font-size:36px;font-weight:700;color:var(--blue);line-height:1.3">사진 넣는 자리</p>',
                 f'<p class="guide" style="position:absolute;left:{px}px;width:{pw}px;top:{P["MAP_SLOT_TOP"][1]}px;font-size:36px;font-weight:500;color:var(--muted);line-height:1.3">전신 옆모습</p>']
    for side, ty, t, d, bx, by in P['MAP_TAGS']:
        parts.append(tag(side, ty, t, d))
        # 선: 라벨 안쪽 끝 → 몸 부위 점(bx, by: 지도 좌표)
        if side == 'l':
            parts.append(line(290, by, bx - 290))
        else:
            parts.append(line(bx, by, 598 - bx))
        parts.append(dot(bx, by))
    return f'<div class="map" style="height:{H}px">{"".join(parts)}</div>'


CARDS = [
    # 01 표지
    ('kind-cover', [
        '<h1 class="headline">날지 못하는 새에게<br><span class="accent">날라고</span> 하지 마세요</h1>', gap(48),
        ph('cover'), gap(48),
        '<p class="body">네, 러닝 자세 얘기 맞습니다</p>']),
    # 02 밈: 타조
    ('kind-meme', [
        '<h1 class="headline">억지 자세 교정 =<br>타조에게 <span class="accent">비행 연습</span></h1>', gap(48),
        ph('ostrich', radius=0), gap(48),
        '<p class="body">타조는 날기를 포기한 게 아닙니다.<br><span class="strong">달리기를 고른 겁니다.</span></p>']),
    # 03 엘리트 복사
    ('kind-elite', [
        '<h1 class="headline">1등 자세를 따라 하면<br><span class="accent">1등</span>이 될까요?</h1>', gap(48),
        ph('elite'), gap(48),
        '<p class="body">1등 자세는 그 몸이 만든 결과지,<br><span class="strong">빨라지는 비법이 아닙니다</span></p>']),
    # 04 뒤꿈치 85%
    ('kind-number', [
        '<h1 class="headline">뒤꿈치 착지가 오답이면,<br>대회장은 <span class="accent">오답 노트</span></h1>', gap(40),
        ph('heel'), gap(28),
        '<p class="num">85%+</p>', gap(12),
        '<p class="body">10km 넘는 대회 아마추어 러너는<br>대부분 <span class="strong">뒤꿈치로</span> 딛습니다</p>']),
    # 05 근거 수준
    ('kind-evidence', [
        '<h1 class="headline">‘좋은 자세’,<br><span class="accent">근거</span> 있나요?</h1>', gap(48),
        ph('styles'), gap(20),
        '<p class="note">같은 길, 신발도 자세도 제각각</p>', gap(44),
        '<p class="body">모두에게 통하는 자세는<br><span class="strong">아직 확인되지 않았습니다</span></p>']),
    # 06 자기최적화
    ('kind-self', [
        '<h1 class="headline">당신 몸,<br><span class="accent">계산 잘합니다</span></h1>', gap(48),
        ph('group'), gap(44),
        '<p class="body">에너지 덜 드는 보폭을<br>계산기 없이 찾아갑니다</p>', gap(14),
        '<p class="note">훈련된 장거리 러너 연구들</p>']),
    # 07 그래프
    ('kind-chart', [
        '<h1 class="headline">느려질수록<br>땅과 <span class="accent">정이 듭니다</span></h1>', gap(72),
        '<div class="photo" style="height:680px"><img src="../assets/charts/speed-contact.png" alt="속도별 접지 시간 그래프: 빠를수록 짧고 느릴수록 길다" style="width:888px;left:0;top:0"></div>', gap(52),
        '<p class="note">땅에 닿는 시간 · 남성 아마추어 러너 추정치</p>']),
    # 08 Fig.1
    ('kind-figure', [
        '<h1 class="headline">빠를 땐 <span class="accent">스프링</span>,<br>느릴 땐 바퀴</h1>', gap(52),
        photo('fig1-000.jpg', 401, 888, 0, 0, '탄성 위주 러닝과 근육 위주 러닝의 동작 궤적 (Gindre 2026 Fig.1)', folder='figures'), gap(32),
        '<div class="row" style="gap:0">'
        '<div class="col" style="width:444px;gap:4px"><p class="item accent">띠용띠용 스프링</p><p class="note" style="color:var(--ink)">짧게 딛고<br>위아래로 크게</p></div>'
        '<div class="col" style="width:444px;gap:4px"><p class="item">데굴데굴 바퀴</p><p class="note" style="color:var(--ink)">오래 딛고<br>낮게, 관절은 크게</p></div></div>', gap(52),
        '<p class="key">속도가 붙으면 대체로<br>띠용 쪽으로 옮겨 갑니다</p>']),
    # 09 억지로 바꾸면
    ('kind-warn', [
        '<h1 class="headline">자세는 업데이트,<br>몸은 <span class="accent">아직 구버전</span></h1>', gap(48),
        ph('tired'), gap(44),
        '<p class="body">너무 빨리, 너무 크게 바꾸면<br><span class="strong warn">비효율과 부상 위험</span>이 커질 수 있습니다</p>']),
    # 10 이유: 근력·탄성·조절
    ('kind-why', [
        '<h1 class="headline">그 자세,<br>다 <span class="accent">사정</span>이 있습니다</h1>', gap(48),
        '<div class="row">'
        + ''.join(f'<div class="col">{ph(k, w=280, radius=20)}<p class="item">{t}</p></div>'
                  for k, t in (('strength', '근력'), ('elastic', '탄성'), ('control', '조절'))) + '</div>', gap(48),
        '<p class="body">내 몸 스펙이<br><span class="strong">자세를 만듭니다</span></p>']),
    # 11 능력 지도
    ('kind-map', [
        '<h1 class="headline">자세 검사 말고,<br><span class="accent">몸 스펙</span> 검사</h1>', gap(48),
        None, gap(40),   # ability_map()으로 채움
        '<p class="body">내 몸 사용설명서는<br><span class="strong">평가로 씁니다</span></p>']),
    # 12 결론·콜백
    ('kind-summary', [
        '<h1 class="headline">날개를 다는 대신<br><span class="accent">다리를 키웁니다</span></h1>', gap(48),
        ph('train'), gap(48),
        '<p class="key">타조처럼.<br>자세 교정보다, 능력 평가부터</p>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    parts = [ability_map() if p is None else p for p in parts]
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>러닝 자세 {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
