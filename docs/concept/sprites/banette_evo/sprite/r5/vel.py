# vel.png: r5 | r4 | model op 8x (registratie: spritepixel (i,j) = modelblok 24+(i-1)*S, 1+(j-4)*S, S=968/62),
# close-ups 12x per reparatiezone (r5 | r4 | model), 1x/2x op licht en donker naast het verkleinde model.
# python3 vel.py cur.npy vel.png   (r4 en r5 delen pal.py; alleen index 8 is lichter geworden)
import sys,numpy as np; from PIL import Image, ImageDraw
from view import rgba
g=np.load(sys.argv[1]); out=sys.argv[2]; g1=np.load('r4.npy')
import importlib.util as _u; _s=_u.spec_from_file_location('p4','../r4/pal.py'); _m=_u.module_from_spec(_s); _s.loader.exec_module(_m); PAL4=_m.PAL
S=968/62; m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
def modelbox(x0,y0,x1,y1,w,h,f=Image.LANCZOS):
    mb=(24+(x0-1)*S,1+(y0-4)*S,24+(x1-1)*S,1+(y1-4)*S)
    return mw.crop(tuple(int(round(v))+200 for v in mb)).resize((w,h),f)
def sp(x0,y0,x1,y1,z,bg=(255,255,255),G=None):
    im=(rgba(g) if G is None else rgba(G,PAL4)).crop((x0,y0,x1,y1)); b=Image.new('RGBA',im.size,bg+(255,)); return Image.alpha_composite(b,im).convert('RGB').resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
W=64*8*3+60
rows=[]
c=Image.new('RGB',(W,560),'white'); d=ImageDraw.Draw(c)
c.paste(sp(0,0,64,64,8),(10,30)); c.paste(sp(0,0,64,64,8,G=g1),(542,30)); c.paste(modelbox(0,0,64,64,512,512),(1074,30))
d.text((10,8),'r5 8x',fill=(0,0,0)); d.text((542,8),'r4 8x',fill=(0,0,0)); d.text((1074,8),'model (zelfde registratie)',fill=(0,0,0))
rows.append(c)
zones=[('1 ogen hoofd',(14,22,38,33)),('2 mond',(12,29,44,45)),('3 linkerkruis',(0,15,12,28)),('6 belletjes: links | rechts',None),
       ('4 Shuppet links (ogen)',(2,40,17,50)),('4 Shuppet rechts (ogen)',(45,45,60,56)),('5+9 draden links',(0,24,16,46)),('5 draden rechts',(48,22,64,58)),
       ('7+8+12 muts: glans, schaduwgrens, naad',(26,3,50,25)),('10 spleet hoofd/arm + 11 lap',None)]
def zrow(naam,boxes,z=12):
    parts=[]
    for (x0,y0,x1,y1) in boxes:
        w,h=(x1-x0)*z,(y1-y0)*z
        parts.append((sp(x0,y0,x1,y1,z),sp(x0,y0,x1,y1,z,G=g1),modelbox(x0,y0,x1,y1,w,h)))
    H=max(p[0].height for p in parts); Wt=sum(3*p[0].width+40 for p in parts)+10
    c=Image.new('RGB',(max(W,Wt),H+30),'white'); d=ImageDraw.Draw(c); d.text((10,8),naam+f' {z}x (r5 | r4 | model)',fill=(0,0,0)); x=10
    for a,b,mm in parts:
        c.paste(a,(x,25)); c.paste(b,(x+a.width+10,25)); c.paste(mm,(x+2*a.width+20,25)); x+=3*a.width+40
    return c
for naam,box in zones:
    if naam.startswith('6'): rows.append(zrow(naam,[(4,32,11,39),(48,16,56,23)],16))
    elif naam.startswith('10'): rows.append(zrow(naam,[(41,18,48,34),(23,44,35,51)],12))
    else:
        z=12 if (box[2]-box[0])<=24 else 10
        rows.append(zrow(naam,[box],z))
def modbg(z,bg):
    mm=modelbox(0,0,64,64,64*z,64*z,Image.BOX if z==1 else Image.LANCZOS); A=np.asarray(mm).astype(int); wit=(A.min(2)>=235)
    o=A.copy(); o[wit]=bg; return Image.fromarray(o.astype('uint8'))
c=Image.new('RGB',(W,180),'white'); d=ImageDraw.Draw(c); d.text((10,4),'1x: r5 | model (licht), r5 | model (donker)        2x: r5 | model (licht), r5 | model (donker)',fill=(0,0,0))
LI,DO=(248,248,248),(40,40,48); x=10
for bg in (LI,DO):
    c.paste(sp(0,0,64,64,1,bg),(x,40)); c.paste(modbg(1,bg),(x+70,40)); x+=150
for bg in (LI,DO):
    c.paste(sp(0,0,64,64,2,bg),(x,40)); c.paste(modbg(2,bg),(x+134,40)); x+=280
rows.append(c)
H=sum(r.height for r in rows); V=Image.new('RGB',(max(r.width for r in rows),H),'white'); y=0
for r in rows: V.paste(r,(0,y)); y+=r.height
V.save(out); print(V.size)
