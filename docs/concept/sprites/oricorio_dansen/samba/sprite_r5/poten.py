# poten.py: opgetild been: de horizontale staaf (r4 rij 50 'dbbbbb1' tussen twee zwarte rijen) wordt een dun schuin
# Oricorio-been (donkerroze lichtkant | lichtroze | zwart schaduwkant, zoals Baile x30-32), knie naar voren (links);
# voet en tenen blijven de Baile-voet (r4 rij 52-55 = Baile rij 52-55 in samba-palet); standbeen + voet = Baile (ongewijzigd).
import numpy as np, sys
from render import lees
H='.123456789abcdef'
def zet(a,y,x0,s):
    for i,c in enumerate(s):
        if c!=' ': a[y,x0+i]=H.index(c)
E=[
 (49,28,'1'),
 (50,27,'.dbbb1..'),
 (51,25,'.dbb1....'),
]
def pas(a):
    for y,x,s in E: zet(a,y,x,s)
    return a
if __name__=='__main__':
    a=lees(sys.argv[1]); o=pas(a.copy()); np.save(sys.argv[2],o)
    for y in range(47,62): print('%02d '%y+''.join(H[v] for v in o[y,18:40]))
