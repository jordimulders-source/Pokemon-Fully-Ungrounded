# r9: basis r8; alleen verschuiven/afdekken (Jordi: "ja doe 1 t/m 3, maar niet opnieuw tekenen")
import numpy as np, sys
sys.path.insert(0,'../sprite_r7'); from build import save
o=np.load('../sprite_r8/bokser.npy'); a=o.copy(); NIEUW=[]
# 1 VERRE SCHOUDER: bestaande bal 2 px naar rechts, deels achter kin/borst; armaansluiting verlengd met dezelfde armpixels
D=2
bal={(x,y) for y in range(15,23) for x in range(24,32) if o[y,x]}
bal-= {(24,21),(24,22)}            # armpixels onder de bal
bal-= {(31,15),(31,16),(30,22),(31,22)}   # kop-/romppixels, geen bal
voor={(x,y) for (x,y) in [(x+D,y) for x,y in bal] if (x,y) not in bal and o[y,x]}   # kin/romp ervoor laten
voor|={(30,22),(31,22)}
for x,y in bal: a[y,x]=0
for x,y in bal:
    t=(x+D,y)
    if t not in voor: a[y,x+D]=o[y,x]
# arm verlengen: kolom x23 (laatste armkolom) herhalen in de vrijgekomen kolommen
for y in range(16,23):
    for x in range(24,24+D+1):
        if a[y,x]==0 and o[y,23]: a[y,x]=o[y,23]
# r21-22: armbodem loopt door tot de bal
for x in range(24,27):
    if a[22,x]==0: a[22,x]=1
# romp vóór de bal: omlijning waar balbinnenkant tegen een niet-lijnpixel van de romp/kin komt
for y in range(15,23):
    xs=[x for x in range(24,34) if (x,y) not in voor and a[y,x] and x-D>=24 and (x-D,y) in bal]
    if xs:
        r=max(xs)
        if (r+1,y) in voor and a[y,r+1] not in (1,) and a[y,r]!=1: a[y,r]=1; NIEUW.append((r,y))
# 2 VERRE VOET: voet + onderste stuk van het verre been 1 rij omhoog (rij r52 van het been valt weg)
F={(x,y) for y in range(52,62) for x in range(30,40) if o[y,x]}
for x,y in F: a[y,x]=0
for x,y in F: a[y-1,x]=o[y,x]
a[55,40]=o[56,40]   # schoenbovenrand-hoek mee omhoog (bestaand pixel)
# 3 TAILLEBAND: kolommen x35-37 (midden-links, lijf draait naar links) 1 px lager -> boog: hoek r32, x34 r33, x35-37 r34, x38-40 r33, hoek r32
for x in range(35,38):
    a[32,x],a[33,x],a[34,x]=o[31,x],o[32,x],o[33,x]
save(a,'bokser')
print('nieuwe omlijningspixels:',NIEUW)
d=np.argwhere(a!=o); print('gewijzigd t.o.v. r8:',len(d))
zones=[(17,14,34,24),(29,50,42,63),(30,31,44,36)]
m=np.ones(a.shape,bool)
for x0,y0,x1,y1 in zones: m[y0:y1,x0:x1]=0
print('buiten de 3 zones:',int(((a!=o)&m).sum()))
