"""layers.json(원래 HTML 좌표)에서 Adobe Express 편집용 PPTX를 직접 작성한다. 외부 라이브러리 없음.
- 슬라이드 1080×1350px(4:5) = 11.25×14.0625in. 1px = 9525 EMU, 글자 크기 pt = px × 0.75
- 한 줄 = 한 텍스트 상자. 자동 줄바꿈(wrap=none)·자동 맞춤(noAutofit) 끔, 여백 0, 가운데 정렬·세로 가운데
- 상자는 줄 중심을 기준으로 좌우 여유를 둬서 글자 폭이 조금 달라져도 중심축과 줄 수가 유지된다
- 굵기는 굵게 버튼이 아니라 굵기별 고정 폰트 'RCardnews W{굵기}'로 지정(b=0). 한글은 ea 글꼴로 적용되므로 latin/ea/cs 모두 지정
- 프레임·연한 박스·구분선은 실제 도형, 표지 사진은 보이는 영역만 잘라 넣은 이미지"""
import json, sys, zipfile
from pathlib import Path
from xml.sax.saxutils import escape

# 사용: python tools/cardkit/build_pptx.py content/<slug>
ROOT = Path(sys.argv[1]).resolve()
BUILD = ROOT / 'adobe-express/build'
OUT = ROOT / f'adobe-express/{ROOT.name}-express.pptx'
TITLE = sys.argv[2] if len(sys.argv) > 2 else ROOT.name
EMU = 9525
SW, SH = 1080 * EMU, 1350 * EMU
PAD = 60  # 줄 상자 좌우 여유(px)
Y_NUDGE = 0.06  # 세로 보정(글자 크기 대비), verify_pptx.ps1 실측으로 조정
cards = json.loads((BUILD / 'layers.json').read_text(encoding='utf-8-sig'))
as_list = lambda v: v if isinstance(v, list) else ([] if v is None else [v])  # PowerShell JSON은 1개짜리 배열을 객체로 쓴다
for c in cards:
    c['shapes'] = as_list(c['shapes']); c['lines'] = as_list(c['lines'])
    for l in c['lines']:
        l['runs'] = as_list(l['runs'])

NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')
HDR = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'


def e(px):
    return int(round(px * EMU))


def xfrm(x, y, w, h):
    return f'<a:xfrm><a:off x="{e(x)}" y="{e(y)}"/><a:ext cx="{e(w)}" cy="{e(h)}"/></a:xfrm>'


def font(weight):
    w = min((500, 650, 700, 750, 800, 850), key=lambda v: abs(v - weight))
    return f'RCardnews W{w}'


def rpr(st, tag='a:rPr'):
    f = font(st['weight'])
    return (f'<{tag} lang="ko-KR" altLang="en-US" sz="{round(st["size"] * 75)}" b="0" i="0" '
            f'spc="{round(st["spacing"] * 75)}" kern="0" dirty="0">'
            f'<a:solidFill><a:srgbClr val="{st["color"][1:].upper()}"/></a:solidFill>'
            f'<a:latin typeface="{f}" pitchFamily="34" charset="-127"/><a:ea typeface="{f}" pitchFamily="34" charset="-127"/>'
            f'<a:cs typeface="{f}" pitchFamily="34" charset="-127"/></{tag}>')


def textbox(sid, line):
    cx = (line['left'] + line['right']) / 2
    w = line['right'] - line['left'] + 2 * PAD
    w = min(w, 2 * min(cx - 20, 1060 - cx))
    # PowerPoint는 같은 상자에서 글자를 Chrome보다 약간 위에 그린다(실측 3~4px) → 글자 크기 비례 보정
    nudge = Y_NUDGE * max(r['style']['size'] for r in line['runs'])
    x, y, h = cx - w / 2, line['top'] + nudge, line['bottom'] - line['top']
    label = ''.join(r['text'] for r in line['runs'])
    runs = ''.join(f'<a:r>{rpr(r["style"])}<a:t xml:space="preserve">{escape(r["text"])}</a:t></a:r>' for r in line['runs'])
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="{escape("텍스트: " + label[:24])}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr>{xfrm(x, y, w, h)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
            f'<p:txBody><a:bodyPr vert="horz" wrap="none" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="ctr" anchorCtr="0"><a:noAutofit/></a:bodyPr>'
            f'<a:lstStyle/><a:p><a:pPr algn="ctr"><a:lnSpc><a:spcPct val="100000"/></a:lnSpc><a:spcBef><a:spcPts val="0"/></a:spcBef>'
            f'<a:spcAft><a:spcPts val="0"/></a:spcAft><a:buNone/></a:pPr>{runs}{rpr(line["runs"][-1]["style"], "a:endParaRPr")}</a:p></p:txBody></p:sp>')


def shape(sid, name, x, y, w, h, fill=None, line=None, radius=0):
    geom = (f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val {round(radius / min(w, h) * 100000)}"/></a:avLst></a:prstGeom>'
            if radius else '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>')
    fill_x = f'<a:solidFill><a:srgbClr val="{fill[1:].upper()}"/></a:solidFill>' if fill else '<a:noFill/>'
    ln = (f'<a:ln w="{e(line[1])}"><a:solidFill><a:srgbClr val="{line[0][1:].upper()}"/></a:solidFill></a:ln>' if line else '<a:ln><a:noFill/></a:ln>')
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="{escape(name)}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr>{xfrm(x, y, w, h)}{geom}{fill_x}{ln}</p:spPr>'
            f'<p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/><a:p><a:endParaRPr lang="ko-KR"/></a:p></p:txBody></p:sp>')


def picture(sid, rid, s):
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="{sid}" name="사진" descr="{escape(s.get("alt", "사진"), {chr(34): "&quot;"})}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            f'<p:spPr>{xfrm(s["x"], s["y"], s["w"], s["h"])}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')


files, media = {}, []
for i, card in enumerate(cards, 1):
    items, sid, rels = [], 2, ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>']
    shapes = card['shapes'] if isinstance(card['shapes'], list) else [card['shapes']]
    for s in shapes:
        if s['type'] == 'photo':
            media.append(s['file']); rid = f'rId{len(rels) + 1}'
            rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{s["file"]}"/>')
            items.append(picture(sid, rid, s))
        elif s['type'] == 'box':
            items.append(shape(sid, '연한 박스', s['x'], s['y'], s['w'], s['h'], fill=s['fill'], radius=s['radius']))
        elif s['type'] == 'line':
            items.append(shape(sid, '구분선', s['x'], s['y'], s['w'], s['h'], fill=s['fill']))
        else:  # 인라인 SVG 화살표·도식 등은 자동 변환하지 않는다 → img(PNG/SVG 파일)로 넣거나 도형을 추가할 것
            print(f'WARN card {card["card"]}: PPTX에 포함되지 않은 요소 {s.get("what", s["type"])} at ({round(s["x"])},{round(s["y"])})')
        sid += 1
    items.append(shape(sid, 'B01 프레임', 34, 34, 1012, 1282, line=('#D0DCE5', 2), radius=28)); sid += 1
    for line in card['lines']:
        items.append(textbox(sid, line)); sid += 1
    files[f'ppt/slides/slide{i}.xml'] = (HDR + f'<p:sld {NS}><p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>'
        f'<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
        f'<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>{"".join(items)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')
    files[f'ppt/slides/_rels/slide{i}.xml.rels'] = HDR + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + ''.join(rels) + '</Relationships>'

n = len(cards)
ct_slides = ''.join(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>' for i in range(1, n + 1))
files['[Content_Types].xml'] = HDR + ('<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
    '<Default Extension="jpg" ContentType="image/jpeg"/><Default Extension="png" ContentType="image/png"/>'
    '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
    '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
    '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
    '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
    '<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>'
    '<Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/>'
    '<Override PartName="/ppt/tableStyles.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>'
    '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
    '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
    + ct_slides + '</Types>')
files['_rels/.rels'] = HDR + ('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>')
files['docProps/core.xml'] = HDR + ('<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" '
    'xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>' + escape(TITLE) + '</dc:title>'
    '<dc:creator>R스포츠재활센터</dc:creator></cp:coreProperties>')
files['docProps/app.xml'] = HDR + ('<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Microsoft Office PowerPoint</Application>'
    f'<Slides>{n}</Slides></Properties>')
sld_ids = ''.join(f'<p:sldId id="{255 + i}" r:id="rId{i + 2}"/>' for i in range(1, n + 1))
files['ppt/presentation.xml'] = HDR + (f'<p:presentation {NS} saveSubsetFonts="1"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
    f'<p:sldIdLst>{sld_ids}</p:sldIdLst><p:sldSz cx="{SW}" cy="{SH}"/><p:notesSz cx="6858000" cy="9144000"/><p:defaultTextStyle/></p:presentation>')
pres_rels = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>',
             '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>']
pres_rels += [f'<Relationship Id="rId{i + 2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>' for i in range(1, n + 1)]
k = n + 3
for part, typ in (('presProps.xml', 'presProps'), ('viewProps.xml', 'viewProps'), ('tableStyles.xml', 'tableStyles')):
    pres_rels.append(f'<Relationship Id="rId{k}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/{typ}" Target="{part}"/>'); k += 1
files['ppt/_rels/presentation.xml.rels'] = HDR + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + ''.join(pres_rels) + '</Relationships>'
files['ppt/presProps.xml'] = HDR + f'<p:presentationPr {NS}/>'
files['ppt/viewProps.xml'] = HDR + f'<p:viewPr {NS}><p:normalViewPr><p:restoredLeft sz="15620"/><p:restoredTop sz="94660"/></p:normalViewPr><p:gridSpacing cx="76200" cy="76200"/></p:viewPr>'
files['ppt/tableStyles.xml'] = HDR + '<a:tblStyleLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" def="{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}"/>'
EMPTY_TREE = ('<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/>'
              '<a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>')
files['ppt/slideMasters/slideMaster1.xml'] = HDR + (f'<p:sldMaster {NS}>{EMPTY_TREE}'
    '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
    '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>'
    '<p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>')
files['ppt/slideMasters/_rels/slideMaster1.xml.rels'] = HDR + ('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>')
files['ppt/slideLayouts/slideLayout1.xml'] = HDR + f'<p:sldLayout {NS} type="blank" preserve="1">{EMPTY_TREE.replace("<p:cSld>", "<p:cSld name=\"Blank\">")}<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>'
files['ppt/slideLayouts/_rels/slideLayout1.xml.rels'] = HDR + ('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>')
clr = lambda name, v: f'<a:{name}><a:srgbClr val="{v}"/></a:{name}>'
fill_style = '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
files['ppt/theme/theme1.xml'] = HDR + ('<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="RCardnews"><a:themeElements>'
    '<a:clrScheme name="RCardnews">' + '<a:dk1><a:srgbClr val="121416"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>'
    + clr('dk2', '5E6570') + clr('lt2', 'F0F7FC') + clr('accent1', '0879D8') + clr('accent2', 'CC414A') + clr('accent3', 'D0DCE5')
    + clr('accent4', '5E6570') + clr('accent5', 'F0F7FC') + clr('accent6', '121416') + clr('hlink', '0879D8') + clr('folHlink', '5E6570') + '</a:clrScheme>'
    '<a:fontScheme name="RCardnews"><a:majorFont><a:latin typeface="RCardnews W850"/><a:ea typeface="RCardnews W850"/><a:cs typeface="RCardnews W850"/></a:majorFont>'
    '<a:minorFont><a:latin typeface="RCardnews W500"/><a:ea typeface="RCardnews W500"/><a:cs typeface="RCardnews W500"/></a:minorFont></a:fontScheme>'
    '<a:fmtScheme name="RCardnews"><a:fillStyleLst>' + fill_style * 3 + '</a:fillStyleLst>'
    '<a:lnStyleLst>' + '<a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>' * 3 + '</a:lnStyleLst>'
    '<a:effectStyleLst>' + '<a:effectStyle><a:effectLst/></a:effectStyle>' * 3 + '</a:effectStyleLst>'
    '<a:bgFillStyleLst>' + fill_style * 3 + '</a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>')

OUT.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', files.pop('[Content_Types].xml'))
    for name, data in files.items():
        z.writestr(name, data)
    for m in media:
        z.write(BUILD / m, f'ppt/media/{m}')
print(f'{OUT.name}: {n} slides, {sum(len(c["lines"]) for c in cards)} line boxes')
