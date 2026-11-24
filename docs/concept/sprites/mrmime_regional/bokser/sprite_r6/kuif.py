# Bokser r6: kop = r3 (oog B), lijf = r5; alleen de linkerkuif afgeknipt tot de vorm van de rechterkuif
# (gespiegeld), die door de driekwarthoek deels achter de kop valt. Varianten: POS=minder|meer (achter de kop).
import os, numpy as np
from PIL import Image
from palet import PAL
POS=os.environ.get('POS','minder'); UIT=os.environ.get('UIT','bokser')
r5=np.load('../sprite_r5/bokser.npy')
r3=np.zeros((64,64),int); r3[0:63,10:53]=np.load('../sprite_r3/bokser.npy')   # oog B (Jordi: geen lichtgrijze cirkels)
f=r5.copy(); f[0:13,20:64]=r3[0:13,20:64]          # kop exact r3 (t/m rij 12, onderkant ogen)
# rechterkuif in r3 (rij 2-5, kol 44-50), gespiegeld -> linkerkuif
R=r3[2:6,44:51]; L=R[:,::-1].copy()
# 1. voorste kuif weg (haar over voorhoofd/schedel): rij 0-4 tot kol 43, rij 5-6 tot kol 39
weg=[(y,x) for y in range(0,7) for x in range(30,44) if f[y,x] and ((y<=4) or (y<=6 and x<=39)) and f[y,x] in (1,2,4)
     and not (y>=5 and x>=40)]
weg=[(y,x) for y,x in weg if x>=32]   # gezichtsomlijning kol 31 blijft
for y,x in weg: f[y,x]=0
# 2. kop eronder (schedel): huid + omlijning, ronding naar de voorhoofdlijn van r3 (31,6) en het achterhoofd (43,4)
SCH={3:[(35,1),(36,1),(37,1),(38,1),(39,1),(40,1),(41,1),(42,1)],
     4:[(33,1),(34,1)]+[(x,8) for x in range(35,42)]+[(42,7),(43,1)],
     5:[(32,1)]+[(x,8) for x in range(33,40)],
     6:[(32,8),(33,8),(34,8),(35,8)]}
schedel=set()
for y,l in SCH.items():
    for x,v in l: f[y,x]=v; schedel.add((y,x))
# 3. linkerkuif (vorm rechterkuif, gespiegeld) achter de kop: alleen waar nu leeg
Y0,X0={'minder':(1,29),'meer':(2,31)}[POS]
for dy in range(L.shape[0]):
    for dx in range(L.shape[1]):
        v=int(L[dy,dx]); y,x=Y0+dy,X0+dx
        if v and f[y,x]==0: f[y,x]=v
# open onderrand van de kuif dicht (kuifpixel naast transparant -> 1)
for dy in range(L.shape[0]):
    for dx in range(L.shape[1]):
        y,x=Y0+dy,X0+dx
        if f[y,x] in (2,4) and (y,x) not in schedel and any(f[yy,xx]==0 for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))): f[y,x]=1
np.save(UIT+'.npy',f)
p=Image.fromarray(f.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(UIT+'.png',transparency=0)
d=(f!=r3); d[13:,:]=False; d[:,:20]=False
print(UIT,POS,'kop anders dan r3:',int(d.sum()))
for j in range(0,9): print('%2d '%j+''.join('.' if v==0 else str(v) for v in f[j,26:56]))
