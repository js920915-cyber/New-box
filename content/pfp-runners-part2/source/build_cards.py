"""PFP 2탄 카드 HTML 생성. 그래프는 Powers et al. 2014 Table 수치로 직접 그린다(원 그림 복제 아님).
사용: python3 source/build_cards.py  → source/cards.html, source/video-*.html
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
INK, BLUE, GRAY, MUTED, LINE = "#121416", "#0879d8", "#7d8794", "#5e6570", "#d0dce5"

# Powers CM et al. JOSPT 2014;44(5):320-327, Table: PFJ stress (MPa, mean) at 0,15,...,90°
ANGLES = [0, 15, 30, 45, 60, 75, 90]
DATA = {
    "squat": [0.3, 0.9, 1.9, 3.9, 6.7, 10.5, 12.3],
    "ext_cr": [7.9, 5.6, 5.1, 5.0, 5.2, 6.0, 6.5],
    "ext_vr": [8.4, 5.6, 4.7, 4.2, 3.6, 2.6, 0.5],
}

# ---------- chart ----------
W, H = 888, 640
PL, PR, PT, PB = 92, 650, 70, 552   # plot box
YMAX = 14


def sx(a):
    return PL + (PR - PL) * a / 90


def sy(v):
    return PB - (PB - PT) * v / YMAX


def poly(vals, a0=0, a1=90):
    pts = [(sx(a), sy(v)) for a, v in zip(ANGLES, vals) if a0 <= a <= a1]
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def axes(title_right=False):
    g = []
    for v in (0, 4, 8, 12):
        y = sy(v)
        g.append(f'<line x1="{PL}" y1="{y:.1f}" x2="{PR}" y2="{y:.1f}" stroke="#e8edf1" stroke-width="2"/>')
        g.append(f'<text x="{PL-16}" y="{y+11:.1f}" text-anchor="end" font-size="32" fill="{MUTED}">{v}</text>')
    for a in ANGLES:
        g.append(f'<text x="{sx(a):.1f}" y="{PB+44}" text-anchor="middle" font-size="32" fill="{MUTED}">{a}°</text>')
    g.append(f'<line x1="{PL}" y1="{PB}" x2="{PR}" y2="{PB}" stroke="#9aa6b2" stroke-width="2"/>')
    if title_right:
        g.append(f'<text x="{PR+22}" y="{PT+30}" font-size="30" font-weight="600" fill="{MUTED}">관절 압박</text>')
        g.append(f'<text x="{PR+22}" y="{PT+68}" font-size="30" font-weight="600" fill="{MUTED}">(MPa)</text>')
    else:
        g.append(f'<text x="{PL-60}" y="{PT-30}" font-size="32" font-weight="600" fill="{MUTED}">관절 압박 (MPa)</text>')
    g.append(f'<text x="{(PL+PR)/2:.1f}" y="{PB+86}" text-anchor="middle" font-size="32" font-weight="600" fill="{MUTED}">무릎 굽힘 각도 →</text>')
    return "\n".join(g)


def ref4(label=True):
    y = sy(4)
    s = f'<line x1="{PL}" y1="{y:.1f}" x2="{PR}" y2="{y:.1f}" stroke="{INK}" stroke-width="2" stroke-dasharray="4 8" opacity=".55"/>'
    if label:
        s += f'<text x="{PR+22}" y="{y-4:.1f}" font-size="32" font-weight="600" fill="{MUTED}">4 MPa</text>'
        s += f'<text x="{PR+22}" y="{y+34:.1f}" font-size="28" fill="{MUTED}">계단 걷기 수준</text>'
    return s


def dots(vals, color, r=7, a0=0, a1=90):
    return "".join(f'<circle cx="{sx(a):.1f}" cy="{sy(v):.1f}" r="{r}" fill="{color}" stroke="#fff" stroke-width="3"/>'
                   for a, v in zip(ANGLES, vals) if a0 <= a <= a1)


def label(y, text, color, dash=False):
    d = ' stroke-dasharray="10 7"' if dash else ""
    return (f'<line x1="{PR+22}" y1="{y:.1f}" x2="{PR+58}" y2="{y:.1f}" stroke="{color}" stroke-width="6" stroke-linecap="round"{d}/>'
            f'<text x="{PR+70}" y="{y+11:.1f}" font-size="34" font-weight="700" fill="{INK}">{text}</text>')


def chart_compare():
    s = [f'<svg class="chart" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Noto Sans KR" '
         f'role="img" aria-label="무릎 굽힘 각도별 슬개대퇴관절 압박: 스쿼트는 굽힐수록 증가, 발목 중량 무릎 펴기는 펼수록 증가, 고정 저항은 전 구간 5~8 MPa">',
         axes(), ref4(False),
         f'<polyline points="{poly(DATA["ext_cr"])}" fill="none" stroke="{GRAY}" stroke-width="5" stroke-dasharray="12 9" stroke-linejoin="round"/>',
         f'<polyline points="{poly(DATA["ext_vr"])}" fill="none" stroke="{BLUE}" stroke-width="6" stroke-linejoin="round"/>',
         f'<polyline points="{poly(DATA["squat"])}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>',
         dots(DATA["ext_cr"], GRAY), dots(DATA["ext_vr"], BLUE), dots(DATA["squat"], INK),
         label(sy(12.3), "스쿼트", INK),
         label(sy(6.5), "고정 저항", GRAY, True),
         label(sy(0.9), "발목 중량", BLUE),
         f'<text x="{PR+22}" y="{sy(4)-4:.1f}" font-size="30" font-weight="600" fill="{MUTED}">┄ 4 MPa</text>',
         "</svg>"]
    return "\n".join(s)


def chart_path():
    global PT
    PT = 150
    try:
        return _chart_path()
    finally:
        PT = 70


def _chart_path():
    zx = sx(45)
    s = [f'<svg class="chart" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Noto Sans KR" '
         f'role="img" aria-label="0~45도 스쿼트와 45~90도 발목 중량 무릎 펴기를 이으면 전 구간 약 4 MPa 이하">',
         f'<rect x="{PL}" y="{PT}" width="{zx-PL:.1f}" height="{PB-PT}" fill="#f0f7fc"/>',
         f'<rect x="{zx:.1f}" y="{PT}" width="{PR-zx:.1f}" height="{PB-PT}" fill="#f7f9fb"/>',
         axes(True), ref4(),
         f'<line x1="{zx:.1f}" y1="{PT}" x2="{zx:.1f}" y2="{PB}" stroke="#9aa6b2" stroke-width="2"/>',
         f'<polyline points="{poly(DATA["ext_cr"])}" fill="none" stroke="#c4ccd4" stroke-width="4" stroke-dasharray="12 9"/>',
         f'<polyline points="{poly(DATA["ext_vr"], 0, 45)}" fill="none" stroke="#c4ccd4" stroke-width="4"/>',
         f'<polyline points="{poly(DATA["squat"], 45, 90)}" fill="none" stroke="#c4ccd4" stroke-width="4"/>',
         f'<polyline points="{poly(DATA["squat"], 0, 45)}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>',
         f'<polyline points="{poly(DATA["ext_vr"], 45, 90)}" fill="none" stroke="{BLUE}" stroke-width="7" stroke-linejoin="round"/>',
         dots(DATA["squat"], INK, 8, 0, 45), dots(DATA["ext_vr"], BLUE, 8, 45, 90),
         f'<text x="{(PL+zx)/2:.1f}" y="{PT-96}" text-anchor="middle" font-size="40" font-weight="800" fill="{INK}">CKC</text>',
         f'<text x="{(PL+zx)/2:.1f}" y="{PT-56}" text-anchor="middle" font-size="30" font-weight="600" fill="{MUTED}">스쿼트</text>',
         f'<text x="{(zx+PR)/2:.1f}" y="{PT-96}" text-anchor="middle" font-size="40" font-weight="800" fill="{BLUE}">OKC</text>',
         f'<text x="{(zx+PR)/2:.1f}" y="{PT-56}" text-anchor="middle" font-size="30" font-weight="600" fill="{MUTED}">발목 중량 무릎 펴기</text>',
         "</svg>"]
    return "\n".join(s)


# ---------- pictograms (자체 제작) ----------
def g(inner, sw):
    return f'<g fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round" stroke-width="{sw}">{inner}</g>'


def picto_squat(x=0, y=0, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            + g('<polyline points="150,252 236,268 204,378"/><line x1="200" y1="382" x2="256" y2="384"/>', 38)
            + g('<line x1="190" y1="118" x2="150" y2="246"/>', 58)
            + g('<polyline points="196,132 262,160 316,156"/>', 28)
            + f'<circle cx="214" cy="70" r="36" fill="{INK}"/></g>')


def picto_seated(x=0, y=0, s=1.0, machine=False):
    leg = '<polyline points="104,246 214,246 304,318"/>'
    extra = ""
    if machine:
        extra = (f'<line x1="214" y1="246" x2="300" y2="300" stroke="{GRAY}" stroke-width="12" stroke-linecap="round"/>'
                 f'<rect x="282" y="300" width="44" height="34" rx="10" fill="{GRAY}" transform="rotate(38 304 317)"/>'
                 f'<circle cx="214" cy="246" r="12" fill="{GRAY}"/>')
    else:
        extra = f'<rect x="286" y="318" width="40" height="34" rx="8" fill="{GRAY}" transform="rotate(38 306 335)"/>'
    chair = (f'<g stroke="#9aa6b2" stroke-width="12" stroke-linecap="round">'
             f'<line x1="70" y1="276" x2="210" y2="276"/><line x1="86" y1="276" x2="86" y2="380"/>'
             f'<line x1="194" y1="276" x2="194" y2="380"/><line x1="70" y1="276" x2="70" y2="140"/></g>')
    return (f'<g transform="translate({x},{y}) scale({s})">' + chair
            + g(leg, 38) + extra
            + g('<line x1="118" y1="112" x2="106" y2="240"/>', 58)
            + g('<polyline points="122,128 154,190 196,236"/>', 26)
            + f'<circle cx="128" cy="62" r="36" fill="{INK}"/></g>')


def picto_sldl(x=0, y=0, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            + g('<polyline points="300,206 316,292 304,382"/><line x1="300" y1="386" x2="360" y2="388"/>', 38)
            + g('<polyline points="296,200 190,214 90,226"/><line x1="86" y1="226" x2="80" y2="262"/>', 36)
            + g('<line x1="300" y1="200" x2="452" y2="176"/>', 58)
            + g('<polyline points="436,186 446,250 450,300"/>', 26)
            + f'<rect x="420" y="296" width="62" height="30" rx="10" fill="{GRAY}"/>'
            + f'<circle cx="514" cy="164" r="36" fill="{INK}"/></g>')


PART1_FIG = """
  <g fill="none" stroke="#121416" stroke-linecap="round" stroke-linejoin="round">
   <polyline points="330,226 352,292 332,328" stroke-width="30"/>
   <line x1="222" y1="106" x2="198" y2="208" stroke-width="24"/>
   <line x1="302" y1="98" x2="340" y2="196" stroke-width="24"/>
   <polygon points="222,106 302,98 322,220 266,212" fill="#121416" stroke-width="26"/>
   <polyline points="262,214 300,292 262,364" stroke-width="32"/>
   <line x1="238" y1="368" x2="292" y2="370" stroke-width="18"/>
  </g>
  <line x1="262" y1="220" x2="262" y2="374" stroke="#8f9baa" stroke-width="4" stroke-dasharray="11 9"/>
  <circle cx="254" cy="52" r="31" fill="#121416"/>
  <g fill="none" stroke="#0879d8" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
   <path d="M186 70 Q154 96 160 138"/><polyline points="147,124 160,140 173,124"/>
   <path d="M200 296 Q232 278 266 290"/><polyline points="252,276 268,290 250,302"/>
  </g>
 """

FRAME = ('<svg class="card-frame" width="1080" height="1350" viewBox="0 0 1080 1350"><rect x="34" y="34" width="1012" '
         'height="1282" rx="28" fill="none" stroke="#d0dce5" stroke-width="2"/></svg>')

CSS = """
@font-face{font-family:'Noto Sans KR';src:url('../assets/NotoSansKR-VF.ttf') format('truetype');font-weight:100 900}
:root{--cw:1080px;--ch:1350px;--gutter:96px;--h-cover:88px;--h-inside:84px;--key:56px;--body:44px;--note:36px;
 --ink:#121416;--muted:#5e6570;--blue:#0879d8;--red:#cc414a;--tint:#f0f7fc}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#e9edf1}
body{display:flex;flex-direction:column;align-items:center;gap:40px;padding:40px 0}
.card{position:relative;width:var(--cw);height:var(--ch);padding:104px var(--gutter) 98px;overflow:hidden;background:#fff;
 font-family:'Noto Sans KR',sans-serif;color:var(--ink);text-align:center;display:flex;flex-direction:column;align-items:center}
.card-frame{position:absolute;inset:0;pointer-events:none}
.headline{margin:0;font-size:var(--h-inside);font-weight:850;line-height:1.2;letter-spacing:-.035em}
.cover .headline{font-size:var(--h-cover);line-height:1.18}
.body{margin:0;font-size:var(--body);font-weight:500;line-height:1.42;letter-spacing:-.02em}
.key{margin:0;font-size:var(--key);font-weight:800;line-height:1.3;letter-spacing:-.03em}
.note{margin:0;font-size:var(--note);font-weight:500;line-height:1.42;color:var(--muted);letter-spacing:-.02em}
.safety{margin:0;font-size:var(--note);font-weight:650;line-height:1.42;letter-spacing:-.02em}
.accent{color:var(--blue)}
.item-h{margin:0;font-size:48px;font-weight:800;line-height:1.3;letter-spacing:-.03em}
.panel{width:888px;border-radius:24px;background:var(--tint);position:relative}
"""


MODE = "preview"   # preview: 안내 문구 있는 자리 / clean: 빈 자리(배경·오버레이용)
SLOTS = []


def card(i, cls, inner):
    return f'<article class="card {cls}" id="c{i:02d}">\n{inner}\n{FRAME}\n</article>'


def slot(card_no, n, x, y, w, h, kind, what, spec):
    """사용자 사진/영상 자리. 좌표는 카드 기준 절대값(오버레이와 정확히 일치시키기 위해)."""
    SLOTS.append(dict(card=f"{card_no:02d}", id=f"{card_no:02d}-{n}", kind=kind, x=x, y=y, width=w, height=h,
                      ratio=spec.split(" · ")[0], content=what))
    style = f"left:{x}px;top:{y}px;width:{w}px;height:{h}px"
    if MODE == "clean":
        return f'<div class="slot" data-slot="{card_no:02d}-{n}" style="{style}"></div>'
    tag = "영상" if kind == "video" else "사진"
    return (f'<div class="slot guide" data-slot="{card_no:02d}-{n}" style="{style}">'
            f'<span class="g-tag">{tag} 넣는 자리</span><strong>{what}</strong><span class="g-spec">{spec}</span></div>')


def cards():
    SLOTS.clear()
    out = []
    # 01 표지 — 사진
    out.append(card(1, "cover c01 media", f"""
 <h1 class="headline">스쿼트 vs 레그 익스텐션,<br><span class="accent">무릎</span>에 덜 부담인 건?</h1>
 {slot(1, 1, 96, 348, 888, 560, "photo", "표지: 운동하는 러너", "가로 888×560 · 표정·무릎이 보이게")}
 <p class="abs lead" style="top:954px">정답은 운동 이름이 아니라<br>‘무릎 각도’에 있습니다</p>
 <p class="abs note" style="top:1112px">PFP 2탄 · 1탄 ‘러너의 무릎 앞 통증’ 이어서</p>
"""))
    # 02 연구 설정 (연구 장비 설명이라 픽토그램 유지)
    cols = [("스쿼트", "CKC · 발이 바닥에", picto_squat(-40, 0, 0.72)),
            ("무릎 펴기", "OKC · 발목 중량", picto_seated(10, 0, 0.72)),
            ("무릎 펴기", "OKC · 고정 저항", picto_seated(10, 0, 0.72, True))]
    colhtml = "".join(f"""<div class="col"><svg width="276" height="330" viewBox="0 0 276 290">{p}</svg>
   <h3 class="item-h" style="font-size:44px">{h}</h3><p class="note" style="color:var(--ink);font-weight:600">{t}</p></div>""" for h, t, p in cols)
    out.append(card(2, "c02", f"""
 <h2 class="headline">1탄 결론,<br><span class="accent">허벅지 앞 근육</span> 키우기</h2>
 <p class="body" style="margin-top:44px">발생 위험 요인으로 확인된 예외가<br>무릎 폄 근력이었죠. 어떻게 키울까요?</p>
 <div class="cols" style="margin-top:64px;width:100%;display:grid;grid-template-columns:repeat(3,1fr);gap:12px">{colhtml}</div>
 <p class="body" style="margin-top:64px;font-weight:650">세 운동을 같은 근육 활성도로 맞추고<br>0~90° 각도별 무릎뼈 압박을 비교했습니다.</p>
"""))
    # 03 그래프
    out.append(card(3, "c03", f"""
 <h2 class="headline">각도에 따라<br>압박이 <span class="accent">뒤집힙니다</span></h2>
 <div style="margin-top:40px">{chart_compare()}</div>
 <p class="body" style="margin-top:30px">깊게 굽힐수록 스쿼트가, 펼수록<br>발목 중량 무릎 펴기가 압박이 컸고</p>
 <p class="key" style="font-size:48px;margin-top:14px">45°에서는 차이가 없었습니다.</p>
"""))
    # 04 그래프 규칙
    out.append(card(4, "c04", f"""
 <h2 class="headline">0~45°는 CKC,<br>45~90°는 <span class="accent">OKC</span></h2>
 <div style="margin-top:40px">{chart_path()}</div>
 <p class="body" style="margin-top:30px">얕은 스쿼트 + 굽힌 구간의 무릎 펴기,<br>이 조합에서 압박이 약 4 MPa 아래였습니다.</p>
 <p class="note" style="margin-top:16px">4 MPa: 계단을 오르내릴 때 보고된 최대치 수준</p>
"""))
    # 05 주의
    out.append(card(5, "c05", """
 <h2 class="headline">그대로 처방하기 전에<br><span class="accent">알아둘 것</span></h2>
 <div class="bands" style="margin-top:30px;width:100%">
  <div class="band"><h3 class="item-h">고정 저항 기계</h3><p class="body">전 구간 4 MPa 이상이라<br>연구진도 주의를 권했습니다.</p></div>
  <div class="band"><h3 class="item-h">건강한 성인 10명</h3><p class="body">PFP 환자는 접촉 면적이 작아<br>압박이 더 클 수 있습니다.</p></div>
  <div class="band"><h3 class="item-h">모델 추정값</h3><p class="body">올라오는 구간만 계산했고<br>실제 측정값이 아닙니다.</p></div>
 </div>
 <div class="callout"><p class="body" style="font-weight:650">각도는 출발점입니다.<br>운동 중·다음 날 통증 반응으로 조절하세요.</p></div>
"""))
    # 06 스쿼트 — 영상 T01
    out.append(card(6, "c06 media", f"""
 <h2 class="headline">스쿼트는<br><span class="accent">무릎 45°</span>까지</h2>
 {slot(6, 1, 108, 340, 864, 486, "video", "스쿼트 옆모습", "가로 16:9 · 무릎·발끝까지")}
 <p class="abs vq" style="top:862px">무릎이 45°보다<br>더 굽혀지지 않나요?</p>
 <div class="abs vnotes" style="top:1040px">
  <div><h3 class="item-h">깊이</h3><p class="body">높은 박스로 제한</p></div>
  <div><h3 class="item-h">통증</h3><p class="body">운동 중·다음 날 확인</p></div>
 </div>
"""))
    # 07 무릎 펴기 — 사진 2컷
    out.append(card(7, "c07 media", f"""
 <h2 class="headline">무릎 펴기는<br><span class="accent">90°→45°</span>까지</h2>
 {slot(7, 1, 96, 340, 432, 432, "photo", "시작 자세", "1:1 · 옆모습")}
 {slot(7, 2, 552, 340, 432, 432, "photo", "멈춘 자세", "1:1 · 옆모습")}
 <div class="abs pair" style="top:796px"><h3 class="item-h">시작 · 90°</h3><h3 class="item-h">멈춤 · 45°</h3></div>
 <p class="abs key" style="top:892px;font-size:52px">다리를 끝까지<br>펴지 않습니다</p>
 <p class="abs body" style="top:1058px">발목에 중량을 달고 앉아서<br>무릎 45°에서 멈춥니다.</p>
"""))
    # 08 왜 싱글 레그 데드리프트
    out.append(card(8, "c08", f"""
 <h2 class="headline">움직임 패턴은<br><span class="accent">엉덩관절</span>에서</h2>
 <p class="body" style="margin-top:34px">1탄에서 본 몸통 기울어짐과<br>허벅지가 안으로 모이는 움직임,</p>
 <div class="panel" style="margin-top:36px;height:330px">
  <svg width="888" height="330" viewBox="0 0 888 330" aria-label="1탄 움직임 도식에서 싱글 레그 데드리프트로 연결">
   <g transform="translate(-20,0) scale(.86)">{PART1_FIG}</g>
   <g fill="none" stroke="{BLUE}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"><line x1="372" y1="170" x2="440" y2="170"/><polyline points="420,148 444,170 420,192"/></g>
   {picto_sldl(468, 6, 0.74)}
  </svg>
 </div>
 <p class="key" style="margin-top:36px;font-size:52px">싱글 레그 데드리프트로<br>한 발 조절을 연습합니다</p>
 <p class="body" style="margin-top:22px">엉덩이 근육을 크게 쓰는 동작으로 보고되고,<br>엉덩관절+무릎 운동 병행이 권장됩니다.</p>
"""))
    # 09 SLDL 옆 — 영상 T04
    out.append(card(9, "c09 media", f"""
 <h2 class="headline">싱글 레그 데드리프트,<br><span class="accent">옆에서</span> 보기</h2>
 {slot(9, 1, 108, 340, 864, 486, "video", "싱글 레그 데드리프트 옆모습", "가로 16:9 · 머리부터 발끝까지")}
 <p class="abs vq" style="top:862px">엉덩이가 먼저<br>뒤로 가나요?</p>
 <div class="abs vnotes" style="top:1040px">
  <div><h3 class="item-h">등</h3><p class="body">머리~뒷다리 일직선</p></div>
  <div><h3 class="item-h">지지 무릎</h3><p class="body">살짝 굽힌 채 유지</p></div>
 </div>
"""))
    # 10 SLDL 앞 — 영상 T02
    out.append(card(10, "c10 media", f"""
 <h2 class="headline">싱글 레그 데드리프트,<br><span class="accent">앞에서</span> 보기</h2>
 {slot(10, 1, 96, 340, 432, 768, "video", "싱글 레그 데드리프트 정면", "세로 9:16 · 무릎·골반")}
 <div class="abs side" style="top:372px">
  <div><h3 class="item-h">무릎</h3><p class="body">둘째 발가락 방향,<br>안으로 모이지 않게</p></div>
  <div><h3 class="item-h">골반</h3><p class="body">양쪽 높이를<br>수평으로 유지</p></div>
  <div><h3 class="item-h">몸통</h3><p class="body">지지 다리 쪽으로<br>기울지 않게</p></div>
 </div>
 <p class="abs key side-q" style="top:1050px">1탄의 움직임,<br>보이나요?</p>
"""))
    # 11 요약
    out.append(card(11, "c11", """
 <h2 class="headline">무릎 앞이 아픈 러너,<br><span class="accent">이렇게 시작</span>합니다</h2>
 <div class="range"><div class="bar"><div style="background:var(--ink)">CKC 스쿼트</div><div style="background:var(--blue)">OKC 발목 중량</div></div>
  <div class="ticks"><span>0°</span><span>45°</span><span>90°</span></div></div>
 <div class="msgs">
  <div class="msg"><h3 class="item-h">얕게는 CKC</h3><p class="body">스쿼트는 무릎 0~45° 범위에서</p></div>
  <div class="msg"><h3 class="item-h">깊게는 OKC</h3><p class="body">발목 중량 무릎 펴기는 90~45°에서</p></div>
  <div class="msg"><h3 class="item-h">조절은 한 발로</h3><p class="body">싱글 레그 데드리프트, 옆·앞에서 확인</p></div>
 </div>
 <p class="safety" style="margin-top:52px">통증이 운동 중 커지거나 다음 날까지 남으면<br>범위와 무게를 줄이고 담당 트레이너와 조정하세요.</p>
"""))
    return out


EXTRA_CSS = """
.c02 .col{display:flex;flex-direction:column;align-items:center}
.c02 .col .note{margin-top:6px;font-size:34px}
.c05 .band{padding:17px 0}
.c05 .band + .band{border-top:2px solid #e6ecf1}
.c05 .band .body{margin-top:8px;font-size:42px;line-height:1.38}
.c05 .callout{margin-top:30px;width:100%;background:var(--tint);border-radius:24px;padding:30px}
.c05 .callout .body{font-size:42px}
.c11 .msgs{margin-top:60px;width:100%;display:flex;flex-direction:column;gap:42px}
.c11 .range{margin-top:56px;width:100%}
.c11 .bar{display:flex;height:84px;border-radius:20px;overflow:hidden;gap:4px}
.c11 .bar div{flex:1;display:flex;align-items:center;justify-content:center;color:#fff;font-size:40px;font-weight:800;letter-spacing:-.02em}
.c11 .ticks{display:flex;justify-content:space-between;margin-top:12px;font-size:34px;font-weight:600;color:var(--muted)}
.c11 .msg .body{margin-top:8px}
.media .slot{position:absolute;overflow:hidden;background:#f3f5f7}
.media .guide{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:24px;
 border:3px dashed #b9c4cf;text-align:center}
.media .guide .g-tag{font-size:32px;font-weight:700;color:var(--blue)}
.media .guide strong{font-size:40px;font-weight:800;line-height:1.3;letter-spacing:-.02em}
.media .guide .g-spec{font-size:32px;font-weight:500;color:var(--muted);line-height:1.35}
.media .abs{position:absolute;left:96px;right:96px;margin:0}
.media .lead{font-size:48px;font-weight:700;line-height:1.4;letter-spacing:-.03em}
.media .vq{font-size:58px;font-weight:850;line-height:1.24;letter-spacing:-.035em}
.media .vnotes{display:grid;grid-template-columns:1fr 1fr;gap:40px}
.media .vnotes .item-h{font-size:44px}
.media .vnotes .body{margin-top:4px;font-size:40px;line-height:1.36}
.c07 .pair{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.c07 .pair .item-h{font-size:44px}
.c10 .side{left:552px;right:96px;display:flex;flex-direction:column;gap:44px}
.c10 .side .body{margin-top:4px;font-size:40px;line-height:1.36}
.c10 .side-q{left:552px;font-size:48px}
"""


def page(body, title):
    return (f'<!doctype html>\n<html lang="ko"><head><meta charset="utf-8"><title>{title}</title>'
            f'<style>{CSS}{EXTRA_CSS}</style></head><body>\n{body}\n</body></html>\n')


if __name__ == "__main__":
    import json
    title = "PFP 2탄 — 각도별 OKC·CKC와 싱글 레그 데드리프트"
    MODE = "preview"
    open(os.path.join(HERE, "cards.html"), "w", encoding="utf-8").write(page("\n".join(cards()), title))
    MODE = "clean"
    open(os.path.join(HERE, "cards-clean.html"), "w", encoding="utf-8").write(page("\n".join(cards()), title + " (빈 자리)"))
    json.dump(SLOTS, open(os.path.join(HERE, "slots.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ok", len(SLOTS), "slots")
