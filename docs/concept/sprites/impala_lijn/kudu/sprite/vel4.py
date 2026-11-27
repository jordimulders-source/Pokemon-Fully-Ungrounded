# Vel ronde 4 + lijnkaart hals
import json
from PIL import Image, ImageDraw
import tempfile; S=tempfile.gettempdir()+'/'
def rgba(p):
    im=Image.open(p)
    if im.mode=='P': im.save(S+'_v.png',transparency=0); im=Image.open(S+'_v.png')
    return im.convert('RGBA')
# lijnkaart: model (uitsnede hals) met de spritecellen van strengen (rood), manenrand (blauw), kaaklijn (groen) als omtrek
L=json.load(open('r4/lijnen.json')); cx0,cy0,cx1,cy1=0,18,36,50; z=24
m=Image.open('r3/model_A3.png').convert('RGBA').crop((91+cx0*16,cy0*16,91+cx1*16,cy1*16)).resize(((cx1-cx0)*z,(cy1-cy0)*z),Image.LANCZOS)
d=ImageDraw.Draw(m)
def vak(x,y,c): d.rectangle([((x-cx0)*z+2,(y-cy0)*z+2),((x-cx0+1)*z-3,(y-cy0+1)*z-3)],outline=c,width=3)
for x,y in L['streng']: vak(x,y,(230,0,0,255))
for x,y,t in L['grens']: vak(x,y,(0,170,0,255) if t=='kaak' else (0,80,255,255))
spr=rgba('r4/kudu_r4.png').crop((6+cx0,cy0,6+cx1,cy1)).resize(m.size,Image.NEAREST)
V=Image.new('RGBA',(m.size[0]*2+10,m.size[1]+40),(255,255,255,255)); dd=ImageDraw.Draw(V)
V.paste(m,(0,40)); V.paste(Image.new('RGBA',spr.size,(170,200,225,255)),(m.size[0]+10,40)); V.paste(spr,(m.size[0]+10,40),spr)
dd.text((0,4),'lijnkaart hals over model A3: rood = streng (skelet modellijn, d), blauw = manenrand over de vacht (d), groen = kaaklijn (D)',fill=(0,0,0))
dd.text((0,20),'spritecellen x %d-%d, y %d-%d op %dx; rechts r4 op dezelfde schaal'%(cx0,cx1,cy0,cy1,z),fill=(0,0,0))
V.save('r4/lijnkaart_hals.png')
# vel: r4 | r3 | model, 8x; 1x op licht en donker naast de impala
Z=512; V=Image.new('RGBA',(3*(Z+10),Z+40+170),(255,255,255,255)); d=ImageDraw.Draw(V)
r4=rgba('r4/kudu_r4.png'); r3=rgba('r3/kudu_r3.png'); imp=rgba('../../impala/af/impala.png')
mm=Image.open('r3/model_A3.png').convert('RGBA').crop((91-6*16,0,91-6*16+1024,1024)).resize((Z,Z),Image.LANCZOS)
for i,(t,im) in enumerate([('r4 8x (oog B: Ponyta + lid uit het model)',r4),('r3 8x',r3)]):
    b=im.resize((Z,Z),Image.NEAREST); V.paste(b,(i*(Z+10),20),b); d.text((i*(Z+10),4),t,fill=(0,0,0))
V.paste(mm,(2*(Z+10),20)); d.text((2*(Z+10),4),'model A3 verkleind',fill=(0,0,0))
y=Z+50
for j,bg in enumerate([(255,255,255,255),(40,44,52,255)]):
    x=j*320; V.paste(Image.new('RGBA',(300,150),bg),(x,y))
    for k,im in enumerate([r4,r3,imp]): V.paste(im,(x+10+k*95,y+40),im)
d.text((0,y-14),'1x op licht en donker: r4 | r3 | impala (af)',fill=(0,0,0))
V.save('r4/vel.png'); print('ok')
