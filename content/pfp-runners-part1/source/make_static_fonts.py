"""Noto Sans KR 가변 폰트에서 카드에 쓰인 굵기별 정적 폰트를 만든다.
각 굵기를 별도 패밀리(Noto Sans KR W850 등)로 이름 붙여 PPTX/Express에서 굵기가 섞이지 않게 한다.
세로 메트릭을 hhea/typo/win 모두 1160/-288로 통일해 앱마다 줄 위치가 달라지는 것을 줄인다."""
import sys, os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools import subset

# 편집용 글자 범위: 라틴·숫자·문장부호·한글 음절 11,172자 전체·자모·전각 기호 (한자 제외로 용량 축소)
KEEP = [(0x20, 0x7E), (0xA0, 0x17F), (0x2000, 0x206F), (0x2100, 0x21FF), (0x2460, 0x24FF),
        (0x25A0, 0x25FF), (0x2600, 0x26FF), (0x3000, 0x303F), (0x1100, 0x11FF), (0x3130, 0x318F),
        (0xA960, 0xA97F), (0xAC00, 0xD7A3), (0xD7B0, 0xD7FF), (0xFF00, 0xFFEF)]

src, out = sys.argv[1], sys.argv[2]
WEIGHTS = [500, 600, 650, 700, 800, 850]
for w in WEIGHTS:
    f = TTFont(src)
    inst = instantiateVariableFont(f, {"wght": w}, updateFontNames=False)
    fam = f"Noto Sans KR W{w}"
    ps = f"NotoSansKR-W{w}"
    name = inst["name"]
    for rec in list(name.names):
        if rec.nameID in (1, 2, 3, 4, 6, 16, 17, 21, 22, 25):
            name.removeNames(nameID=rec.nameID)
    for pid, eid, lid in ((3, 1, 0x409), (1, 0, 0)):
        name.setName(fam, 1, pid, eid, lid)
        name.setName("Regular", 2, pid, eid, lid)
        name.setName(f"{ps};static instance of Noto Sans KR VF", 3, pid, eid, lid)
        name.setName(fam, 4, pid, eid, lid)
        name.setName(ps, 6, pid, eid, lid)
    os2 = inst["OS/2"]
    os2.version = max(os2.version, 4)
    os2.usWeightClass = 400
    os2.fsSelection = (os2.fsSelection & ~0b1100001) | 0b1000000 | (1 << 7)  # REGULAR + USE_TYPO_METRICS
    inst["head"].macStyle = 0
    os2.sTypoAscender, os2.sTypoDescender, os2.sTypoLineGap = 1160, -288, 0
    os2.usWinAscent, os2.usWinDescent = 1160, 288
    inst["hhea"].ascent, inst["hhea"].descent, inst["hhea"].lineGap = 1160, -288, 0
    for t in ("STAT", "MVAR", "HVAR", "avar", "fvar", "gvar"):
        if t in inst: del inst[t]
    opts = subset.Options()
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    opts.name_languages = ["*"]
    opts.notdef_outline = True
    opts.glyph_names = False
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=[u for a, b in KEEP for u in range(a, b + 1)])
    sub.subset(inst)
    p = os.path.join(out, ps + ".ttf")
    inst.save(p)
    print(p, os.path.getsize(p) // 1024, "KB")
