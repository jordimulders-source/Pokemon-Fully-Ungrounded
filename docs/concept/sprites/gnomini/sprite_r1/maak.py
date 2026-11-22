# maak.py: lijf_X.png + benoemde pixelreparaties -> gnomini_A.png / gnomini_B.png; telt per zone de afwijking t.o.v. de kale reductie.
import numpy as np; from PIL import Image
from gemeen import *
def lees(p): return np.asarray(Image.open(p)).astype(int).copy()
P=np.array(PAL,float)
# reparaties (x, y, index, reden) — elk naar het model op 12x
FIX_A=[(30,37,1,'blauwe ruispixel in de lijn tussen neus en mutsrand -> zwart (model: lijn)'),
       (15,45,6,'lichte kleur op de buitenrand arm L -> selout donkerroze'),
       (16,42,6,'selout arm L gelijk trekken (midden-schaduwtint op de rand)')]
oA=lees('lijf_A.png')
for x,y,k,_ in FIX_A: oA[y,x]=k
oB=lees('lijf_B.png')
for x,y,k,_ in FIX_A: oB[y,x]=k
# B: arm R en voet R uit A overnemen, 3 px naar rechts (natief 4 kolommen = 3,1 px); zo blijven ze pixelgelijk aan A (onvervormd)
import sys
K=int(sys.argv[1]) if len(sys.argv)>1 else 4; SH=int(round(K*S))   # natief K kolommen -> SH spritepixels
zA=np.load('zone_A.npy'); zB=np.load('zone_B.npy')
for zz in (5,7):
    oB[zB==zz]=0
for zz in (5,7):
    ys,xs=np.where(zA==zz); oB[ys,xs+SH]=oA[ys,xs]
zB2=zB.copy(); zB2[np.isin(zB,(5,7))]=0
for zz in (5,7):
    ys,xs=np.where(zA==zz); zB2[ys,xs+SH]=zz
np.save('zone_B2.npy',zB2)
FIX_B=[]
for x,y,k,_ in FIX_B: oB[y,x]=k
# B: buitenrand van muts en lijf rechts onder de mutsrand (schaduwkant) zwart, zoals in A (na het verbreden kreeg die rand mutstint/selout)
fgB=oB>0
for y in range(37,50):
    for x in range(40,60):
        if zB2[y,x] in (1,3) and fgB[y,x] and not fgB[y,x+1] and oB[y,x]!=1: FIX_B.append((x,y,1,'buitenrand rechts (schaduwkant) -> zwart')); oB[y,x]=1
print('FIX_B',[(x,y) for x,y,_,_ in FIX_B])
opslaan(oA,'gnomini_A.png'); opslaan(oB,'gnomini_B.png')
for var,o,z in (('A',oA,zA),('B',oB,zB2)):
    kaal=lees('kaal_%s.png'%var)
    # kale reductie heeft een eigen palet-indexvolgorde (zelfde PAL), vergelijk op kleur
    print(var,'afwijkend t.o.v. de kale reductie per zone (px afwijkend / px zone):')
    for zz,n in ZNAAM.items():
        m=z==zz; d=(o!=kaal)&m
        print('   %-7s %3d / %3d'%(n,d.sum(),m.sum()))
    m=(z==0)&((o>0)|(kaal>0)); print('   %-7s %3d (silhouetrand: in de een wel, in de ander niet)'%('buiten',((o>0)!=(kaal>0)).sum()))
