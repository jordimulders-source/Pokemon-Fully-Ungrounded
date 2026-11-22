# rand.py: open randen dicht (lichte kleur op de buitenrand, gevonden door check.py) en het opgetilde been als schuine
# 2-px band met donkerroze bovenrand en zwarte onderrand (Oricorio-opbouw).
import numpy as np, sys
from render import lees
H='.123456789abcdef'
def zet(a,y,x0,s):
    for i,c in enumerate(s):
        if c!=' ': a[y,x0+i]=H.index(c)
E=[
 (18,52,'4'),            # F2-rand naast F1
 (30,40,'4'),            # bovenrand schouder rechtervleugel
 (44,47,'11'),           # bovenrand blauwe veerpunt
 (47,38,'1'),            # onderkant franjeveertje
 (50,27,'dbbb1.'),       # dij
 (51,25,'ddb111'),       # knie naar voren, zwarte onderrand
]
def pas(a):
    for y,x,s in E: zet(a,y,x,s)
    return a
if __name__=='__main__':
    a=lees(sys.argv[1]); o=pas(a.copy()); np.save(sys.argv[2],o)
    for y in range(47,57): print('%02d '%y+''.join(H[v] for v in o[y,20:40]))
