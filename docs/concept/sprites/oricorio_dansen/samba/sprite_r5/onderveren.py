# onderveren.py: onderste rechterveren (rij 45-50, kol 44-51): het blauwe rechthoekblok (rechte rand x50 rij 46-49,
# rechte onderrand rij 50 x44-49) wordt twee spitse veerpunten met een inkeping ertussen, zoals de puntjes in het model.
import numpy as np, sys
from render import lees
H='.123456789abcdef'
def zet(a,y,x0,s):
    for i,c in enumerate(s):
        if c!=' ': a[y,x0+i]=H.index(c)
E=[
 (46,48,'aa1.'),
 (47,47,'991.'),
 (48,49,'a1'),
 (49,46,'aaa1.'),
 (50,44,'.1111.'),
]
def pas(a):
    for y,x,s in E: zet(a,y,x,s)
    return a
if __name__=='__main__':
    a=lees(sys.argv[1]); o=pas(a.copy()); np.save(sys.argv[2],o)
    for y in range(42,52): print('%02d '%y+''.join(H[v] for v in o[y,36:54]))
