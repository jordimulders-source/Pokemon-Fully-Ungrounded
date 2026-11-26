# Sneeuwmonster r8 = r7 + Jordi: "nee de knopen zijn nog steeds niet mooi, kijk naar het model" · "de bovenste is nu ook hoekig".
# Alleen de twee knopen veranderen (opbouw van de modelknoop: donkere rand linksboven, zwarte sikkel rechtsonder,
# middengrijze vulling, lichtgrijs hooglicht als vlakje linksboven). Patroon naar de Stantler-bol (_gba, x31-35 y12-16).
# Gebruik: cd sneeuwmonster && python3 sprite_r8/bouw.py
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); import gemeen
from gemeen import *
U='sprite_r8/'
base=np.asarray(Image.open('sprite_r7/sneeuwmonster_r7.png')).astype(int)
STEEN={1,6,7,8}; SNEEUW={3,4,5}
# # = omlijning (1), d = steen donker (6), m = steen midden (7), L = steen licht (8): bestaande steentinten, geen nieuwe kleur
# (modelknoop gemeten: rand-donker L 55-67, vulling L 95-103, hooglicht L 124, sikkel L 5)
KN={
 'k5' :'.ddd./dLLm#/dmmm#/dmm##/.###.',
 'k6' :'.dddd./dLLmm#/dLmmm#/dmmmm#/dmmm##/.####.',
 'k6s':'..ddd./.dLLm#/dLmmm#/dmmmm#/dmmm#./.###..',
 'k6r':'..ddd./.dLLm#/dLmmm#/dmmmm#/.dmm##/..###.',   # voorstel Claude: 6x6 met rijbreedtes 3-5-6-6-5-3 (rondere omtrek)
}
CODE={'#':1,'d':6,'m':7,'L':8}
VAR={ # naam: (boven patroon, plek), (onder patroon, plek)
 'k5' :((KN['k5'],(24,35)),(KN['k5'],(24,41))),
 'k6' :((KN['k6'],(24,34)),(KN['k6'],(23,41))),
 'k6s':((KN['k6s'],(24,34)),(KN['k6'],(23,41))),
 'k6r':((KN['k6r'],(24,34)),(KN['k6r'],(23,41))),
}
VAK=[(22,33,30,40),(21,40,30,47)]   # knoopvakken: hierbuiten diff 0
oud=[{(X,Y) for Y in range(v[1],v[3]+1) for X in range(v[0],v[2]+1) if base[Y,X] in (6,7,8) or (base[Y,X]==1 and 23<=X<=29 and 33<=Y<=46 and all(base[Y+dy,X+dx]!=0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))))} for v in VAK]
def vorm(pat,x0,y0): return {(x0+i,y0+j):CODE[ch] for j,r in enumerate(pat.split('/')) for i,ch in enumerate(r) if ch!='.'}
uit={}
for n,((pb,lb),(po,lo)) in VAR.items():
    o=base.copy(); nieuw={**vorm(pb,*lb),**vorm(po,*lo)}
    weg=[p for s in oud for p in s if p not in nieuw]
    # oude steenpixels buiten de nieuwe knoop -> sneeuw: meest voorkomende sneeuwtint van de buren (van buiten naar binnen)
    rest=set(weg)
    while rest:
        for X,Y in sorted(rest):
            nb=[o[Y+dy,X+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)) if (X+dx,Y+dy) not in rest and (X+dx,Y+dy) not in nieuw and o[Y+dy,X+dx] in SNEEUW]
            if nb: o[Y,X]=max(set(nb),key=nb.count); rest.discard((X,Y)); break
        else: raise SystemExit('vastgelopen')
    for (X,Y),k in nieuw.items(): o[Y,X]=k
    D=np.argwhere(o!=base); assert all(any(v[0]<=X<=v[2] and v[1]<=Y<=v[3] for v in VAK) for Y,X in D)
    # knopen raken elkaar niet
    b,u=vorm(pb,*lb),vorm(po,*lo); assert not any((X+dx,Y+dy) in u for X,Y in b for dx in (-1,0,1) for dy in (-1,0,1))
    opslaan(o,U+'sneeuwmonster_r8_%s.png'%n); uit[n]=o
    print(n,'diff t.o.v. r7: %d px (knoop %d, sneeuw %d)'%(len(D),sum(1 for Y,X in D if (X,Y) in nieuw),sum(1 for Y,X in D if (X,Y) not in nieuw)))
    toon(o,32,48,19,33)
# vel
def rgbo(o,bg=(255,255,255)):
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(PAL)): img[o==k]=PAL[k]
    return Image.fromarray(img)
MI=Image.open(MODEL).convert('RGB'); f=lambda u,ph:ph+0.5+10.24*u
def mcrop(x0,y0,x1,y1,z):
    u0=(x0-X0)/S+U0; u1=(x1-X0)/S+U0; v0=(y0-Y0)/S+V0; v1=(y1-Y0)/S+V0
    return MI.crop((int(f(u0,9.05)),int(f(v0,9.25)),int(f(u1,9.05)),int(f(v1,9.25)))).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
def grid(a,z):
    dr=ImageDraw.Draw(a)
    for x in range(0,a.width,z): dr.line([(x,0),(x,a.height)],fill=(225,225,225))
    for y in range(0,a.height,z): dr.line([(0,y),(a.width,y)],fill=(225,225,225))
    return a
K=(20,32,33,49); z=16; w=(K[2]-K[0])*z; h=(K[3]-K[1])*z
B=(14,8,50,56); W8=(B[2]-B[0])*8; H8=(B[3]-B[1])*8
T=[('r7 (oud)',base)]+list(uit.items())
V=Image.new('RGB',(max(6*(w+10),5*(W8+10)),h+20+H8+30+90),'white'); dr=ImageDraw.Draw(V)
for i,(t,a) in enumerate([('model',mcrop(*K,z))]+[(t+' 16x',grid(rgbo(o).crop(K).resize((w,h),Image.NEAREST),z)) for t,o in T]):
    dr.text((i*(w+10)+2,2),t,fill=(200,0,0)); V.paste(a,(i*(w+10),14))
y=h+22
for i,(t,o) in enumerate(T):
    dr.text((i*(W8+10)+2,y),t+' 8x',fill=(200,0,0)); V.paste(rgbo(o).crop(B).resize((W8,H8),Image.NEAREST),(i*(W8+10),y+14))
y+=H8+24; x=0
for t,o in T:
    dr.text((x,y),t,fill=(200,0,0))
    for bg in [(255,255,255),(40,48,56)]: V.paste(rgbo(o,bg),(x,y+14)); x+=70
    x+=16
V.save(U+'vel.png'); print(U+'vel.png',V.size)
