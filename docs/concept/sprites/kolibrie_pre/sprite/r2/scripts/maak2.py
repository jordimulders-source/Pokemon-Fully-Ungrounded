# r2: schrijft hummlet.png (oog a), hummlet_oogB.png, normal.pal, onderlaag.png en vel.png
import numpy as np, os; from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'; D=R+'docs/concept/sprites/kolibrie_pre/'; OUTD=D+'sprite/r2/'
PALTXT=open(D+'af/normal.pal').read(); PAL=[tuple(map(int,l.split())) for l in PALTXT.split('\n')[3:19]]
OX,OY=12,24
def opslaan(A,p):
    S=np.zeros((64,64),'uint8'); S[OY:OY+A.shape[0],OX:OX+A.shape[1]]=A
    im=Image.fromarray(S,'P'); im.putpalette([c for q in PAL for c in q]); im.save(p,transparency=0)
opslaan(np.load('r2_a.npy'),OUTD+'hummlet.png'); opslaan(np.load('r2_b.npy'),OUTD+'hummlet_oogB.png')
open(OUTD+'normal.pal','w').write(PALTXT)
Image.open(D+'sprite/r1/onderlaag.png').save(OUTD+'onderlaag.png')
rg=lambda p: Image.open(p).convert('RGBA')
a=rg(OUTD+'hummlet.png'); b=rg(OUTD+'hummlet_oogB.png'); r1=rg(D+'sprite/r1/hummlet.png'); on=rg(OUTD+'onderlaag.png')
old=rg(D+'af/kolibrie_pre.png'); tl=rg(R+'graphics/pokemon/taillow/anim_front.png').crop((0,0,64,64)); st=rg(R+'graphics/pokemon/starly/anim_front.png').crop((0,0,64,64))
model=Image.open(D+'referenties/gemini_gekozen_r5.png').convert('RGBA')
BG=(236,236,226,255); DK=(40,36,52,255)
up=lambda i,s: i.resize((i.width*s,i.height*s),Image.NEAREST)
C=64*8+16
V=Image.new('RGBA',(3*C+60,3*C+12*13+40),BG); d=ImageDraw.Draw(V)
items=[(a,'r2 oog a (hoofdversie) 8x'),(b,'r2 oog b (Starly) 8x'),(r1,'r1 8x'),(on,'onderlaag 8x'),(old,'oude sprite 8x'),(tl,'Taillow 8x'),(st,'Starly 8x')]
for k,(i,tx) in enumerate(items):
    x=(k%3)*C; y=(k//3)*C; V.alpha_composite(up(i,8),(x,y)); d.text((x+4,y+4),tx,fill=(0,0,0,255))
x0=C; y0=2*C
for j,bg in enumerate([BG,DK,(255,255,255,255)]):
    for k,i in enumerate([a,b,r1]):
        T=Image.new('RGBA',(64,64),bg); T.alpha_composite(i); V.alpha_composite(T,(x0+j*200+k*66,y0+10))
        V.alpha_composite(up(T,2),(x0+j*200+(k%3)*66, y0+90+ (k)*0) if False else (x0+k*136, y0+90+j*136))
d.text((x0+4,y0),'1x: oog a | oog b | r1 (licht, donker, wit);  2x eronder',fill=(0,0,0,255))
y=3*C; K=12
for k,i in enumerate([a,b]):
    V.alpha_composite(up(i.crop((OX,OY,OX+28,OY+12)),K),(k*(28*K+12),y))
mk=model.crop((int(11.5*10.24+9.25-10.24+1),int(18.5*10.24+9.25-10.24+1),int((11.5+28*77/40)*10.24+0.25),int((18.5+12*77/40)*10.24+0.25))).resize((28*K,12*K),Image.LANCZOS)
V.alpha_composite(mk,(2*(28*K+12),y)); V.alpha_composite(up(r1.crop((OX,OY,OX+28,OY+12)),K),(0,y+12*K+10)) if False else None
d.text((4,y+12*K+4),'kop 12x: oog a | oog b | model',fill=(0,0,0,255))
V.save(OUTD+'vel.png'); print(V.size)
