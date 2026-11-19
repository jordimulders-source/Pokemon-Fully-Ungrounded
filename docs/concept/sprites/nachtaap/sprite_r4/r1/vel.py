# vel.png: r1 8x | model zelfde schaal | oude sprite 8x ; close-up kop 12x (sprite | model) ; 1x op licht en donker
import sys; sys.path.insert(0,'r1'); from pal import *
from PIL import Image, ImageDraw
g=np.array(Image.open('r1/anim_front.png'))[:64].astype(int)
o=np.array(Image.open('referenties/oude_sprite_anim_front.png'))[:64].astype(int)
M=Image.open('referenties/gemini_gekozen_r4.png').convert('RGB')
P=16.02; O=14.5
def model(x0,y0,x1,y1,s):  # sprite-coords -> modelcrop (sprite y = natief y + 1)
    return M.crop((round(O+x0*P),round(O+(y0-1)*P),round(O+x1*P),round(O+(y1-1)*P))).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST)
W=(255,255,255)
x0,y0,x1,y1=8,16,56,60
a=naar_img(g[y0:y1,x0:x1],8,W).convert('RGB'); m=model(x0,y0,x1,y1,8)
ob=o[y0:y1,x0-4:x1-4]  # oude sprite staat 4 px verder links: zelfde uitsnede-breedte
b=naar_img(ob,8,W).convert('RGB')
kx0,ky0,kx1,ky1=13,19,44,41
ka=naar_img(g[ky0:ky1,kx0:kx1],12,W).convert('RGB'); km=model(kx0,ky0,kx1,ky1,12)
Wd=a.width*3+40; Hd=a.height+ka.height+170
V=Image.new('RGB',(Wd,Hd),(235,235,235)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate(((a,'r1 (8x)'),(m,'model Gemini r4 (zelfde schaal)'),(b,'oude sprite (8x)'))):
    V.paste(im,(i*(a.width+20),20)); d.text((i*(a.width+20)+4,4),t,fill=(0,0,0))
yk=a.height+50; d.text((4,yk-16),'kop 12x: sprite | model',fill=(0,0,0))
V.paste(ka,(0,yk)); V.paste(km,(ka.width+20,yk))
x=ka.width*2+60
for bg in ((248,248,248),(40,40,48)):
    t=naar_img(g,1,bg).convert('RGB'); V.paste(t,(x,yk)); t2=naar_img(g,2,bg).convert('RGB'); V.paste(t2,(x,yk+80)); x+=150
V.save('r1/vel.png'); print(V.size)
