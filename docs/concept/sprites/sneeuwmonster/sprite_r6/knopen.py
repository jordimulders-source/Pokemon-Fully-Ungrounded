# Knopen in driekwart (Jordi: "de knopen zijn te recht" · "hij staat in driekwart"), op sneeuwmonster_r6.png.
# a: modelvorm per pixel (steendekking >= .55 op het 1024-model; geen eigen vorm)
# b: a smaller en schuiner volgens de lijfbolling: 3 breed, gekanteld ovaal = Delcatty ver-oog (_gba, (23,24)) gespiegeld
#    (XX./XXX/XXX/.XX -> .XX/XXX/XXX/XX.), zelfde kantelrichting als de bovenste modelknoop (boven naar rechts).
# Tinten per pixel uit het model: gem. helderheid van de steenpixels (< 40 zwart, < 70 steen donker, < 105 midden, anders licht).
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
U='sprite_r6/'
base=np.asarray(Image.open(U+'sneeuwmonster_r6.png')).astype(int)
M=np.asarray(Image.open(MODEL).convert('RGB')).astype(float); LM=M@[.299,.587,.114]; SM=M.max(2)-M.min(2); ST=(LM<170)&(SM<40)
fr=lambda X,ph,o0,u0: int(round(ph+0.5+10.24*((X-o0)/S+u0)))
def reg(X,Y): return np.s_[fr(Y,9.25,Y0,V0):fr(Y+1,9.25,Y0,V0),fr(X,9.05,X0,U0):fr(X+1,9.05,X0,U0)]
def dek(X,Y): return ST[reg(X,Y)].mean()
def tint(X,Y):
    r=reg(X,Y); d=ST[r]
    if not d.any(): return 6
    l=LM[r][d].mean(); return 1 if l<40 else 6 if l<70 else 7 if l<105 else 8
VAK=[(22,33,29,39),(22,40,29,46)]   # (x0,y0,x1,y1) bovenste en onderste knoop
def vorm_a(v):
    x0,y0,x1,y1=v; return {(X,Y) for Y in range(y0,y1+1) for X in range(x0,x1+1) if dek(X,Y)>=0.55}
PB=['.XX','XXX','XXX','XX.']
VORM={'a':[vorm_a(VAK[0]),vorm_a(VAK[1])],
      'b':[{(25+i,35+j) for j,r in enumerate(PB) for i,ch in enumerate(r) if ch=='X'},
           {(25+i,41+j) for j,r in enumerate(PB) for i,ch in enumerate(r) if ch=='X'}]}
oud={(X,Y) for v in VAK for Y in range(v[1],v[3]+1) for X in range(v[0],v[2]+1) if base[Y,X] in (1,6,7,8) and not any(base[Y+dy,X+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))}
uit={}
for n,(Vb,Vo) in VORM.items():
    o=base.copy()
    for X,Y in oud:   # oude knooppixels -> sneeuw: meest voorkomende sneeuwbuur (buiten de oude knoop)
        nb=[base[Y+dy,X+dx] for dy in (-2,-1,0,1,2) for dx in (-2,-1,0,1,2) if base[Y+dy,X+dx] in (3,4,5) and (X+dx,Y+dy) not in oud]
        o[Y,X]=max(set(nb),key=nb.count) if nb else 4
    for V in (Vb,Vo):
        for X,Y in V: o[Y,X]=tint(X,Y)
    opslaan(o,U+'r6_knoop_%s.png'%n); uit[n]=o
    D=np.argwhere(o!=base); assert all(any(v[0]<=X<=v[2] and v[1]<=Y<=v[3] for v in VAK) for Y,X in D)
    print('knoop',n,'diff t.o.v. r6: %d px'%len(D)); toon(o,33,46,21,30)
# vel: knoopvarianten 12x naast het model, 1x
def rgbo(o,bg=(255,255,255)):
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(PAL)): img[o==k]=PAL[k]
    return Image.fromarray(img)
MI=Image.open(MODEL).convert('RGB'); f=lambda u,ph:ph+0.5+10.24*u
def mcrop(x0,y0,x1,y1,z):
    u0=(x0-X0)/S+U0; u1=(x1-X0)/S+U0; v0=(y0-Y0)/S+V0; v1=(y1-Y0)/S+V0
    return MI.crop((int(f(u0,9.05)),int(f(v0,9.25)),int(f(u1,9.05)),int(f(v1,9.25)))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def grid(a,z):
    dr=ImageDraw.Draw(a)
    for x in range(0,a.width,z): dr.line([(x,0),(x,a.height)],fill=(225,225,225))
    for y in range(0,a.height,z): dr.line([(0,y),(a.width,y)],fill=(225,225,225))
    return a
K=(19,31,33,48); z=12; w=(K[2]-K[0])*z; h=(K[3]-K[1])*z
T=[('r6 (oud)',base),('a: modelvorm',uit['a']),('b: smaller/schuiner',uit['b']),('model',None)]
V=Image.new('RGB',(4*(w+10),h+20+80),'white'); dr=ImageDraw.Draw(V)
for i,(t,o) in enumerate(T):
    a=mcrop(*K,z) if o is None else grid(rgbo(o).crop(K).resize((w,h),Image.NEAREST),z)
    dr.text((i*(w+10)+2,2),t,fill=(200,0,0)); V.paste(a,(i*(w+10),14))
x=0
for t,o in T[:3]:
    for bg in [(255,255,255),(40,48,56)]: V.paste(rgbo(o,bg),(x,h+24)); x+=70
    x+=20
V.save(U+'vel_knopen.png'); print(U+'vel_knopen.png')
