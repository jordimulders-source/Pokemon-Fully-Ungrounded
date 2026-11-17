# vel.png: r10 | r9 | model op 8x; mondmasker naast model op 12x; close-ups 12x (r10 | r9 | model); 1x/2x licht/donker naast model.
# python3 vel.py cur.npy vel.png
import sys,numpy as np; from PIL import Image, ImageDraw
from view import rgba; from mask import frac
g=np.load(sys.argv[1]); out=sys.argv[2]; g1=np.load('r9.npy')
S=968/62; m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
def modelbox(x0,y0,x1,y1,w,h,f=Image.LANCZOS):
    mb=(24+(x0-1)*S,1+(y0-4)*S,24+(x1-1)*S,1+(y1-4)*S)
    return mw.crop(tuple(int(round(v))+200 for v in mb)).resize((w,h),f)
def sp(G,x0,y0,x1,y1,z,bg=(255,255,255)):
    im=rgba(G).crop((x0,y0,x1,y1)); b=Image.new('RGBA',im.size,bg+(255,)); return Image.alpha_composite(b,im).convert('RGB').resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
W=64*8*3+60; rows=[]
c=Image.new('RGB',(W,560),'white'); d=ImageDraw.Draw(c)
c.paste(sp(g,0,0,64,64,8),(10,30)); c.paste(sp(g1,0,0,64,64,8),(542,30)); c.paste(modelbox(0,0,64,64,512,512),(1074,30))
d.text((10,8),'r10 8x',fill=(0,0,0)); d.text((542,8),'r9 8x',fill=(0,0,0)); d.text((1074,8),'model (zelfde registratie)',fill=(0,0,0)); rows.append(c)
# mondmasker
x0,y0,x1,y1=13,30,44,45; z=12
M=Image.new('RGB',(x1-x0,y1-y0))
for j in range(y0,y1):
    for i in range(x0,x1):
        f=frac(i,j); M.putpixel((i-x0,j-y0),(30,30,30) if f>=.5 else ((150,150,150) if f>=.25 else (245,245,245)))
M=M.resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); dm=ImageDraw.Draw(M)
for i in range(x1-x0+1): dm.line([(i*z,0),(i*z,M.height)],fill=(200,220,255))
for j in range(y1-y0+1): dm.line([(0,j*z),(M.width,j*z)],fill=(200,220,255))
parts=[sp(g,x0,y0,x1,y1,z),M,modelbox(x0,y0,x1,y1,(x1-x0)*z,(y1-y0)*z)]
c=Image.new('RGB',(max(W,sum(p.width+10 for p in parts)+10),parts[0].height+30),'white'); d=ImageDraw.Draw(c)
d.text((10,8),'1 mondband 12x: r10 | bandmasker (zwart = >=50%% van het modelblok helderheid<75, grijs 25-50%%) | model   x%d-%d y%d-%d'%(x0,x1-1,y0,y1-1),fill=(0,0,0)); x=10
for p in parts: c.paste(p,(x,25)); x+=p.width+10
rows.append(c)
def zrow(naam,boxes,z=12):
    parts=[]
    for (x0,y0,x1,y1) in boxes:
        w,h=(x1-x0)*z,(y1-y0)*z; parts.append([sp(g,x0,y0,x1,y1,z),sp(g1,x0,y0,x1,y1,z),modelbox(x0,y0,x1,y1,w,h)])
    H=max(max(q.height for q in p) for p in parts); Wt=sum(sum(q.width+10 for q in p)+30 for p in parts)+10
    c=Image.new('RGB',(max(W,Wt),H+30),'white'); d=ImageDraw.Draw(c); d.text((10,8),naam+f' {z}x (r10 | r9 | model)',fill=(0,0,0)); x=10
    for p in parts:
        for q in p: c.paste(q,(x,25)); x+=q.width+10
        x+=30
    return c
rows.append(zrow('2 bel links | bel rechts',[(3,31,13,40),(46,15,57,24)]))
rows.append(zrow('3+4+5 Shuppet links | Shuppet rechts',[(1,38,17,58),(45,42,63,62)],10))
rows.append(zrow('6 mutstop | 8 naad',[(30,3,46,14),(19,11,30,34)]))
rows.append(zrow('7 kinrand | 10 linkerkruis',[(12,34,30,47),(0,15,13,28)]))
rows.append(zrow('9 rood gezicht',[(24,11,45,33)],10))
def modbg(z,bg):
    mm=modelbox(0,0,64,64,64*z,64*z,Image.BOX if z==1 else Image.LANCZOS); A=np.asarray(mm).astype(int); wit=(A.min(2)>=235)
    o=A.copy(); o[wit]=bg; return Image.fromarray(o.astype('uint8'))
c=Image.new('RGB',(W,180),'white'); d=ImageDraw.Draw(c); d.text((10,4),'1x: r10 | model (licht), r10 | model (donker)        2x: r10 | model (licht), r10 | model (donker)',fill=(0,0,0))
LI,DO=(248,248,248),(40,40,48); x=10
for bg in (LI,DO): c.paste(sp(g,0,0,64,64,1,bg),(x,40)); c.paste(modbg(1,bg),(x+70,40)); x+=150
for bg in (LI,DO): c.paste(sp(g,0,0,64,64,2,bg),(x,40)); c.paste(modbg(2,bg),(x+134,40)); x+=280
rows.append(c)
H=sum(r.height for r in rows); V=Image.new('RGB',(max(r.width for r in rows),H),'white'); y=0
for r in rows: V.paste(r,(0,y)); y+=r.height
V.save(out); print(V.size)
