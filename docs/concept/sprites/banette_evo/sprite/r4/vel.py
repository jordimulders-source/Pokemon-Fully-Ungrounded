# vel.png: r3 | r2 | model op 8x (zelfde registratie: spritepixel (i,j) = modelblok 24+(i-1)*S, 1+(j-4)*S, S=968/62),
# close-ups 12x per reparatiezone, 1x/2x op licht en donker. python3 vel.py cur.npy vel.png
import sys,numpy as np; from PIL import Image, ImageDraw
from view import rgba
g=np.load(sys.argv[1]); out=sys.argv[2]; g1=np.load('r3.npy')
import importlib.util as _u; _s=_u.spec_from_file_location('p3','../r3/pal.py'); _m=_u.module_from_spec(_s); _s.loader.exec_module(_m); PAL3=_m.PAL
S=968/62; m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
def modelbox(x0,y0,x1,y1,w,h):
    mb=(24+(x0-1)*S,1+(y0-4)*S,24+(x1-1)*S,1+(y1-4)*S)
    return mw.crop(tuple(int(round(v))+200 for v in mb)).resize((w,h),Image.LANCZOS)
def sp(x0,y0,x1,y1,z,bg=(255,255,255),G=None):
    im=(rgba(g) if G is None else rgba(G,PAL3)).crop((x0,y0,x1,y1)); b=Image.new('RGBA',im.size,bg+(255,)); return Image.alpha_composite(b,im).convert('RGB').resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
W=64*8*3+60
zones=[('1 mond + 4 rechteroog',(12,22,46,46)),('3 linkerkruis',(0,14,16,30)),('2+5 Shuppet links (ogen, lijf)',(0,37,18,58)),('2+5 Shuppet rechts (ogen, lijf)',(44,40,64,63))]
rows=[]
c=Image.new('RGB',(W,560),'white'); d=ImageDraw.Draw(c)
c.paste(sp(0,0,64,64,8),(10,30)); c.paste(sp(0,0,64,64,8,G=g1),(542,30)); c.paste(modelbox(0,0,64,64,512,512),(1074,30))
d.text((10,8),'r4 8x',fill=(0,0,0)); d.text((542,8),'r3 8x',fill=(0,0,0)); d.text((1074,8),'model (zelfde registratie, dx=dy=0)',fill=(0,0,0))
rows.append(c)
for naam,(x0,y0,x1,y1) in zones:
    z=12; w,h=(x1-x0)*z,(y1-y0)*z
    c=Image.new('RGB',(max(W,3*w+40),h+30),'white'); d=ImageDraw.Draw(c); d.text((10,8),naam+' 12x (r4 | r3 | model)',fill=(0,0,0))
    c.paste(sp(x0,y0,x1,y1,z),(10,25)); c.paste(sp(x0,y0,x1,y1,z,G=g1),(w+20,25)); c.paste(modelbox(x0,y0,x1,y1,w,h),(2*w+30,25)); rows.append(c)
def modbg(z,bg):
    m=modelbox(0,0,64,64,64*z,64*z); A=np.asarray(m).astype(int); wit=(A.min(2)>=235)
    o=A.copy(); o[wit]=bg; return Image.fromarray(o.astype('uint8'))
c=Image.new('RGB',(W,180),'white'); d=ImageDraw.Draw(c); d.text((10,4),'1x: r4 | model (licht), r4 | model (donker)        2x: r4 | model (licht), r4 | model (donker)',fill=(0,0,0))
LI,DO=(248,248,248),(40,40,48); x=10
for bg in (LI,DO):
    c.paste(sp(0,0,64,64,1,bg),(x,40)); c.paste(modbg(1,bg),(x+70,40)); x+=150
for bg in (LI,DO):
    c.paste(sp(0,0,64,64,2,bg),(x,40)); c.paste(modbg(2,bg),(x+134,40)); x+=280
rows.append(c)
H=sum(r.height for r in rows); V=Image.new('RGB',(max(r.width for r in rows),H),'white'); y=0
for r in rows: V.paste(r,(0,y)); y+=r.height
V.save(out); print(V.size)
