# Zet stap D op 64x64, schrijft hummlet.png (P, index 0 transparant), normal.pal, onderlaag.png en vel.png
import numpy as np, sys; from PIL import Image, ImageDraw
import os; R=os.path.abspath(os.path.join(os.path.dirname(__file__),'../../../../../../../'))+'/'; D=R+'docs/concept/sprites/kolibrie_pre/'; OUTD=D+'sprite/r1/'
PALTXT=open(D+'af/normal.pal').read(); PAL=[tuple(map(int,l.split())) for l in PALTXT.split('\n')[3:19]]
A=np.load('stapD.npy'); TH,TW=A.shape
OX=12; OY=58-(TH-1)
S=np.zeros((64,64),'uint8'); S[OY:OY+TH,OX:OX+TW]=A
im=Image.fromarray(S,'P'); im.putpalette([c for p in PAL for c in p]); im.save(OUTD+'hummlet.png',transparency=0)
open(OUTD+'normal.pal','w').write(PALTXT)
ond=Image.open('onderlaag.png'); O=Image.new('RGBA',(64,64),(0,0,0,0)); O.paste(ond,(OX,OY)); O.save(OUTD+'onderlaag.png')
def rgba(p): return Image.open(p).convert('RGBA')
spr=rgba(OUTD+'hummlet.png')
old=rgba(D+'af/kolibrie_pre.png')
tl=rgba(R+'graphics/pokemon/taillow/anim_front.png').crop((0,0,64,64))
st=rgba(R+'graphics/pokemon/starly/anim_front.png').crop((0,0,64,64))
model=Image.open(D+'referenties/gemini_gekozen_r5.png').convert('RGBA')
BG=(236,236,226,255); DK=(40,36,52,255)
def up(i,s): return i.resize((i.width*s,i.height*s),Image.NEAREST)
W=64*8*3+40; V=Image.new('RGBA',(W,64*8*2+64*12//2+120),BG); d=ImageDraw.Draw(V)
items=[(spr,'r1 hummlet 8x'),(O,'onderlaag (kale reductie) 8x'),(old,'oude sprite 8x'),(tl,'Taillow 8x'),(st,'Starly 8x')]
for k,(i,t) in enumerate(items):
    x=(k%3)*(64*8+20); y=(k//3)*(64*8+20)
    V.alpha_composite(up(i,8),(x,y)); d.text((x+4,y+4),t,fill=(0,0,0,255))
# 1x licht/donker
x=2*(64*8+20); y=64*8+20
for j,b in enumerate([BG,DK,(255,255,255,255)]):
    T=Image.new('RGBA',(64,64),b); T.alpha_composite(spr); V.alpha_composite(T,(x+j*70,y)); 
    T2=Image.new('RGBA',(64,64),b); T2.alpha_composite(spr); V.alpha_composite(up(T2,2),(x+j*140,y+80))
# close-up kop 12x naast model-uitsnede
y=2*(64*8+20)
kop=spr.crop((OX,OY,OX+28,OY+12)); V.alpha_composite(up(kop,12),(0,y))
mk=model.crop((120,190,120+28*1.925*10.24,190+12*1.925*10.24)).resize((28*12,12*12),Image.LANCZOS); V.alpha_composite(mk,(28*12+20,y))
ok=O.crop((OX,OY,OX+28,OY+12)); V.alpha_composite(up(ok,12),(2*(28*12+20),y))
V.save(sys.argv[1] if len(sys.argv)>1 else OUTD+'vel.png'); print('ok',OY,OX)
