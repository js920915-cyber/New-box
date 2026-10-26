"""ACL 홉 거리 vs 무릎 일 카드 HTML 생성: source/01.html ~ 06.html (tools/cardkit의 qa.js·layers.js 포함).
글은 h1/p, 굵기 500·650·700·750·800·850만. 2026-10-26 사용자 지시: 글보다 논문 그림 위주(02 논문 제목, 03 Figure 3, 04 Figure 2,
05 가이드라인 Box 5 원문, 06 가이드라인 저자부), 06은 Andreas만. 논문 그림은 source/paper_figures.py가 assets/paper/에 잘라 둔다.
02의 LSI 막대는 div(PPTX 도형)·p(글 상자). 그림 위 강조 테두리는 div 4개(PPTX 도형).
사용: python3 content/acl-hop-distance-knee-work/source/build.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parents[2] / 'tools/cardkit'
FONT = '../../../templates/fonts/NotoSansKR-VF.ttf'
SCRIPTS = ''.join(f'<script>{(KIT / n).read_text(encoding="utf-8")}</script>' for n in ('qa.js', 'layers.js'))
BOX = json.loads((HERE.parent / 'assets/paper/boxes.json').read_text(encoding='utf-8'))

INK, MUTED, BLUE, RED, TINT = '#121416', '#5e6570', '#0879d8', '#cc414a', '#f0f7fc'
TRACK = '#edf1f4'

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
.note{{font-size:36px;font-weight:500;line-height:1.4;color:var(--muted);letter-spacing:-.02em}}
.label{{font-size:36px;font-weight:700;line-height:1.4;color:var(--blue);letter-spacing:-.02em}}
.accent{{color:var(--blue)}} .warn{{color:var(--red)}}
.slot{{border-radius:20px;background:var(--tint);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;flex:none}}
.slot .tag{{font-size:36px;font-weight:700;color:var(--blue);line-height:1.3}}
.slot .guide{{font-size:36px;font-weight:500;color:var(--muted);line-height:1.42}}
.paper{{background:var(--tint);border-radius:16px;flex:none}}
.photo{{position:relative;overflow:hidden;flex:none}}
.photo img{{position:absolute;left:0;top:0;display:block}}
.chart{{position:relative;width:888px;flex:none}}
.chart .a{{position:absolute;margin:0;white-space:nowrap}}
.lab{{font-size:40px;font-weight:750;line-height:1.3;letter-spacing:-.02em}}
.tick{{font-size:32px;font-weight:500;line-height:1.3;color:var(--muted)}}
.val{{font-size:52px;font-weight:850;line-height:1.15;letter-spacing:-.02em}}
.row{{display:flex;align-items:center;justify-content:space-between;width:888px;flex:none}}
.callout{{display:flex;flex-direction:column;align-items:center}}
.grp{{font-size:36px;font-weight:650;line-height:1.3;letter-spacing:-.02em}}
.num{{font-size:64px;font-weight:850;line-height:1.2;letter-spacing:-.02em}}
.sdv{{font-size:34px;font-weight:650;color:var(--muted);letter-spacing:0}}
.big{{font-size:64px;font-weight:850;line-height:1.2;letter-spacing:-.03em;color:var(--blue)}}
.name{{font-size:48px;font-weight:800;line-height:1.3;letter-spacing:-.02em}}
"""
FRAME = ('<svg class="card-frame" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">'
         '<rect x="35" y="35" width="1010" height="1280" rx="28" fill="none" stroke="#D0DCE5" stroke-width="2"/></svg>')


def gap(px):
    return f'<div style="height:{px}px;flex:none"></div>'


def rect(x, y, w, h, color):
    return f'<div style="position:absolute;left:{x:.1f}px;top:{y:.1f}px;width:{w:.1f}px;height:{h:.1f}px;background:{color}"></div>'


def outline(x0, y0, x1, y1, color, t=5):
    """강조 테두리: 선 4개(PPTX에서 각각 도형)"""
    w, h = x1 - x0, y1 - y0
    return rect(x0, y0, w, t, color) + rect(x0, y1 - t, w, t, color) + rect(x0, y0, t, h, color) + rect(x1 - t, y0, t, h, color)


def at(text, cx, top, w, cls, style=''):
    return f'<p class="a {cls}" style="left:{cx - w / 2:.1f}px;top:{top:.1f}px;width:{w}px;{style}">{text}</p>'


def slot(w, h, tag, guide):
    return f'<div class="slot" style="width:{w}px;height:{h}px"><p class="tag">{tag}</p><p class="guide">{guide}</p></div>'


def paper(src, w, alt, pad=0, box=None, color=RED, t=5):
    """논문에서 잘라 온 그림(원본 비율 유지, 폭 w). box=원본 픽셀 좌표 강조 테두리. pad>0이면 연한 바탕 위에 올림"""
    nw, nh = BOX['size'][src]
    h = w * nh / nw
    s = w / nw
    over = outline(*(v * s for v in box), color, t) if box else ''
    img = (f'<div class="photo" style="width:{w}px;height:{h:.1f}px"><img src="../assets/paper/{src}" alt="{alt}" '
           f'style="width:{w}px;height:{h:.1f}px">{over}</div>')
    if not pad:
        return img
    return f'<div class="paper" style="padding:{pad}px">{img}</div>'


def chart_lsi():
    """02: 같은 0~100% 축의 가로 막대 2개 (홉 거리 LSI 97%, 도약 시 무릎 일 LSI 69%)"""
    W, BH, ROW = 888, 64, 132
    s = []
    for i, (label, v, color) in enumerate((('홉 거리 LSI', 97, BLUE), ('도약 시 무릎 관절 일 LSI', 69, RED))):
        y = i * ROW
        s.append(at(label, W / 2, y, W, 'lab'))
        s.append(rect(0, y + 58, W, BH, TRACK))
        s.append(rect(0, y + 58, W * v / 100, BH, color))
        s.append(at(f'{v}%', W * v / 100 - 70, y + 58 + (BH - 60) / 2, 130, 'val', 'color:#fff'))
    base = ROW + 58 + BH + 12
    s.append(rect(0, base, W, 2, '#d0dce5'))
    for t, x, cx in (('0', 0, 12), ('50', W / 2 - 1, W / 2), ('100%', W - 2, W - 48)):  # 끝 눈금 글은 안전 영역 안쪽으로
        s.append(rect(x, base, 2, 12, '#d0dce5'))
        s.append(at(t, cx, base + 14, 96, 'tick'))
    return f'<div class="chart" style="height:{base + 56}px">{"".join(s)}</div>'


def callout():
    """03: Figure 3 옆 무릎 기여율 (Table 2 평균±SD). 유의 표시는 수술측–비수술측만(p<0.017 보정 기준)"""
    rows = [('수술측 <span style="color:var(--muted)">Involved</span>', '9.7%', '±3.9', RED),
            ('비수술측 <span style="color:var(--muted)">Uninvolved</span>', '13.5%', '±4.0', BLUE),
            ('대조군 <span style="color:var(--muted)">Control</span>', '11.9%', '±4.2', '#7d858d')]
    s = ['<p class="label" style="color:var(--ink)">무릎 기여율</p>', gap(26)]
    for i, (g, v, sd, c) in enumerate(rows):
        s += [f'<p class="grp">{g}</p>', f'<p class="num" style="color:{c}">{v} <span class="sdv">{sd}</span></p>']
        if i == 0:
            s += [gap(4), '<p class="label" style="font-size:34px;color:var(--ink)">↕ p &lt; 0.001</p>', gap(4)]
        elif i == 1:
            s.append(gap(26))
    return f'<div class="callout" style="width:424px">{"".join(s)}</div>'


CARDS = [
    # 01 표지 (사진 자리 유지)
    ('kind-cover', [
        '<h1 class="headline">점프 거리가 같으면<br><span class="accent">무릎</span>도 회복된 걸까?</h1>', gap(48),
        slot(888, 680, '사진 넣는 자리', '한국인 성인 선수 · 한 발 멀리뛰기<br>옆에서 전신 · 도약 직후 공중 장면'), gap(48),
        '<p class="sub">ACL 재활에서 놓치기 쉬운 평가</p>']),
    # 02 핵심 결과: 논문 제목 + 수치
    ('kind-lsi', [
        '<h1 class="headline">점프 거리는 <span class="accent">97%</span><br>무릎이 수행한 일은 <span class="warn">69%</span></h1>', gap(32),
        paper('k2022-title.png', 776, 'Kotsifaki 2022 논문 제목과 저자', pad=24), gap(14),
        '<p class="note">Kotsifaki 등 · Br J Sports Med 2022 · 복귀 승인 후 측정</p>', gap(18),
        '<p class="body strong">ACL 재건술 후 남성 선수 26명</p>', gap(36),
        chart_lsi()]),
    # 03 Figure 3 + 무릎 기여율
    ('kind-fig3', [
        '<h1 class="headline">비슷한 점프 거리,<br><span class="accent">다른 무릎의 기여</span></h1>', gap(20),
        '<p class="note">논문 Figure 3 · 도약할 때 관절별 일 기여율</p>', gap(28),
        '<div class="row">' + paper('k2022-fig3-propulsion.png', 412, 'Kotsifaki 2022 Figure 3 도약 구간 관절별 일 기여율', pad=16,
                                    box=BOX['fig3_knee'], t=10) + callout() + '</div>', gap(28),
        '<p class="body">수술한 무릎의 기여가 <span class="strong">반대쪽보다 작았습니다.</span></p>', gap(10),
        '<p class="note">그림 속 %는 반올림 값 · 평균±표준편차는 Table 2</p>']),
    # 04 Figure 2: 도약 일은 고관절·발목이 대부분
    ('kind-fig2', [
        '<h1 class="headline">점프 거리는 <span class="accent">무릎만</span><br>결정하지 않습니다</h1>', gap(14),
        '<p class="sub" style="font-weight:650">고관절과 발목이 큰 역할을 합니다</p>', gap(28),
        paper('k2022-fig2-propulsion.png', 856, 'Kotsifaki 2022 Figure 2 도약 구간 관절별 일', pad=16, box=BOX['fig2_knee'], t=4), gap(12),
        '<p class="note">논문 Figure 2 · 도약할 때 관절이 만든 일(J/kg)</p>', gap(24),
        '<p class="body">이 연구에서 도약 일의 약 88%는 고관절·발목이,<br><span class="warn strong">무릎(Knee)은 약 12%</span>를 맡았습니다.</p>']),
    # 05 가이드라인 Box 5 원문
    ('kind-guide', [
        '<h1 class="headline">그래서 Aspetar는<br><span class="accent">점프의 역학</span>까지<br>살펴봅니다</h1>', gap(32),
        paper('g2023-box5-rts.png', 840, 'Aspetar 2023 가이드라인 Box 5 스포츠 복귀 최소 기준 머리글 원문'), gap(8),
        paper('g2023-box5-jumping.png', 840, 'Aspetar 2023 가이드라인 Box 5 Jumping biomechanics 원문'), gap(28),
        '<p class="big">각도 · 모멘트 · 일</p>', gap(12),
        '<p class="body">수직·수평 점프에서 고관절·무릎·발목의<br>절대값과 좌우 대칭을 모두 정상 수준으로</p>', gap(28),
        '<p class="note">전문 선수의 복귀 평가를 위한 제안이며,<br>재부상 예방이 검증된 기준은 아닙니다.</p>']),
    # 06 Andreas 소개 (조인혁 선생님 제외 — 2026-10-26 사용자 지시)
    ('kind-lecture', [
        '<h1 class="headline">이 가이드라인에 참여한<br><span class="accent">ACL 재활 전문가</span>를<br>만납니다</h1>', gap(28),
        paper('g2023-header.png', 848, 'Aspetar 2023 가이드라인 제목과 저자, Andreas Bjerregaard 표시', pad=20,
              box=BOX['g2023_andreas'], color=BLUE, t=4), gap(36),
        '<div class="row">' + slot(272, 320, '사진 넣는 자리', 'Andreas<br>승인 프로필 사진')
        + '<div class="callout" style="width:600px"><p class="name">Andreas Bjerregaard</p>' + gap(12)
        + '<p class="note" style="color:var(--ink);font-weight:650;white-space:nowrap">2023 Aspetar ACL 재활<br>임상진료지침 공동저자</p>' + gap(10)
        + '<p class="note" style="white-space:nowrap">전 Aspetar ACL Rehabilitation Team<br>물리치료사</p></div></div>', gap(44),
        '<p class="sub accent" style="font-size:40px">R스포츠 아카데미</p>', gap(4),
        '<p class="key">ACL 재활 전문가 초청 강의</p>']),
]

for i, (kind, parts) in enumerate(CARDS, 1):
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>ACL 홉 거리 {i:02d}</title><style>{CSS}</style></head>'
            f'<body><article class="card {kind}">{FRAME}{"".join(parts)}</article>{SCRIPTS}</body></html>')
    (HERE / f'{i:02d}.html').write_text(html, encoding='utf-8')
print(f'{len(CARDS)} cards')
