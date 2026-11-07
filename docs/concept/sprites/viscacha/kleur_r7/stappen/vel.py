# vel.py: r7 | r6 | model op 8x; close-ups per onderdeel (sprite | model, 12x); 1x licht/donker naast model 1x
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r7/stappen')
from tl import *
import importlib.util
V6=V+'kleur_r6/'
spec=importlib.util.spec_from_file_location('p6',V6+'palet.py'); p6=importlib.util.module_from_spec(spec); spec.loader.exec_module(p6)
def rimg6(R,bg=(255,255,255)):
    im=Image.new('RGB',(64,64)); im.putdata([bg if c=='.' else p6.PAL[int(c,16)] for r in R for c in r]); return im
R7=raster(D+'raster.txt'); R6=raster(V6+'raster.txt')
s7=rimg(R7); s6=rimg6(R6); m=model(0,0,64,64,8)
# model op 1x (BOX)
a,b=mbox(0,0); c,d=mbox(64,64)
src=Image.new('RGB',(int(c-a)+2,int(d-b)+2),'white'); src.paste(SRC,(int(-a),int(-b)))
m1=src.crop((0,0,int(c-a),int(d-b))).resize((64,64),Image.BOX)
W=3*512+40; H=24+512+30
parts=[('kop + gezicht',0,14,30,46),('oren',8,14,28,28),('wang, sikkel, bef',12,26,32,46),('voorpoten',10,42,28,54),
       ('rug + lijf',22,27,50,52),('achterpoten',22,46,52,63),('staart',44,28,64,50),('pluim',48,13,62,30)]
z=10; rows=[]
for nm,x0,y0,x1,y1 in parts:
    w=(x1-x0)*z; h=(y1-y0)*z
    im=Image.new('RGB',(2*w+10,h+16),'white'); d_=ImageDraw.Draw(im); d_.text((2,2),nm,fill=(0,0,0))
    im.paste(grid(s7.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),x0,y0,z),(0,16))
    im.paste(grid(model(x0,y0,x1,y1,z),x0,y0,z),(w+10,16)); rows.append(im)
# rangschik close-ups in 2 kolommen
colw=max(r.width for r in rows)
lines=[rows[i:i+2] for i in range(0,len(rows),2)]
H2=sum(max(r.height for r in L)+10 for L in lines)
one=Image.new('RGB',(64*4*2+64*2*2+60,64*2+30),'white'); dd=ImageDraw.Draw(one)
x=0
for bg,lab in [((248,248,240),'1x licht'),((40,48,64),'1x donker')]:
    t=rimg(R7,bg); one.paste(t,(x,20)); one.paste(t.resize((128,128),Image.NEAREST),(x+70,20)); dd.text((x,2),lab,fill=(0,0,0)); x+=210
one.paste(m1,(x,20)); one.paste(m1.resize((128,128),Image.NEAREST),(x+70,20)); dd.text((x,2),'model 1x (BOX)',fill=(0,0,0))
TW=max(W,2*colw+20,one.width)
O=Image.new('RGB',(TW,H+H2+one.height+20),'white'); D_=ImageDraw.Draw(O)
for i,(im,lab) in enumerate([(s7,'r7'),(s6,'r6'),(None,'model (gemini_gekozen_ronde6, r6-schaal)')]):
    D_.text((i*(512+20)+4,4),lab,fill=(0,0,0))
    O.paste((im.resize((512,512),Image.NEAREST) if im else m),(i*(512+20),24))
y=H
for L in lines:
    x=0
    for r in L: O.paste(r,(x,y)); x+=colw+20
    y+=max(r.height for r in L)+10
O.paste(one,(0,y+10))
O.save(D+'vel.png'); print(O.size)
