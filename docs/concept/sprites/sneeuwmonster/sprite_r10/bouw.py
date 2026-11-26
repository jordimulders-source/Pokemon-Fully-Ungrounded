# Sneeuwmonster r10 = r9_v1 + Jordi (rode cirkel, blok onder links tussen voet en lijf): "dit fixen dan mag die naar de eindkeuring".
# Oorzaak: het model heeft daar een eigen middenblauw (native L ±161, tussen lijntint 2 en schaduw 3); r9 rondde dat af naar
# de lijntint -> effen donker blok. Nu: tint per pixel uit de modelhelderheid (oppervlakgewogen) met een nieuwe tint 9 = dat
# modelblauw; pixels die vooral uit de blauwe modellijn bestaan blijven lijntint 2. Buitenlijn (pixels naast transparant) blijft. Alleen zone x21-28, y47-50 (assert).
# Gebruik: cd sneeuwmonster && python3 sprite_r10/bouw.py
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); import gemeen
from gemeen import *; from klassen import klassen
U='sprite_r10/'
a,c,L=klassen()
reg=[(v,u) for v in range(74,79) for u in range(38,44) if c[v,u]==3 and 145<=L[v,u]<=175]
blauw=tuple(int(round(x)) for x in np.mean([a[v,u] for v,u in reg],0))
gemeen.PAL.append(blauw); PAL=gemeen.PAL   # index 9
base=np.asarray(Image.open('sprite_r9/sneeuwmonster_r9_v1.png')).astype(int)
ZONE=[(X,Y) for Y in range(47,51) for X in range(21,29)]
def mL(X,Y):
    acc=0; tw=0
    for u,v,w in overlap(X,Y):
        if c[v,u]!=0: acc+=w*L[v,u]; tw+=w
    return acc/tw if tw else None
def tint(l): return 1 if l<70 else 2 if l<135 else 9 if l<175 else 3 if l<212 else 4 if l<236 else 5
o=base.copy(); waarden={}
for X,Y in ZONE:
    if base[Y,X]==0: continue
    rand=any(base[Y+dy,X+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))
    l=mL(X,Y); waarden[(X,Y)]=l
    if rand or l is None: continue
    # lijnpixel: blauwe modellijn (klasse B, L<135) dekt >= 50% van de pixel -> lijntint 2 (anders middelt de lijn weg in de sneeuw)
    lijn=sum(w for u,v,w in overlap(X,Y) if c[v,u]==3 and L[v,u]<135)
    o[Y,X]=2 if lijn>=0.5 and tint(l) in (9,3) else tint(l)
    if lijn>=0.25: print('lijnpixel',(X,Y),'dekking %.2f'%lijn)
D=np.argwhere(o!=base); assert all((X,Y) in ZONE for Y,X in D)
opslaan(o,U+'sneeuwmonster_r10.png')
print('blauw (index 9) =',blauw,'uit',len(reg),'natieve pixels')
print('modelwaarden (L, oppervlakgewogen) zone x21-28:')
for Y in range(47,51): print(Y,' '.join('%4d'%waarden[(X,Y)] if waarden.get((X,Y)) is not None else '   .' for X in range(21,29)),'| voor',''.join(str(base[Y,X]) for X in range(21,29)),'na',''.join(str(o[Y,X]) for X in range(21,29)))
print('diff t.o.v. r9_v1: %d px, alle in de zone'%len(D))
# vel
def rgbo(o,bg=(255,255,255)):
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(PAL)): img[o==k]=PAL[k]
    return Image.fromarray(img)
def grid(im,z,box=None):
    dr=ImageDraw.Draw(im)
    for x in range(0,im.width,z): dr.line([(x,0),(x,im.height)],fill=(200,200,200))
    for y in range(0,im.height,z): dr.line([(0,y),(im.width,y)],fill=(200,200,200))
    if box: dr.rectangle(box,outline=(220,0,0),width=2)
    return im
MI=Image.open(MODEL).convert('RGB'); f=lambda u,ph:ph+0.5+10.24*u
def mcrop(x0,y0,x1,y1,z):
    u0=(x0-X0)/S+U0; u1=(x1-X0)/S+U0; v0=(y0-Y0)/S+V0; v1=(y1-Y0)/S+V0
    return MI.crop((int(f(u0,9.05)),int(f(v0,9.25)),int(f(u1,9.05)),int(f(v1,9.25)))).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
K=(16,42,36,53); z=16; w=(K[2]-K[0])*z; h=(K[3]-K[1])*z
bx=((21-K[0])*z,(47-K[1])*z,(29-K[0])*z,(51-K[1])*z)
B=(14,8,50,56); W8=(B[2]-B[0])*8; H8=(B[3]-B[1])*8
V=Image.new('RGB',(3*(w+10),h+20+H8+30+90),'white'); dr=ImageDraw.Draw(V)
for i,(t,im) in enumerate((('voor (r9_v1) 16x',grid(rgbo(base).crop(K).resize((w,h),Image.NEAREST),z,bx)),('na (r10) 16x',grid(rgbo(o).crop(K).resize((w,h),Image.NEAREST),z,bx)),('model',grid(mcrop(*K,z),z,bx)))):
    dr.text((i*(w+10)+2,2),t,fill=(200,0,0)); V.paste(im,(i*(w+10),14))
y=h+22
for i,(t,oo) in enumerate((('voor 8x',base),('na 8x',o))):
    dr.text((i*(W8+10)+2,y),t,fill=(200,0,0)); V.paste(rgbo(oo).crop(B).resize((W8,H8),Image.NEAREST),(i*(W8+10),y+14))
y+=H8+24; x=0
for oo in (base,o):
    for bg in [(255,255,255),(40,48,56)]: V.paste(rgbo(oo,bg),(x,y)); x+=70
    x+=16
V.save(U+'vel.png'); print(U+'vel.png',V.size)
