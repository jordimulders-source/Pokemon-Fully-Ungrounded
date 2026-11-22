# lijf.py: borstband (rij 34-38) en heupband (rij 42-44) effen met volume:
# twee lobben bovenaan, bolle onderrand (laagste punt midden, zoals het model), licht linksboven, schaduwsikkel rechtsonder;
# geen horizontale banden (r4: hele rij 6 boven, hele rij 7 onder).
import numpy as np, sys
from render import lees
H='.123456789abcdef'
def zet(a,y,x0,s):
    for i,c in enumerate(s):
        if c!=' ': a[y,x0+i]=H.index(c)
E=[
 (34,25,'8666733667771'),
 (35,24,'86666667666781'),
 (36,24,'86666677777881'),
 (37,24,'58777777777841'),
 (38,25,'5387777883441'),
 (42,33,'86667'),
 (43,26,'5666666666777853'),
 (44,26,'1667777777777853'),
]
def pas(a):
    for y,x,s in E: zet(a,y,x,s)
    return a
if __name__=='__main__':
    a=lees(sys.argv[1]); o=pas(a.copy()); np.save(sys.argv[2],o)
    print('   '+''.join(str(x%10) for x in range(20,45)))
    for y in range(32,47): print('%02d '%y+''.join(H[v] for v in o[y,20:45]))
