# r16 = r15 + twee punten van Jordi (17 nov): "de gele lijn is nog steeds helemaal recht, en daar links zit nog een overbodige pixel"
# 1 linkerrand muts (was x10 kaarsrecht y12-24): S-curve naar het model (model-rand: 11.4@y12 -> 10.1@y16-19 -> 10.7@y21-22)
#   rand-x per rij: y12 11 | y13-14 10 | y15-17 9 | y18-20 10 | y21-24 11 | y25 hoek 10 (looplengtes 2,2,3,3,4)
#   selout 4 aan de lichtkant (y12-16), zwart 1 tegen het kruis (y17-25); kruis schuift y21-24 1 px de muts in
# 2 losse zwarte pixel (7,24) in de onderkant van het kruis -> 4 (kruisschaduw zoals x8-9)
# Draaien vanuit deze map: python3 build.py
from PIL import Image; import numpy as np
src=Image.open('../r15/banette_evo.png'); pal=src.getpalette(); A0=np.array(src); a=A0.copy()
def put(x,y,v): a[y,x]=v
# --- 1 muntsrand
put(10,12,0); put(11,12,4)                        # dome loopt door: y11-12 op x11
for y in (15,16): put(9,y,4); put(10,y,3)          # bolling naar links, selout, randlicht 3
put(9,17,1); put(10,17,3)                          # (9,17) was al zwart (bovenrand kruis), nu ook mutsrand
for y,cr in ((21,3),(22,3),(23,3),(24,4)):         # rand naar rechts, kruis loopt 1 px door
    put(10,y,cr); put(11,y,1); put(12,y,3)
put(10,25,1); put(11,25,3)                         # hoek rand/onderrand kruis -> oor, randlicht oor
# --- 2 overbodige pixel
put(7,24,4)
out=Image.fromarray(a.astype('uint8'),'P'); out.putpalette(pal); out.save('banette_evo.png',transparency=0)
# --- bewijs
d=np.argwhere(a!=A0)
buiten=[(x,y) for y,x in d if not (4<=x<=13 and 10<=y<=27)]
print('pixeldiff totaal',len(d),'| buiten zone x4-13 y10-27:',len(buiten))
for y,x in d: print('  (%d,%d) %d -> %d'%(x,y,A0[y,x],a[y,x]))
for y in range(12,26):
    r=a[y]; xs=[x for x in range(8,14) if r[x] in (1,4) and r[x-1] in (0,1,2,3,4) and (r[x]==4 and r[x-1]==0 or r[x]==1 and r[x+1] in (2,3,4) and r[x+1]!=1)]
    print('  y%d rand x%s'%(y,xs[-1] if xs else '?'), ''.join('.' if v==0 else '%x'%v for v in r[0:18]))
# losse pixels: niet-transparant zonder 4-buur van dezelfde index en zonder enige niet-transparante buur
z=np.pad(a,1); los=[(x,y) for y in range(64) for x in range(64) if a[y,x] and not any(z[y+1+dy,x+1+dx] for dy,dx in((0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)))]
print('geheel losse pixels:',los, '| kleuren gebruikt:',len(np.unique(a)))
