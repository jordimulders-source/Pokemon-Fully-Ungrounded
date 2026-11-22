# vel.png: r6 | r5 | model op 8x (registratie: spritepixel (i,j) = modelblok 24+(i-1)*S, 1+(j-4)*S, S=968/62),
# close-ups 12x per reparatiezone (r6 | r5 | model), Shuppet-ogen ook naast de echte Shuppet (Gen 3, 6x),
# 1x/2x op licht en donker naast het verkleinde model.   python3 vel.py cur.npy vel.png
import sys,numpy as np; from PIL import Image, ImageDraw
from view import rgba
g=np.load(sys.argv[1]); out=sys.argv[2]; g1=np.load('r5.npy')
S=968/62; m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
def modelbox(x0,y0,x1,y1,w,h,f=Image.LANCZOS):
    mb=(24+(x0-1)*S,1+(y0-4)*S,24+(x1-1)*S,1+(y1-4)*S)
    return mw.crop(tuple(int(round(v))+200 for v in mb)).resize((w,h),f)
def sp(G,x0,y0,x1,y1,z,bg=(255,255,255)):
    im=rgba(G).crop((x0,y0,x1,y1)); b=Image.new('RGBA',im.size,bg+(255,)); return Image.alpha_composite(b,im).convert('RGB').resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
W=64*8*3+60; rows=[]
c=Image.new('RGB',(W,560),'white'); d=ImageDraw.Draw(c)
c.paste(sp(g,0,0,64,64,8),(10,30)); c.paste(sp(g1,0,0,64,64,8),(542,30)); c.paste(modelbox(0,0,64,64,512,512),(1074,30))
d.text((10,8),'r6 8x',fill=(0,0,0)); d.text((542,8),'r5 8x',fill=(0,0,0)); d.text((1074,8),'model (zelfde registratie)',fill=(0,0,0)); rows.append(c)
def zrow(naam,boxes,z=12,extra=None):
    parts=[]
    for (x0,y0,x1,y1) in boxes:
        w,h=(x1-x0)*z,(y1-y0)*z; parts.append([sp(g,x0,y0,x1,y1,z),sp(g1,x0,y0,x1,y1,z),modelbox(x0,y0,x1,y1,w,h)])
    if extra: parts[-1].append(extra)
    H=max(max(q.height for q in p) for p in parts); Wt=sum(sum(q.width+10 for q in p)+30 for p in parts)+10
    c=Image.new('RGB',(max(W,Wt),H+30),'white'); d=ImageDraw.Draw(c); d.text((10,8),naam+f' {z}x (r6 | r5 | model)',fill=(0,0,0)); x=10
    for p in parts:
        for q in p: c.paste(q,(x,25)); x+=q.width+10
        x+=30
    return c
sh=Image.open('../../../../../../graphics/pokemon/shuppet/anim_front_gba.png').convert('RGBA').crop((0,0,64,64))
sb=Image.new('RGBA',sh.size,(255,255,255,255)); sh=Image.alpha_composite(sb,sh).convert('RGB').crop((12,14,46,40)).resize((34*6,26*6),Image.NEAREST)
rows.append(zrow('1+4+12 Shuppets (ogen, rand, arm) | rechts: echte Shuppet Gen 3 (6x)',[(2,40,17,57),(45,46,60,62)],12,extra=sh))
rows.append(zrow('2+13 bellen links | rechts',[(3,31,13,40),(47,15,57,24)],16))
rows.append(zrow('5+6+8+11 rode muts: steeklijn, krul, schaduwsikkel, kolom 41, druppel',[(24,3,54,50)],10))
rows.append(zrow('7 flap | 9 kruis',[(43,16,52,33),(0,16,12,27)],12))
rows.append(zrow('10 gezicht | 3 kin',[(12,14,26,38),(11,30,20,43)],12))
def modbg(z,bg):
    mm=modelbox(0,0,64,64,64*z,64*z,Image.BOX if z==1 else Image.LANCZOS); A=np.asarray(mm).astype(int); wit=(A.min(2)>=235)
    o=A.copy(); o[wit]=bg; return Image.fromarray(o.astype('uint8'))
c=Image.new('RGB',(W,180),'white'); d=ImageDraw.Draw(c); d.text((10,4),'1x: r6 | model (licht), r6 | model (donker)        2x: r6 | model (licht), r6 | model (donker)',fill=(0,0,0))
LI,DO=(248,248,248),(40,40,48); x=10
for bg in (LI,DO): c.paste(sp(g,0,0,64,64,1,bg),(x,40)); c.paste(modbg(1,bg),(x+70,40)); x+=150
for bg in (LI,DO): c.paste(sp(g,0,0,64,64,2,bg),(x,40)); c.paste(modbg(2,bg),(x+134,40)); x+=280
rows.append(c)
H=sum(r.height for r in rows); V=Image.new('RGB',(max(r.width for r in rows),H),'white'); y=0
for r in rows: V.paste(r,(0,y)); y+=r.height
V.save(out); print(V.size)
