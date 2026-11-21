# lvleugel.py: linkervleugel (rij 37-49, kol 5-25): zwarte binnenlijnen (rij 42 x11-13, rij 45 x11-14, x16 r47, x15 r48)
# en de verticale lijnen x15 (rij 39-41) en x14 (rij 42-44) weg of naar donkergroen; bovenrand één vloeiende boog (inkeping x11-14 weg) die naar het lijf toe stijgt zoals het model.
import numpy as np, sys
from render import lees
H='.123456789abcdef'
def zet(a,y,x0,s):
    for i,c in enumerate(s):
        if c!=' ': a[y,x0+i]=H.index(c)
E=[
 (36,17,'44444'),
 (37,11,'44444422233 3'),
 (38,7,'4444222222233333 345'),
 (39,6,'122222222233333444445'),
 (40,7,'1222223333344444445'),
 (41,8,'1133334444444444455'),
 (42,9,'45544337666688667'),
 (43,8,'42222237666686674'),
 (44,8,'1222333476666877'),
 (45,9,'1154444444'),
 (46,11,'5222242'),
 (47,11,'4222259'),
 (48,11,'13335'),
 (49,15,'.'),
]
def pas(a):
    for y,x,s in E: zet(a,y,x,s)
    return a
if __name__=='__main__':
    a=lees(sys.argv[1]); o=pas(a.copy()); np.save(sys.argv[2],o)
    print('   '+''.join(str(x%10) for x in range(4,28)))
    for y in range(34,51): print('%02d '%y+''.join(H[v] for v in o[y,4:28]))
