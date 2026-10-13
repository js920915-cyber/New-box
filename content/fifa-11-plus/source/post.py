# 360x450 모바일 미리보기 + T04 영상 오버레이(창 투명) 생성·검사
import sys, json, pathlib
from PIL import Image, ImageDraw
root=pathlib.Path(__file__).resolve().parent.parent
for i in range(1,7):
    p=root/'exports'/f'{i:02d}.png'; im=Image.open(p)
    assert im.size==(1080,1350), (p, im.size)
    im.convert('RGB').resize((360,450),Image.LANCZOS).save(root/'qa'/f'{i:02d}-mobile.png')
slot=dict(x=108,y=340,width=864,height=486)
bg=Image.open(root/'video-template'/'05-video-background.png').convert('RGBA')
mask=Image.new('L',bg.size,255); ImageDraw.Draw(mask).rectangle([slot['x'],slot['y'],slot['x']+slot['width']-1,slot['y']+slot['height']-1],fill=0)
bg.putalpha(mask); out=root/'video-template'/'05-video-overlay.png'; bg.save(out)
a=Image.open(out).getchannel('A'); px=a.load(); bad=0
for y in range(1350):
    for x in range(1080):
        inside=slot['x']<=x<slot['x']+slot['width'] and slot['y']<=y<slot['y']+slot['height']
        if px[x,y]!=(0 if inside else 255): bad+=1
print('overlay alpha errors:',bad)
json.dump({"template":"T04","card":"05","slots":[dict(slot,ratio="16:9")],"note":"T04 기본 y320에서 제목 2줄 확보를 위해 y340으로 조정"},open(root/'video-template'/'placement.json','w'),ensure_ascii=False,indent=2)
