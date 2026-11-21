# romp.py: rechterrand lijf/kop x37 (r4: zwarte verticale lijn rij 27-38) wordt een bolle binnenlijn in donkergroen 5
# waar de vleugel erachter ligt (zwart alleen waar de rand tegen de achtergrond ligt), met een lichte bolling naar x38 (rij 32-35).
import numpy as np, sys
from render import lees
H='.123456789abcdef'
def zet(a,y,x0,s):
    for i,c in enumerate(s):
        if c!=' ': a[y,x0+i]=H.index(c)
E=[
 (30,37,'5'),
 (31,37,'5'),
 (31,41,'3'),            # lichte streep (rest van r4-veerstrepen) in de schouder weg
 (32,37,'45'), (32,40,'3'),
 (33,36,'445'),
 (34,37,'85'),
 (35,37,'85'),
 (36,37,'5'),
 (37,37,'5'),
 (38,37,'5'),
]
def pas(a):
    for y,x,s in E: zet(a,y,x,s)
    return a
if __name__=='__main__':
    a=lees(sys.argv[1]); o=pas(a.copy()); np.save(sys.argv[2],o)
    for y in range(26,42): print('%02d '%y+''.join(H[v] for v in o[y,30:46]))
