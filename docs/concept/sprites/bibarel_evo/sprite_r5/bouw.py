# bouw.py ronde 5 (vanaf r4). Coördinator: borststuk zo breed als het crème borstvlak in het model, bruine romp ernaast van oksel
# tot taille, gebogen tailleband (1 px crème-donker), broek over de volle heupbreedte; schaduw 7/6/F; bovenlichaam per deel
# licht linksboven + één schaduwsikkel. Kraag/gezicht/stam/potlood/staart/klep/silhouet: diff 0 t.o.v. r4. Alleen pixelopdrachten.
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
from scipy import ndimage
r4=laad('sprite_r4/sprite.png'); T=np.load('sprite_r1/toon.npy')
o=r4.copy(); zone={}
fg=r4>0; P=np.pad(fg,1); RAND=fg&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
def z(n,x,y,v):
    if RAND[y,x]: return
    if o[y,x]!=v: o[y,x]=v
    zone[(x,y)]=n
C,S,D=7,6,15
PLOOI={(x,y) for y,(a,b) in {34:(41,42),35:(40,44),36:(40,44),37:(39,44),38:(40,43),39:(41,42)}.items() for x in range(a,b+1)}
CONTOUR={(45,35),(45,36),(45,37),(44,38),(44,39),(44,40),(44,41)}
zoom4={(22,42),(23,42),(24,43),(25,43),(26,43),(27,44),(28,44),(29,44),(30,43),(31,43),(32,43),(33,42),(34,42)}
# ---- 1. tuinbroekvorm: borststuk, bandjes en zak 1-op-1 uit het model (model_tuinbroek.py: oppervlakteaandeel per spritepixel) ----
# Jordi: "ja als de tuinbroek niet zoals het model nagemaakt wordt qua vorm is de sprite niet geslaagd"
BF=np.load('sprite_r5/bib_frac.npy'); ZF=np.load('sprite_r5/zak_frac.npy')
BIB=(BF>=0.5); BIB[:30]=False; BIB[43:]=False; BIB[:,:19]=False; BIB[:,41:]=False
LIJN=BIB&(ZF>=0.3)
# tailleband (niet in het model: alleen de broek "puur inkleuren"): direct onder de onderrand van het borststuk, volgt de buikronding
BAND={19:38,20:38,21:39,22:39,23:41,24:42,25:43,26:43,27:43,28:43,29:43,30:43,31:42,32:42,33:41,34:40,35:40,36:40,37:41,38:41,39:42,40:42,41:42,42:44}
DONKER=(1,2,8,9)
for y in range(30,46):
    for x in range(19,43):
        if (x,y) in PLOOI or (x,y) in CONTOUR or RAND[y,x] or (r4[y,x] in DONKER and not (y<34 and BIB[y,x])): continue
        if y<34 and not BIB[y,x]:
            if r4[y,x] in (C,S,D): z('bandjes',x,y,4)        # crème buiten de modelbandjes -> vacht
            continue
        if y<34:
            z('bandjes',x,y,S if LIJN[y,x] else C); continue
        b=BAND[x]
        if y<b:
            if BIB[y,x]: z('borststuk',x,y,(D if y==36 and 26<=x<=33 else S) if LIJN[y,x] else C)
            else: z('romp',x,y,4 if T[y,x]>=112 else 3)
        elif y==b: z('tailleband',x,y,D)
        else:
            v=r4[y,x]; z('broek taille',x,y, C if (v in (S,D) and y<=42 and x<=36) or (x,y) in zoom4 or v not in (C,S,D) else v)
z('tailleband',22,40,D)                                                # band doorlopend bij de stap x22->x23
# romp links: vacht, donkere eigen tint (3) langs het borststuk
for y in range(34,41):
    for x in range(19,23):
        if zone.get((x,y))=='romp':
            z('romp',x,y,3 if (x+1<64 and BIB[y,x+1]) else 4)
# romp rechts: vlekjes <3 px -> buurtint
RZ=np.zeros((64,64),bool)
for (x,y),n in zone.items():
    if n=='romp' and x>30: RZ[y,x]=True
for k in (3,4):
    lab,nn=ndimage.label((o==k)&RZ)
    for i in range(1,nn+1):
        pts=np.argwhere(lab==i)
        if len(pts)<3:
            for yy,xx in pts: z('romp',xx,yy,3 if k==4 else 4)
# borststuk: schaduwsikkel op de rechterrand (kleur, geen vorm)
for y in range(35,42):
    xs=[x for x in range(19,41) if BIB[y,x]]
    if xs and not LIJN[y,xs[-1]]: z('borststuk sikkel',xs[-1],y,S)
# ---- 2. bovenlichaam ----
# rechterschouder/arm: licht linksboven (5), schaduwsikkel aan de rechterkant (3), breder naar onder; plooi/contour/lichtvlak onderarm (r4) blijven
for y,xs in {28:range(42,47),29:range(41,45),30:range(41,43)}.items():
    for x in xs: z('rechterarm licht',x,y,5)
for y in range(27,42):
    xr=None
    for x in range(52,40,-1):
        if fg[y,x] and r4[y,x] in (2,3,4,5) and not RAND[y,x]: xr=x; break
    if xr is None: continue
    w=1 if y<=30 else (2 if y<=34 else 3)
    for x in range(xr-w+1,xr+1):
        if r4[y,x] in (3,4,5): z('rechterarm sikkel',x,y,3)
for x,y in ((49,27),): z('rechterarm sikkel',x,y,3)
# linkerarm (r4: licht linksboven, schaduw onder) + licht op het deel rechts van de vouwlijn x16
for x,y in ((17,28),(18,28),(17,29)): z('linkerarm licht',x,y,4)
opslaan(o,'sprite_r5/sprite.png',8)
import collections
d=o!=r4; print('gewijzigd t.o.v. r4:',d.sum(),'| buiten zones:',sum(1 for y,x in zip(*np.where(d)) if (x,y) not in zone))
print(dict(collections.Counter(zone[(x,y)].split(' ')[0] for y,x in zip(*np.where(d)))))
print('silhouet gelijk:',((o>0)==(r4>0)).all(),'| kleuren:',len(set(o.ravel().tolist())-{0}))
