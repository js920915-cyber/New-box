"""러닝 자세 바꾸기 전에(담백한 편) 카드 HTML 생성: source/01.html ~ 08.html (tools/cardkit의 qa.js·layers.js 포함).
근거: Gindre 2026 Sports Med 56:2121 (CC BY 4.0) 한 편. 글은 h1/p, 굵기 500·650·700·750·800·850만,
사진은 overflow:hidden 크롭 안의 img, 선은 border-top div(→ PPTX 선 도형). 인라인 SVG 없음.
사용: python3 content/running-form-change/source/build.py"""
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


CSS += """
.list{display:flex;flex-direction:column;align-items:center;gap:52px;width:888px}
.pair{display:flex;flex-direction:column;align-items:center;gap:6px}
.pair .sub{font-size:44px;font-weight:500;line-height:1.42;letter-spacing:-.02em;color:var(--muted)}
.box{background:var(--tint);border-radius:24px;padding:30px 36px;width:888px;display:flex;flex-direction:column;align-items:center;gap:6px}
"""


def pair(head, sub):
    return f'<div class="pair"><p class="key">{head}</p><p class="sub">{sub}</p></div>'


def box(head, sub):
    return f'<div class="box"><p class="key">{head}</p><p class="sub" style="font-size:44px;font-weight:500;line-height:1.42;color:var(--ink)">{sub}</p></div>'


CARDS = [
    # 01 표지
    ('kind-cover', [
        '<h1 class="headline">자세,<br><span class="accent">왜</span> 바꾸고 싶으세요?</h1>', gap(48),
        ph('cover'), gap(48),
        '<p class="body">바꾸기 전에 먼저 확인할 것들</p>']),
    # 02 근거 수준
    ('kind-evidence', [
        '<h1 class="headline">자세를 바꾸면<br><span class="accent">좋아질까요?</span></h1>', gap(48),
        ph('crowd'), gap(44),
        '<p class="body">어떤 자세도 모두에게 기록 향상이나<br><span class="strong">부상 예방 효과가 입증되지 않았습니다</span></p>', gap(16),
        '<p class="note">착지 방식을 바꾸는 효과도 아직 근거가 제한적입니다</p>']),
    # 03 부담 이동
    ('kind-shift', [
        '<h1 class="headline">부담은 줄기보다<br><span class="accent">옮겨갈</span> 수 있습니다</h1>', gap(48),
        ph('heel'), gap(44),
        '<p class="body">한 조직의 스트레스가 줄어도<br><span class="strong">다른 조직의 스트레스는 늘 수 있습니다</span></p>', gap(16),
        '<p class="note">예: 앞꿈치 착지로 바꾸면 발목 쪽 일이 늘어납니다</p>']),
    # 04 목적·개별성·검증
    ('kind-check', [
        '<h1 class="headline">바꾼다면,<br><span class="accent">세 가지</span>를 확인합니다</h1>', gap(100),
        '<div class="list" style="gap:72px">'
        + pair('<span class="accent">목적</span>', '왜 바꾸나요?<br>기록인가요, 통증인가요?')
        + pair('<span class="accent">개별성</span>', '내 몸, 내 속도, 내 목표에<br>맞는 변화인가요?')
        + pair('<span class="accent">검증</span>', '바꾼 뒤 실제로<br>나아졌는지 확인했나요?') + '</div>']),
    # 05 부상 때문이라면: 용량·준비·부하
    ('kind-injury', [
        '<h1 class="headline">부상 때문이라면,<br><span class="accent">몸부터</span> 봅니다</h1>', gap(64),
        '<div class="list" style="gap:28px">'
        + box('용량', '다친 조직이 지금<br>얼마나 견딜 수 있나요?')
        + box('준비', '근력과 조절이<br>바뀐 자세를 받쳐 주나요?')
        + box('부하', '최근 훈련량이<br>갑자기 늘지 않았나요?') + '</div>']),
    # 06 비유
    ('kind-meme', [
        '<h1 class="headline">준비 안 된 몸에<br><span class="accent">자세부터</span> 바꾸라는 건</h1>', gap(48),
        ph('ostrich'), gap(44),
        '<p class="body">날지 못하는 새에게<br><span class="strong">날라고 하는 것과 같습니다</span></p>']),
    # 07 센터 경험
    ('kind-clinic', [
        '<h1 class="headline">자세를 급히 바꾼 러너,<br>생각보다 <span class="accent">많이</span> 찾아옵니다</h1>', gap(48),
        ph('clinic'), gap(44),
        '<p class="body">너무 빨리, 너무 크게 바꾸면<br><span class="strong warn">비효율과 부상 위험</span>이 커질 수 있습니다</p>']),
    # 08 요약
    ('kind-summary', [
        '<h1 class="headline">자세보다 먼저,<br><span class="accent">이유와 몸</span>을 봅니다</h1>', gap(96),
        '<div class="list" style="gap:56px">'
        + pair('왜 바꾸는지', '목적 · 개별성 · 검증')
        + pair('몸이 준비됐는지', '용량 · 준비 · 부하')
        + pair('바꾼 뒤 확인했는지', '느낌 말고 기록과 평가로') + '</div>', gap(96),
        '<p class="body">바꾸고 싶다면,<br><span class="strong">평가부터 시작하세요</span></p>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>러닝 자세 바꾸기 {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
