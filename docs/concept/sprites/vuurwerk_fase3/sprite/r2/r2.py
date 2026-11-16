# r2: bouwt de sprite opnieuw op uit de kale reductie (kaal_dg.png + blok_w_dg.npy/blok_gem_dg.npy) met de r2-regels:
#  kop  : kop.npy (punt 1+3)
#  lijf : per spritepixel groep roze of rood (meerderheid in 5x5 blokken), tint = dichtstbijzijnde van 3 tinten van die groep
#         (roze 6/7/8, rood 6/11/12; 6 = de gedeelde donkermagenta schaduw van het model)            (punt 4)
#  pijl : roze 6/7/8 + geel 13/14/15 (magenta 9 vervalt: palet 9 wordt de donkere lijnkleur)
#  lijnen (punt 5): zwart 1 alleen op de buitenrand aan de schaduwkant; lichtkant = donkere groepstint; dubbele lijn
#         (binnenpixel tegen een randlijn) -> vlakkleur; overige binnenlijnen 1 px in de donkere tint: 9 (donkermagenta,
#         gemeten modellijn [83,24,41]) bij roze, 10 bij rood, 2 in de kop.
import numpy as np, json; from PIL import Image
from collections import Counter
PAL=json.load(open('palet.json')); PAL[9]=[83,24,41]; json.dump(PAL,open('palet_r2.json','w'))
P=np.array(PAL,float)
k=np.asarray(Image.open('kaal_dg.png')).astype(int); WT=np.load('blok_w_dg.npy'); GEM=np.load('blok_gem_dg.npy')
kop=np.load('kop.npy'); H,W=k.shape
Y,X=np.mgrid[:64,:64]
KZ=(X<26)&(Y<31)&~((X>=22)&(Y>=24))
PZ=(Y>=44)&(X<47)
a=k.copy()
# kop
a[KZ]=kop[KZ]
# pijl + lijf
roze=WT[...,7]+WT[...,8]+WT[...,9]; rood=WT[...,10]+WT[...,11]+WT[...,12]
def som5(m): 
    r=np.zeros_like(m)
    for dy in range(-2,3):
        for dx in range(-2,3): r+=np.roll(np.roll(m,dy,0),dx,1)
    return r
R5,O5=som5(roze),som5(rood)
def kies(c,ks): return ks[int(((P[ks]-c)**2).sum(1).argmin())]
for y in range(H):
    for x in range(W):
        v=k[y,x]
        if KZ[y,x] or v in (0,1,2): continue
        c=GEM[y,x]
        if PZ[y,x]:
            if v in (13,14,15): a[y,x]=kies(c,[13,14,15])
            elif v in (10,11,12) and O5[y,x]>R5[y,x]: a[y,x]=kies(c,[6,11,12])
            else: a[y,x]=kies(c,[6,7,8])
        else:
            if v in (3,4,5,13,14,15): continue        # goudstrepen in de hals (model) blijven
            a[y,x]=kies(c,[6,7,8] if R5[y,x]>=O5[y,x] else [6,11,12])
np.save('r2_vlak.npy',a)
