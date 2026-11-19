# vel.png: r1 8x | model zelfde schaal | oude sprite 8x ; kop 12x: r1 | model | oude kop ; 1x en 2x op licht en donker
import sys; sys.path.insert(0,'r1'); from pal import *
from PIL import ImageDraw
f=sys.argv[1] if len(sys.argv)>1 else 'r1'
g=np.array(Image.open(f+'/anim_front.png'))[:64].astype(int)
o=np.array(Image.open('referenties/oude_sprite.png')).astype(int)
M=Image.open('referenties/gemini_gekozen_r3.png').convert('RGB')
P=16.0; O=15.0
def model(x0,y0,x1,y1,s):   # sprite-coords -> model (sprite y = natief y + 2)
    return M.crop((round(O+x0*P),round(O+(y0-2)*P),round(O+x1*P),round(O+(y1-2)*P))).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST)
W=(255,255,255)
x0,y0,x1,y1=0,6,63,64
a=naar_img(g[y0:y1,x0:x1],8,W).convert('RGB'); m=model(x0,y0,x1,y1,8); b=naar_img(o[y0:y1,x0:x1],8,W).convert('RGB')
kx0,ky0,kx1,ky1=1,32,28,57
ka=naar_img(g[ky0:ky1,kx0:kx1],12,W).convert('RGB'); km=model(kx0,ky0,kx1,ky1,12)
ko=naar_img(o[ky0-1:ky1-1,kx0+1:kx1+1],12,W).convert('RGB')   # oude kop 1 px rechts/omhoog uitgesneden: zelfde oogplek
Wd=a.width*3+40; Hd=a.height+ka.height+60
V=Image.new('RGB',(Wd,Hd),(225,225,225)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate(((a,f+' (8x)'),(m,'model Gemini r3 (zelfde schaal)'),(b,'oude sprite (8x)'))):
    V.paste(im,(i*(a.width+20),20)); d.text((i*(a.width+20)+4,4),t,fill=(0,0,0))
yk=a.height+50; d.text((4,yk-16),'kop 12x: '+f+' | model | oude kop (op de oogplek gelegd)',fill=(0,0,0))
for i,im in enumerate((ka,km,ko)): V.paste(im,(i*(ka.width+16),yk))
x=3*(ka.width+16)+20
for bg in ((248,248,248),(40,40,48)):
    V.paste(naar_img(g,1,bg).convert('RGB'),(x,yk)); V.paste(naar_img(g,2,bg).convert('RGB'),(x,yk+80)); x+=150
V.save(f+'/vel.png'); print(V.size)
