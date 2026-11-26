# Sneeuwmonster r7 = r6_knoop_a + Jordi: "links, de stenen zijn nog steeds te recht en onder de stenen bij de linkerpoot zit een
# vlak in een effen kleur, fixen". Ogen, hoofdrand en kuif bevroren (alleen knoopvakken en zone 2 mogen veranderen; assert).
# Gebruik: cd sneeuwmonster && python3 sprite_r7/bouw.py
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *; from klassen import klassen
U='sprite_r7/'
base=np.asarray(Image.open('sprite_r6/r6_knoop_a.png')).astype(int)
a_,c,Lnat=klassen()
M=np.asarray(Image.open(MODEL).convert('RGB')).astype(float); LM=M@[.299,.587,.114]; SM=M.max(2)-M.min(2); ST=(LM<170)&(SM<40)
fr=lambda X,ph,o0,u0: int(round(ph+0.5+10.24*((X-o0)/S+u0)))
def reg(X,Y): return np.s_[fr(Y,9.25,Y0,V0):fr(Y+1,9.25,Y0,V0),fr(X,9.05,X0,U0):fr(X+1,9.05,X0,U0)]
def dek(X,Y): return ST[reg(X,Y)].mean()
def steentint(X,Y):   # tint per pixel uit het model; pixel zonder steendekking -> dichtstbijzijnde pixel met dekking
    best=None
    for r in range(0,4):
        for dy in range(-r,r+1):
            for dx in range(-r,r+1):
                if max(abs(dx),abs(dy))!=r: continue
                rr=reg(X+dx,Y+dy); d=ST[rr]
                if d.mean()>=0.15:
                    l=LM[rr][d].mean(); return 1 if l<40 else 6 if l<70 else 7 if l<105 else 8
    return 6
# modelsneeuw per spritepixel (oppervlakgewogen, alleen sneeuwklasse) voor zone 2
def mw(X,Y):
    fw=lw=0
    for u,v,w in overlap(X,Y):
        if c[v,u]==4: fw+=w; lw+=w*Lnat[v,u]
    return lw/fw if fw>0.2 else None
def tw(l): return 3 if l<212 else 4 if l<236 else 5
def P(s): return [r for r in s.split('/')]
def vorm(pat,x0,y0): return {(x0+i,y0+j) for j,r in enumerate(P(pat)) for i,ch in enumerate(r) if ch=='X'}
def plaats(pat,vak):   # beste plek op het model: max som(dekking - 0,5) over de patroonpixels
    x0,y0,x1,y1=vak; best=None
    for yy in range(y0-1,y1-len(P(pat))+2):
        for xx in range(x0-1,x1-len(P(pat)[0])+2):
            sc=sum(dek(X,Y)-0.5 for X,Y in vorm(pat,xx,yy))
            if best is None or sc>best[0]: best=(sc,xx,yy)
    return best[1],best[2]
VAK=[(23,33,28,39),(22,40,28,45)]
VAR={ # naam: (patroon boven, patroon onder, bron)
 's1':('.XX./.XXX/XXXX/XXXX/.XX.','.XXX./XXXXX/XXXXX/.XXX.',
       'boven: Girafarig (26,23) / Mantine (6,24) _gba gespiegeld (4x5 schuin ovaal); onder: Horsea (23,20), Kangaskhan, Lairon, Pinsir, Seaking _gba (5x4 rond)'),
 's2':('..XX/.XXX/XXXX/XXX./.XX.','.XXX./XXXXX/XXXXX/XXXX./.XX..',
       'boven: s1 sterker gekanteld (boven naar rechts); onder: Charizard (18,48) / Egg (35,26) _gba (5x5, onderkant naar links = gekanteld rond)'),
 's3':('.XXX./XXXXX/XXXXX/.XXX.','.XXX./XXXXX/XXXXX/.XXX.',
       'beide: rondste en meest voorkomende 5x4-steentje in _gba (Horsea, Kangaskhan, Lairon, Pinsir, Seaking: 9x)'),
}
def zone2(o,knoop):   # effen vlak onder de stenen bij de linkerpoot: sneeuwtint per pixel uit de modelhelderheid
    Z=[(X,Y) for Y in range(41,49) for X in range(19,35) if o[Y,X] in (3,4,5) and (X,Y) not in knoop]
    for X,Y in Z:
        m=mw(X,Y)
        if m is not None: o[Y,X]=tw(m)
    # ontkorrelen binnen de zone (vlekjes < 3 px, licht < 2)
    for k,mn in ((3,3),(4,3),(5,2)):
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            mm=lab==i; pts=list(zip(*np.where(mm)))
            if mm.sum()>=mn or not all((x,y) in Z for y,x in pts): continue
            nb=[o[y+dy,x+dx] for y,x in pts for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if o[y+dy,x+dx] in (3,4,5) and o[y+dy,x+dx]!=k]
            if nb: o[mm]=max(set(nb),key=nb.count)
    return o
oudknoop={(X,Y) for v in VAK for Y in range(v[1],v[3]+1) for X in range(v[0],v[2]+1) if base[Y,X] in (1,6,7,8) and not any(base[Y+dy,X+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))}
def mag(X,Y): return any(v[0]<=X<=v[2] and v[1]<=Y<=v[3] for v in VAK) or (19<=X<=34 and 41<=Y<=48)
uit={}
for n,(pb,po,bron) in VAR.items():
    o=base.copy()
    for X,Y in oudknoop:
        m=mw(X,Y); o[Y,X]=tw(m) if m is not None else 4
    kn=set()
    for pat,vak in ((pb,VAK[0]),(po,VAK[1])):
        xx,yy=plaats(pat,vak); V=vorm(pat,xx,yy); kn|=V
        for X,Y in V: o[Y,X]=steentint(X,Y)
        print(n,'knoop op',(xx,yy),pat)
    o=zone2(o,kn)
    D=np.argwhere(o!=base); assert all(mag(X,Y) for Y,X in D)
    opslaan(o,U+'r7_%s.png'%n); uit[n]=o
    print(n,'diff t.o.v. r6_knoop_a: %d px (knopen %d, zone 2 %d) | %s'%(len(D),sum(1 for Y,X in D if any(v[0]<=X<=v[2] and v[1]<=Y<=v[3] for v in VAK)),sum(1 for Y,X in D if not any(v[0]<=X<=v[2] and v[1]<=Y<=v[3] for v in VAK)),bron))
    toon(o,33,50,18,36)
print('modelwaarden zone 2 (L sneeuw per spritepixel, x19-34):')
for Y in range(41,49): print('%2d '%Y+' '.join('  .' if mw(X,Y) is None or base[Y,X]==0 else '%3d'%mw(X,Y) for X in range(19,35)))
BEST='s1'; opslaan(uit[BEST],U+'sneeuwmonster_r7.png')
# vel
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
K8=(17,30,37,52); z8=8; w8=(K8[2]-K8[0])*z8; h8=(K8[3]-K8[1])*z8
K2=(17,39,37,51); z=12; w2=(K2[2]-K2[0])*z; h2=(K2[3]-K2[1])*z
T=[('s1',uit['s1']),('s2',uit['s2']),('s3',uit['s3']),('model',None)]
B=(14,8,50,56); W8=(B[2]-B[0])*8; H8=(B[3]-B[1])*8
V=Image.new('RGB',(max(4*(w8+10),3*(w2+10),2*(W8+10)),h8+20+h2+30+H8+30+90),'white'); dr=ImageDraw.Draw(V)
for i,(t,o) in enumerate(T):
    a=mcrop(*K8,z8) if o is None else grid(rgbo(o).crop(K8).resize((w8,h8),Image.NEAREST),z8)
    dr.text((i*(w8+10)+2,2),t+' (knopen 8x)',fill=(200,0,0)); V.paste(a,(i*(w8+10),14))
y=h8+22
for i,(t,a) in enumerate((('zone 2 voor (r6_knoop_a)',grid(rgbo(base).crop(K2).resize((w2,h2),Image.NEAREST),z)),('zone 2 na (r7 %s)'%BEST,grid(rgbo(uit[BEST]).crop(K2).resize((w2,h2),Image.NEAREST),z)),('model',mcrop(*K2,z)))):
    dr.text((i*(w2+10)+2,y),t,fill=(200,0,0)); V.paste(a,(i*(w2+10),y+14))
y+=h2+30
for i,(t,a) in enumerate((('r7 (%s) 8x'%BEST,rgbo(uit[BEST]).crop(B).resize((W8,H8),Image.NEAREST)),('model',mcrop(*B,8)))):
    dr.text((i*(W8+10)+2,y),t,fill=(200,0,0)); V.paste(a,(i*(W8+10),y+14))
y+=H8+24; x=0
for t,o in T[:3]:
    for bg in [(255,255,255),(40,48,56)]: V.paste(rgbo(o,bg),(x,y)); x+=70
    x+=16
V.save(U+'vel.png'); print(U+'vel.png',V.size)
