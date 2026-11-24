# bouw.py ronde 6 (vanaf r5). Jordi: "het model doet het ook niet goed"; Gemini r5: "hier wel de juiste vorm, maar niet de juiste kleuren";
# benen "Zoals r5" (crème tot het kruis, benen bruin), kleuren "Kleuren van r10"; "en let op kleurtinten en schaduw".
# Vorm: r5_naar_sprite.py (aandeel r5-crème/zak per spritepixel, gepast op de romp van r10_k8). Benen: bruin uit de kale modelreductie
# (sprite_r1/basis.png = r10-model, met dijbollen). Kleuren: crème 7, tan rand 6, naad F (palet = r10-kleuren). Kraag/gezicht/stam/potlood/
# staart/klep/silhouet diff 0 t.o.v. r5.
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
from scipy import ndimage
r5=laad('sprite_r5/sprite.png'); BAS=laad('sprite_r1/basis.png')
CF=np.load('sprite_r6/creme_frac.npy'); ZF=np.load('sprite_r6/zak_frac.npy')
o=r5.copy(); zone={}
fg=r5>0; P=np.pad(fg,1); RAND=fg&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
KRAAG=np.zeros((64,64),bool); KRAAG[15:28,35:42]=True; KRAAG[15:28,18:21]=True; KRAAG[27:31,19:39]=True
C,S,D=7,6,15
def z(n,x,y,v,rand_ok=False):
    assert fg[y,x] and not KRAAG[y,x], (n,x,y)
    if RAND[y,x] and not rand_ok: return
    o[y,x]=v; zone[(x,y)]=n
PLOOI={(x,y) for y,(a,b) in {34:(41,42),35:(40,44),36:(40,44),37:(39,44),38:(40,43),39:(41,42)}.items() for x in range(a,b+1)}
CONTOUR={(45,35),(45,36),(45,37),(44,38),(44,39),(44,40),(44,41)}
# ---- crème-masker (r5-vorm) ----
CM=CF>=0.5; CM[:31]=False; CM[:,:19]=False; CM[59:]=False
# rechterbandje: diagonaal over de schouder (r5), alleen buiten de kraagzone; linkerbandje x22-23 r31-33 (r5-afbeelding)
STRAP=CM.copy(); STRAP[34:]=False
for y in range(28,31):
    for x in range(36,45):
        if CF[y,x]>=0.5 and not KRAAG[y,x] and fg[y,x] and not RAND[y,x]: STRAP[y,x]=True
# rechterbandje boven de kraagzone (rij 26-29) 2-3 px breed over de schouder, zoals in r5 (de r5-afbeelding valt daar in de kraagzone)
for y,(a,b) in {29:(39,41),28:(40,42)}.items():
    for x in range(a,b+1):
        if fg[y,x] and not RAND[y,x] and not KRAAG[y,x] and r5[y,x] in (2,3,4,5): STRAP[y,x]=True
CM|=STRAP
# rechterbandje rij 30-33 diagonaal zoals r5 (niet de rechte r10-bandjes)
for y in range(30,34):
    for x in range(33,41): STRAP[y,x]=False; CM[y,x]=False
for y,(a,b) in {30:(37,39),31:(36,38),32:(36,38),33:(35,37)}.items():
    for x in range(a,b+1):
        if not KRAAG[y,x]: STRAP[y,x]=True; CM[y,x]=True
# bovenrand borststuk tussen de bandjes: lichte U (midden 1 rij lager), zak + naad 1 rij lager (r5: zak y542 -> 36.7)
for x in range(26,33): CM[34,x]=False
ZF=np.roll(ZF,1,axis=0)
ZAK=(ZF>=0.5)&CM
# ---- regio die opnieuw gekleurd wordt ----
REG=np.zeros((64,64),bool)
for y in range(26,61):
    for x in range(12,54):
        if not fg[y,x] or RAND[y,x] or KRAAG[y,x] or (x,y) in PLOOI or (x,y) in CONTOUR: continue
        v=r5[y,x]
        if y>=57 and v in (8,1): continue                # voeten
        if v in (9,11,12,13,14): continue                 # hand, staart
        if v==8 and not (45<=y<=56 and x<=30): continue   # handlijn
        if v in (C,S,D) or (31<=y<=34 and 24<=x<=40) or CM[y,x] or (v==8): REG[y,x]=True
for y,x in zip(*np.where(REG)):
    if CM[y,x]: continue
    b=BAS[y,x]
    z('benen/romp',x,y,b if b in (1,2,3,4,5) or (b==8 and y>=57) else 4)
# rij 31-33 tussen de bandjes: vacht onder de bolletjes (3 direct onder een zwarte bolletjesrand, anders 4)
for y in range(31,35):
    for x in range(24,40):
        if REG[y,x] and not CM[y,x]: z('borst onder bolletjes',x,y,3 if r5[y-1,x] in (1,2,8) or o[y-1,x] in (1,) else 4)
# ---- crème: licht linksboven, sikkel aan de schaduwkant (rechts/onder), breder naar onder ----
ys,xs=np.where(CM&~STRAP); cx,cy=xs.mean(),ys.mean(); rx=(xs.max()-xs.min())/2+0.5; ry=(ys.max()-ys.min())/2+0.5
for y,x in zip(ys,xs):
    nx,ny=(x-cx)/rx,(y-cy)/ry; r=np.hypot(nx,ny); dd=(1.6*nx+ny)/np.hypot(1.6,1)   # schaduwrichting rechtsonder
    v=C
    if r>0.66 and dd>0.32: v=S
    if r>0.9 and dd>0.62: v=D
    z('crème',x,y,v)
# crème grenst aan bruin (benen) onderaan: rand in de crème-ramp (6/F), geen bruine lijn
# bandjes: crème met tan rand aan de schaduwkant
for y,x in zip(*np.where(STRAP)):
    rechts=not STRAP[y,min(63,x+1)]; z('bandjes',x,y,S if rechts else C)
# ---- zakje: lichter vlak (7) met tan omtrek (6), naad (F) erboven, afgeronde onderhoeken ----
zy,zx=np.where(ZAK); y0,y1,x0,x1=zy.min(),zy.max(),zx.min(),zx.max()
for y in range(y0,y1+1):
    for x in range(x0,x1+1):
        if not ZAK[y,x]: continue
        rand=(y==y1 or x==x0 or x==x1)
        z('zak',x,y,S if rand else C)
for x in range(x0,x1+1): z('zak naad',x,y0-1,D)
for x,y in ((x0,y1),(x1,y1)): z('zak hoek',x,y,o[y-1,x+(1 if x==x0 else -1)] if False else C)
for x,y in ((x0+1,y1),(x1-1,y1),(x0,y1-1),(x1,y1-1)): z('zak hoek',x,y,S)
# ---- linkerbeen: dijbol (licht 5) linksboven zoals in het model, schaduw (3) als sikkel rechtsonder (i.p.v. rechte 4/3-grens van de reductie) ----
for x,y in ((17,48),(18,48),(17,49),(18,49),(19,49)): z('benen dijbol',x,y,5)
for y in range(46,57):
    for x in range(15,24):
        if zone.get((x,y),'').startswith('benen') and o[y,x] in (3,4):
            grens={15:53,16:53,17:53,18:52,19:52,20:51,21:51,22:50,23:50}[x]
            z('benen',x,y,3 if y>=grens else 4)
for x,y in ((21,31),(22,31)): z('borst onder bolletjes',x,y,3)
# ---- buitenlijnen: geen zwart en bruin om en om ----
for x,y,v in ((10,33,1),(16,54,1)): z('buitenlijn',x,y,v,True)
for y in range(45,54):
    for x in range(14,20):
        if RAND[y,x] and r5[y,x]==D: z('buitenlijn',x,y,2,True)   # crème-selout -> bruine selout (been is bruin)
# ---- tintvlekjes <3 px in benen/romp en crème -> buurtint ----
for grp in ((2,3,4,5),(C,S,D)):
    M=np.zeros((64,64),bool)
    for (x,y),n in zone.items():
        if o[y,x] in grp and n!='buitenlijn' and not n.startswith('zak'): M[y,x]=True
    for k in grp:
        lab,nn=ndimage.label((o==k)&M)
        for i in range(1,nn+1):
            pts=np.argwhere(lab==i)
            if len(pts)>=3 or k==2: continue
            nb={}
            for yy,xx in pts:
                for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                    Y,X=yy+dy,xx+dx
                    if M[Y,X] and lab[Y,X]!=i: nb[o[Y,X]]=nb.get(o[Y,X],0)+1
            if nb:
                q=max(nb,key=nb.get)
                for yy,xx in pts: z(zone[(xx,yy)],xx,yy,q,True)
opslaan(o,'sprite_r6/sprite.png',8)
import collections
d=o!=r5; print('gewijzigd t.o.v. r5:',d.sum(),'| buiten zones:',sum(1 for y,x in zip(*np.where(d)) if (x,y) not in zone),'| kraagzone:',(d&KRAAG).sum(),'| y<26:',d[:26].sum())
print(dict(collections.Counter(zone[(x,y)].split(' ')[0] for y,x in zip(*np.where(d)))))
print('silhouet gelijk:',((o>0)==(r5>0)).all(),'| kleuren:',len(set(o.ravel().tolist())-{0}))
