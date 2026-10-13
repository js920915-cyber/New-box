from pathlib import Path
import re
import shutil
import json

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[1]
CURRENT=PROJECT/'content/acl-return-to-running'
for d in ('assets','previews','backgrounds','overlays','qa'):
    (ROOT/d).mkdir(parents=True,exist_ok=True)
for f in ('NotoSansKR-VF.ttf','OFL.txt','font-license-metadata.txt'):
    shutil.copy2(CURRENT/'assets'/f,ROOT/'assets'/f)
css=(CURRENT/'source/cards.css').read_text(encoding='utf-8')
css+='''
.library-title {position:absolute;top:100px;left:96px;right:96px;margin:0;font-size:70px;line-height:1.18;font-weight:850;letter-spacing:-.035em;text-align:center;}
.library-title .accent,.focus-blue {color:#0879d8;}
.library-lead {position:absolute;left:96px;right:96px;font-size:34px;font-weight:650;line-height:1.4;text-align:center;}
.library-slot {position:absolute;border:2px solid #d7dce2;background:#f3f5f7;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;}
.library-slot strong {font-size:34px;font-weight:750;line-height:1.4;}
.library-slot span {font-size:28px;line-height:1.4;margin-top:12px;color:#5e6570;}
.library-clean .library-slot,.library-clean .video-slot {background:white;}
.library-clean .library-slot>*,.library-clean .video-slot>* {display:none;}
.side-point {position:absolute;left:576px;width:408px;}
.side-point strong {display:block;font-size:46px;line-height:1.3;font-weight:850;letter-spacing:-.035em;}
.side-point p {font-size:34px;line-height:1.45;margin-top:18px;}
.library-footer {position:absolute;left:96px;right:96px;top:1202px;font-size:28px;line-height:1.4;font-weight:650;text-align:center;}
.compare-label {position:absolute;top:344px;width:360px;font-size:40px;line-height:1.4;font-weight:800;text-align:center;}
.compare-note {position:absolute;top:1074px;width:360px;text-align:center;}
.compare-note strong {display:block;font-size:40px;line-height:1.3;font-weight:850;}
.compare-note p {font-size:30px;line-height:1.4;margin-top:12px;}
.big-question {position:absolute;left:96px;right:96px;top:851px;font-size:58px;font-weight:850;line-height:1.24;text-align:center;letter-spacing:-.035em;}
.focus-explain {position:absolute;top:1016px;left:96px;right:96px;font-size:34px;font-weight:650;line-height:1.4;text-align:center;}
.focus-note {position:absolute;top:1102px;width:380px;text-align:center;}
.focus-note strong {font-size:38px;font-weight:800;line-height:1.4;}
.focus-note p {font-size:30px;line-height:1.4;margin-top:12px;}
.sequence-note {position:absolute;left:578px;width:406px;}
.sequence-note strong {display:block;font-size:40px;font-weight:850;line-height:1.35;letter-spacing:-.035em;}
.sequence-note p {font-size:32px;line-height:1.45;margin-top:18px;}
'''
(ROOT/'source/templates.css').write_text(css,encoding='utf-8')
first=re.search(r'<article[^>]*>(.*?)</article>',(CURRENT/'source/04.html').read_text(encoding='utf-8'),re.S).group(1)
def slot(x,y,w,h,label,ratio):
    return f'<div class="library-slot" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><strong>{label}</strong><span>{ratio}</span></div>'
templates=[
 {'id':'T01','name':'가로 영상 + 질문 리듬','class':'video','slots':[{'x':108,'y':440,'width':864,'height':486,'ratio':'16:9'}],'body':first},
 {'id':'T02','name':'세로 영상 + 옆 해설','class':'portrait','slots':[{'x':96,'y':410,'width':432,'height':768,'ratio':'9:16'}],
 'body':'<h1 class="library-title">달리는 모습을<br><span class="accent">가까이서</span> 봅니다</h1><p class="library-lead" style="top:312px">전신과 발의 지지면이 보이게 촬영해요.</p>'+slot(96,410,432,768,'여기에<br>세로 영상을 넣어주세요','세로 9:16')+
 '<div class="side-point" style="top:426px"><strong>무릎은 어떻게?</strong><p>착지 후의 굽힘·펴짐을<br>살펴봐요.</p></div><div class="side-point" style="top:672px"><strong class="focus-blue">좌우가 다른가요?</strong><p>한쪽을 피하는 움직임이<br>있는지 봐요.</p></div><div class="side-point" style="top:918px"><strong>반복해도 같나요?</strong><p>반복하는 동안<br>움직임이 달라지나요?</p></div><p class="library-footer">영상과 함께 근력·통증·부기도 확인합니다.</p>'},
 {'id':'T03','name':'좌우 영상 비교','class':'comparison','slots':[{'x':108,'y':400,'width':360,'height':640,'ratio':'9:16'},{'x':612,'y':400,'width':360,'height':640,'ratio':'9:16'}],
 'body':'<h1 class="library-title"><span class="accent">좌우 움직임,</span><br>함께 비교해요</h1><p class="library-lead" style="top:288px">같은 조건 · 같은 각도에서 촬영해요.</p><p class="compare-label" style="left:108px">수술한 쪽</p><p class="compare-label" style="left:612px">반대쪽</p>'+slot(108,400,360,640,'왼쪽 영상','세로 9:16')+slot(612,400,360,640,'오른쪽 영상','세로 9:16')+
 '<div class="compare-note" style="left:108px"><strong>무릎 움직임은?</strong><p>착지 후 움직임을 봐요.</p></div><div class="compare-note" style="left:612px"><strong class="focus-blue">한쪽을 피하나요?</strong><p>좌우 리듬을 비교해요.</p></div><p class="library-footer">영상 비교만으로 복귀 가능을 결정하지 않습니다.</p>'},
 {'id':'T04','name':'가로 영상 + 큰 질문','class':'focus','slots':[{'x':108,'y':320,'width':864,'height':486,'ratio':'16:9'}],
 'body':'<h1 class="library-title">달릴 때의 움직임,<br><span class="accent">무엇을 볼까요?</span></h1>'+slot(108,320,864,486,'여기에 달리기 영상을 넣어주세요','가로 16:9')+
 '<p class="big-question">편해 보이면,<br>준비가 끝난 걸까요?</p><p class="focus-explain">영상과 함께 근력·통증·부기도 확인해요.</p><div class="focus-note" style="left:108px"><strong class="focus-blue">근력검사</strong><p>보이는 모습과 함께 평가해요.</p></div><div class="focus-note" style="right:108px"><strong>무릎 반응</strong><p>달린 뒤의 반응도 살펴봐요.</p></div>'},
 {'id':'T05','name':'동작 순서 + 반복 관찰','class':'sequence','slots':[{'x':96,'y':390,'width':432,'height':243,'ratio':'16:9'},{'x':96,'y':668,'width':432,'height':243,'ratio':'16:9'},{'x':96,'y':946,'width':432,'height':243,'ratio':'16:9'}],
 'body':'<h1 class="library-title">한 번보다,<br><span class="accent">반복해서</span> 봅니다</h1><p class="library-lead" style="top:310px">같은 동작의 처음 · 중간 · 끝을 담아주세요.</p>'+slot(96,390,432,243,'처음 구간','가로 16:9')+slot(96,668,432,243,'중간 구간','가로 16:9')+slot(96,946,432,243,'끝 구간','가로 16:9')+
 '<div class="sequence-note" style="top:406px"><strong>시작은 어떤가요?</strong><p>첫 움직임과<br>리듬을 살펴봐요.</p></div><div class="sequence-note" style="top:684px"><strong class="focus-blue">반복하면 달라지나요?</strong><p>움직임이 달라지는<br>구간이 있나요?</p></div><div class="sequence-note" style="top:962px"><strong>끝까지 조절되나요?</strong><p>처음과 끝의<br>움직임을 비교해요.</p></div>'},
]
for t in templates:
    for clean in (False,True):
        variant='-clean' if clean else ''
        extra=' library-clean' if clean else ''
        html=f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{t["id"]} {t["name"]}</title><link rel="stylesheet" href="templates.css"></head><body><article class="card card--{t["class"]}{extra}">{t["body"]}</article></body></html>'
        (ROOT/f'source/{t["id"]}{variant}.html').write_text(html,encoding='utf-8')
(ROOT/'placements.json').write_text(json.dumps([{k:v for k,v in t.items() if k!='body'} for t in templates],ensure_ascii=False,indent=2),encoding='utf-8')
print('5 distinct video templates built.')
