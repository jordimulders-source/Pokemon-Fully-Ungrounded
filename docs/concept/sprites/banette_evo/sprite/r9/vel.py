# vel.png: r9 | r8 | model op 8x, close-ups per reparatiezone (r9 | r8 | model), 1x/2x op licht en donker naast het verkleinde model. python3 vel.py cur.npy vel.png
import sys,numpy as np; from PIL import Image, ImageDraw
from view import rgba
g=np.load(sys.argv[1]); out=sys.argv[2]; g1=np.load('r8.npy')
S=968/62; m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
def modelbox(x0,y0,x1,y1,w,h,f=Image.LANCZOS):
    mb=(24+(x0-1)*S,1+(y0-4)*S,24+(x1-1)*S,1+(y1-4)*S)
    return mw.crop(tuple(int(round(v))+200 for v in mb)).resize((w,h),f)
def sp(G,x0,y0,x1,y1,z,bg=(255,255,255)):
    im=rgba(G).crop((x0,y0,x1,y1)); b=Image.new('RGBA',im.size,bg+(255,)); return Image.alpha_composite(b,im).convert('RGB').resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
W=64*8*3+60; rows=[]
c=Image.new('RGB',(W,560),'white'); d=ImageDraw.Draw(c)
c.paste(sp(g,0,0,64,64,8),(10,30)); c.paste(sp(g1,0,0,64,64,8),(542,30)); c.paste(modelbox(0,0,64,64,512,512),(1074,30))
d.text((10,8),'r9 8x',fill=(0,0,0)); d.text((542,8),'r8 8x',fill=(0,0,0)); d.text((1074,8),'model (zelfde registratie)',fill=(0,0,0)); rows.append(c)
def zrow(naam,boxes,z=12,extra=None):
    parts=[]
    for (x0,y0,x1,y1) in boxes:
        w,h=(x1-x0)*z,(y1-y0)*z; parts.append([sp(g,x0,y0,x1,y1,z),sp(g1,x0,y0,x1,y1,z),modelbox(x0,y0,x1,y1,w,h)])
    if extra: parts[-1].append(extra)
    H=max(max(q.height for q in p) for p in parts); Wt=sum(sum(q.width+10 for q in p)+30 for p in parts)+10
    c=Image.new('RGB',(max(W,Wt),H+30),'white'); d=ImageDraw.Draw(c); d.text((10,8),naam+f' {z}x (r9 | r8 | model)',fill=(0,0,0)); x=10
    for p in parts:
        for q in p: c.paste(q,(x,25)); x+=q.width+10
        x+=30
    return c
rows.append(zrow('1 bel links | bel rechts + 6 kruis (55,19-22)',[(3,31,13,40),(46,15,60,25)],12))
rows.append(zrow('3 steken rode kap',[(31,3,46,15)],12))
rows.append(zrow('2 kapflap (12,29) | 5 mondhoek (40-42,27-31)',[(7,24,17,33),(35,22,46,34)],12))
rows.append(zrow('4 ogen popL | popR',[(2,42,17,49),(45,48,61,55)],12))
def modbg(z,bg):
    mm=modelbox(0,0,64,64,64*z,64*z,Image.BOX if z==1 else Image.LANCZOS); A=np.asarray(mm).astype(int); wit=(A.min(2)>=235)
    o=A.copy(); o[wit]=bg; return Image.fromarray(o.astype('uint8'))
c=Image.new('RGB',(W,180),'white'); d=ImageDraw.Draw(c); d.text((10,4),'1x: r9 | model (licht), r9 | model (donker)        2x: r9 | model (licht), r9 | model (donker)',fill=(0,0,0))
LI,DO=(248,248,248),(40,40,48); x=10
for bg in (LI,DO): c.paste(sp(g,0,0,64,64,1,bg),(x,40)); c.paste(modbg(1,bg),(x+70,40)); x+=150
for bg in (LI,DO): c.paste(sp(g,0,0,64,64,2,bg),(x,40)); c.paste(modbg(2,bg),(x+134,40)); x+=280
rows.append(c)
H=sum(r.height for r in rows); V=Image.new('RGB',(max(r.width for r in rows),H),'white'); y=0
for r in rows: V.paste(r,(0,y)); y+=r.height
V.save(out); print(V.size)
