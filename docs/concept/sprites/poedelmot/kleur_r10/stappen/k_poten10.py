# poten r10: per pluim een eigen ronde omtrek (middelpunten/stralen met de hand op het model, 12x),
# lijn waar een pluim over de volgende valt, 5 klauwgroepen met 2 klauwtjes zoals het model
import math
B=[('E',49.0,51.0,5.0,5.0),('D',44.2,55.0,3.2,3.6),('B',26.5,52.0,4.5,4.0),('A',18.5,52.0,3.6,4.3),('b',27.5,57.3,2.9,2.1),('C',37.6,57.4,3.7,3.9)]
VOOR={n:i for i,(n,*_) in enumerate(B)}          # later = ervoor
def zit(x,y): return r[y][x]!='.'
own={}
for n,cx,cy,rx,ry in B:
    for y in range(45,62):
        for x in range(12,57):
            if zit(x,y) and ((x-cx)/rx)**2+((y-cy)/ry)**2<=1.0: own[(x,y)]=n
KL={(18,55),(19,55),(20,55),(19,56),(20,56),(20,57),(25,58),(24,59),(25,59),(26,59),(32,57),(33,57),(33,58),
    (35,60),(36,60),(37,60),(38,60),(39,60),(36,61),(37,61),(38,61),(39,61),(43,58),(44,58),(45,58),(46,58),(43,59),(44,59),(45,59)}
# middenstuk (achter de pluimen): tan platen met gebogen naden
for y in range(46,58):
    for x in range(29,46):
        if zit(x,y) and (x,y) not in own and (x,y) not in KL and y>=47 and r[y][x] in '67A3':
            k=round(((x-36)/3.5)**2) if 31<=x<=41 else 99
            r[y][x]='3' if y in (50-k,53-k) else ('7' if (x-30)+(y-47)<3 else '6')
for n,cx,cy,rx,ry in B:
    for (x,y),m in own.items():
        if m!=n or (x,y) in KL: continue
        u=(x-cx)/rx; v=(y-cy)/ry
        c='7' if 0.55*u+0.8*v>0.45 else 'A'
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            q=(x+dx,y+dy); o=own.get(q)
            if zit(*q) and o!=n and (o is None or VOOR[o]<VOOR[n]) and q not in KL and r[q[1]][q[0]] not in '23':
                c='3'                            # omtrek (1 px) waar deze pluim over iets erachter valt
                break
        r[y][x]=c
# klauwtjes: 2 per groep, schuin; tussenruimte 3
KLAUW={(18,55),(19,56),(20,57),(20,55),(24,59),(26,59),(32,57),(33,58),(35,60),(36,61),(38,60),(39,61),(43,58),(43,59),(45,58),(45,59)}
for p in KL: r[p[1]][p[0]]='2' if p in KLAUW else '3'
# extra klauwgroep onder B weg: pluimkleur (rand wordt lijn via k_lijn)
for x,y in [(22,55),(23,55),(24,55),(23,56),(24,56)]: r[y][x]='7'
