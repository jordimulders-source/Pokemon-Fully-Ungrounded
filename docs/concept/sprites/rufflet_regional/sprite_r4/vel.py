# vel: koppen 12x (A | B | C | r2 | model | Rufflet), daaronder hele sprites 8x en 1x op licht/donker
import numpy as np; from PIL import Image, ImageDraw; from pal import *
S=12; y0,y1,x0,x1=4,18,4,24
def kop(t): return Image.fromarray(rgb(lees(t),(255,255,255))[y0:y1,x0:x1]).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)
m=Image.open('../gemini/r1.png').convert('RGB'); X=9.75+10.24*18; Y=9.75+10.24*4
mk=m.crop((int(X+20.48*x0),int(Y+20.48*y0),int(X+20.48*x1),int(Y+20.48*y1))).resize(((x1-x0)*S,(y1-y0)*S),Image.LANCZOS)
R=Image.open('../referenties/rufflet_anim_front.png').convert('RGB').crop((18,16,38,34)); R=R.resize((R.width*S,R.height*S),Image.NEAREST)
pan=[('r4A',kop('rufflet_r4A.txt')),('r4B',kop('rufflet_r4B.txt')),('r4C',kop('rufflet_r4C.txt')),('r3B',kop('rufflet_r3B.txt')),('model',mk),('Rufflet',R)]
W_=sum(p.width+16 for _,p in pan)+16; big=[Image.open(f'rufflet_r4{k}_8x.png') for k in 'ABC']
V=Image.new('RGB',(max(W_,3*(512+16)+16+2*(64+16)),40+R.height+40+512+16),(255,255,255)); d=ImageDraw.Draw(V); x=16
for n,p in pan: V.paste(p,(x,30)); d.text((x,12),n,fill=(0,0,0)); x+=p.width+16
yb=40+R.height+30
for i,(k,b) in enumerate(zip('ABC',big)):
    V.paste(b,(16+i*528,yb)); d.text((16+i*528,yb-14),k+' 8x',fill=(0,0,0))
    for j,bg in enumerate([(232,232,232),(40,44,56)]):
        s=Image.open(f'rufflet_r4{k}.png').convert('RGBA'); t=Image.new('RGB',(64,64),bg); t.paste(s,(0,0),s)
        V.paste(t,(16+3*528+j*80,yb+i*90))
V.save('vel.png'); print(V.size)
