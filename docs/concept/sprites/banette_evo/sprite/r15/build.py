# r15 = r14 + drie punten van Jordi (18 nov). Draaien vanuit deze map: python3 build.py
# 1 linkeroor: buitenlijn met bolling (x7,x6,x7) en binnenlijn als diagonaal naar de punt (13>12>11>10>9)
# 2 linker-Shuppet (met draden langer) 2 px omlaag: 2 px lucht tussen bel en hoorn
# 3 schaduw oor: randlicht 3 links, hooglicht 2 onder het kruis, sikkel 4 aan de gezichtskant/punt
from PIL import Image; import numpy as np
src=Image.open('../r14/banette_evo.png'); pal=src.getpalette(); A0=np.array(src); a=A0.copy()
zone={}
def put(x,y,v,z):
    a[y,x]=v; zone.setdefault(z,set()).add((x,y))
# --- 1+3 oor. rij: (buitenlijn-x, tinten van de vulling, binnenlijn-x)
ROWS={25:(None,[3,4,4],13),            # vulling x10-12 (x9 = onderrand kruis)
      26:(7,[2,2,3,4,4],13),
      27:(7,[2,3,3,4,4],13),
      28:(6,[3,3,3,4,4],12),
      29:(6,[3,3,4,4],11),
      30:(6,[3,4,4],10),
      31:(7,[4],9),
      32:(7,[4],9)}
for y,(o,t,i) in ROWS.items():
    x0=10 if o is None else o+1
    if o is not None: put(o,y,1,'oor')
    for k,v in enumerate(t): put(x0+k,y,v,'oor')
    put(i,y,1,'oor')
put(12,29,0,'oor')                      # V-begin van de spleet oor/gezicht (was dubbele lijn)
for y in range(18,25):                   # bovenste strook naast het kruis: randlicht x11, rest 4
    w=4 if y in (20,21,22) else 3
    for k in range(w): put(11+k,y,3 if k==0 else 4,'oor')
# --- 2 linker-Shuppet 2 px omlaag
box=A0[39:57,4:16]; m=(box!=0)&(box!=13)
for (j,i) in zip(*np.nonzero(m)): put(4+i,39+j,0,'shuppet')
for (j,i) in zip(*np.nonzero(m)): put(4+i,41+j,int(box[j,i]),'shuppet')
for c in (4,11,13):                      # elke draad precies 2 px langer (1 px breed)
    y=max(y for y in range(30,45) if A0[y,c]==13)
    for k in (1,2):
        assert a[y+k,c]==0; put(c,y+k,13,'shuppet')
out=Image.fromarray(a.astype('uint8'),'P'); out.putpalette(pal); out.save('banette_evo.png',transparency=0)
# --- bewijs
d=np.argwhere(a!=A0)
Z=set().union(*zone.values())
buiten=[(x,y) for y,x in d if (x,y) not in Z]
print('pixeldiff totaal',len(d),'| buiten de zones',len(buiten))
for z,s in zone.items(): print(' ',z,sum(1 for (x,y) in s if a[y,x]!=A0[y,x]),'px veranderd; bbox x%d-%d y%d-%d'%(min(p[0] for p in s),max(p[0] for p in s),min(p[1] for p in s),max(p[1] for p in s)))
