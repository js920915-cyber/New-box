"""러닝 자세 v5 카드 HTML 생성: source/01.html ~ 10.html (tools/cardkit의 qa.js·layers.js 포함).
글은 h1/p, 굵기 500·650·700·750·800·850만, 사진은 overflow:hidden 크롭 안의 img.
사용: python content/running-form-change-v5/source/build.py"""
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
.photo{{position:relative;overflow:hidden;width:888px;border-radius:20px;flex:none}}
.photo img{{position:absolute;display:block}}
.bubble{{position:absolute;right:24px;top:24px;background:#fff;border-radius:24px;padding:18px 30px}}
.bubble p{{font-size:40px;font-weight:750;line-height:1.32;letter-spacing:-.03em}}
.list{{display:flex;flex-direction:column;align-items:center;gap:30px}}
.pair{{display:flex;flex-direction:column;align-items:center;gap:6px}}
.box{{background:var(--tint);border-radius:20px;padding:30px 40px;width:888px;display:flex;flex-direction:column;align-items:center;gap:12px}}
.row{{display:flex;justify-content:center;align-items:baseline;gap:48px}}
.pair2{{display:flex;gap:16px;width:888px;flex:none}}
.pair2 .ph{{position:relative;overflow:hidden;flex:1;height:620px;border-radius:20px}}
.pair2 .ph img{{position:absolute;display:block}}
.tagb{{position:absolute;left:16px;right:16px;bottom:16px;background:#fff;border-radius:18px;padding:12px 14px}}
.tagb p{{font-size:34px;font-weight:750;line-height:1.3;letter-spacing:-.03em}}
.mark{{position:absolute;left:16px;top:12px;font-size:64px;font-weight:850;line-height:1}}
.cite{{font-size:30px;font-weight:500;line-height:1.35;color:var(--muted);letter-spacing:-.01em}}
.chk{{font-size:46px;font-weight:750;line-height:1.35;letter-spacing:-.03em}}
.bars{{width:888px;display:flex;flex-direction:column;gap:24px;flex:none}}
.brow{{display:flex;flex-direction:column;align-items:flex-start;gap:8px}}
.blab{{font-size:36px;font-weight:750;line-height:1.3;letter-spacing:-.02em;text-align:left}}
.bline{{display:flex;align-items:center;gap:16px;width:888px}}
.bar{{height:46px;border-radius:8px;flex:none}}
.bar80{{height:80px}}
.bnum{{font-size:34px;font-weight:800;line-height:1;text-align:left}}
.legend{{display:flex;gap:40px;justify-content:center}}
.drake{{display:flex;flex-direction:column;gap:14px;width:888px;flex:none}}
.drow{{display:flex;width:888px;height:291px;background:var(--tint);border-radius:20px;overflow:hidden}}
.dimg{{position:relative;overflow:hidden;width:436px;height:291px;flex:none}}
.dimg img{{position:absolute;display:block}}
.dtxt{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px}}
.dmark{{font-size:64px;font-weight:850;line-height:1}}
.center{{justify-content:center;padding-bottom:104px}}
.big{{font-size:72px;font-weight:850;line-height:1.15;letter-spacing:-.03em}}
"""
FRAME = ('<svg class="card-frame" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">'
         '<rect x="35" y="35" width="1010" height="1280" rx="28" fill="none" stroke="#D0DCE5" stroke-width="2"/></svg>')


def photo(src, h, iw, ix, iy, alt, extra=''):
    """보이는 창 888×h, 이미지 폭 iw, 창 기준 위치(ix, iy) → 크롭"""
    return (f'<div class="photo" style="height:{h}px"><img src="../assets/photos/{src}" alt="{alt}" '
            f'style="width:{iw}px;left:{ix}px;top:{iy}px">{extra}</div>')


def gap(px):
    return f'<div style="height:{px}px;flex:none"></div>'


def row(pace, val):
    return f'<div class="row"><p class="item">{pace}</p><p class="big accent">{val}</p></div>'




def slot(h, label='사진 자리'):
    """대표가 직접 사진을 넣을 빈 자리 (888×h)"""
    return (f'<div class="photo" style="height:{h}px;background:#eef1f4;display:flex;align-items:center;justify-content:center">'
            f'<p class="note">{label}</p></div>')
