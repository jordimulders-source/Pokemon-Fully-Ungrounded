# Koeienvanger vereenvoudigen (Jordi 16 nov: "verder heb je mijn goedkeuring om de trein wat simpeler te maken").
# Silhouet (r4-masker) en groene gloed blijven; ijzer/roest binnen het masker wordt per spijl: lichte kant links,
# donkere kant rechts, donkere tussenruimte (zwart) op de plekken van het model en van de bevroren rij 48 erboven.
# Onderste rijen een tint donkerder (schaduw rechtsonder), onderrand zwart, linkerrand selout (C).
from PIL import Image; import numpy as np
IN='sprite_r6/stap_geest.png'; OUT='sprite_r6/stap_kv.png'
s=Image.open(IN); pal=s.getpalette(); a=np.array(s); r4=a.copy()
H={'1':1,'7':7,'8':8,'9':9,'A':10,'B':11,'C':12}
IJZER={1,7,8,9,10,11,12}
# spijlen (x-bereik, tonen licht->donker) op de plekken van het model / bevroren rij 48; tussenruimtes x4, x11, x17 zwart
SPIJL=[(0,3,['7','A','B','C']),(5,10,['A','B','B','C']),(12,16,['7','8','9','9']),(18,22,['A','B','B','C'])]
TUSSEN={4,11,17}
def toon(x,y):
    if x in TUSSEN: return '1'
    for x0,x1,t in SPIJL:
        if x0<=x<=x1:
            u=(x-x0)/(x1-x0)*2.6 + (y-49)/5.0   # facet: licht linksboven, donker rechtsonder (diagonale grens)
            return t[min(3,int(u))]
ROEST={(7,52):'8',(8,52):'8',(7,53):'8',(8,53):'9',(7,54):'9',(8,54):'9',      # roestvlek spijl 2 (model: midden)
       (19,51):'8',(20,51):'8',(21,51):'9',(19,52):'8',(20,52):'9',(21,52):'9'}  # roestvlek spijl 4
DONKER={'A':'B','B':'C','7':'A','8':'9','C':'C','9':'9','1':'1'}
Y0,Y1=49,60
for y in range(Y0,Y1+1):
    for x in range(0,23):
        if r4[y,x] not in IJZER: continue
        c=ROEST.get((x,y),toon(x,y))
        a[y,x]=H[c]
# onderrand: ijzer met lucht of groen eronder -> zwart (schaduwkant)
b=a.copy()
for y in range(Y0,Y1+1):
    for x in range(0,23):
        if b[y,x] in IJZER and (y==63 or b[y+1,x] not in IJZER): a[y,x]=1
# linker buitenrand: lucht links -> selout C
for y in range(Y0,Y1+1):
    for x in range(0,23):
        if b[y,x] in IJZER and (x==0 or b[y,x-1]==0) and a[y,x]!=1: a[y,x]=12
o=Image.fromarray(a.astype('uint8'),'P'); o.putpalette(pal); o.save(OUT,transparency=0)
for y in range(46,62): print('%2d '%y+''.join('.' if v==0 else '%X'%v for v in a[y,:26]), '  r4: '+''.join('.' if v==0 else '%X'%v for v in r4[y,:26]))
