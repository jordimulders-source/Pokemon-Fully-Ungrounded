# geel2.py: gerichte reparaties in de voorste gele tooibladen (rij 14-27) op r4-basis:
# platte bladtoppen spits, rechte onderrand als hangende bladranden, horizontale schaduwband rechts doorbroken.
import numpy as np, sys
H='.123456789abcdef'
def zet(a,y,x0,s):
    for i,c in enumerate(s):
        if c!=' ': a[y,x0+i]=H.index(c)
E=[ # (rij, x-start, tekens; spatie = laten)
 (15,23,'868 '),      # UL: platte top 8888 -> spits (punt rij 14 x23)
 (15,36,'4867'), (15,40,'8'),   # UR: platte top -> spits (punt rij 14 x39)
 (18,19,'4888'), (18,23,'6'),    # ML: bovenrand gebogen
 (19,19,'86'),
 (20,21,'7'),
 (21,21,'1'),
 # LL-onderrand hangend (was rechte zwarte rij 26 x21-25 + open gele pixel x18 rij 25)
 (25,17,'11777777'), (25,25,'77'),
 (26,19,'1177771'),
 (27,21,'1111'),
 # rechts: LR-bovenkant licht (doorbreekt band rij 21-23), onderkant schaduw, hangende rand
 (23,37,'866666'), 
 (25,36,'777777'),
 (26,37,'77771'),
 (27,37,'1111'),
]
def pas(a):
    for y,x,s in E: zet(a,y,x,s)
    return a
if __name__=='__main__':
    a=np.load(sys.argv[1]); o=pas(a.copy()); np.save(sys.argv[2],o)
    print('   '+''.join(str(x%10) for x in range(15,48)))
    for y in range(12,29): print('%02d '%y+''.join(H[v] for v in o[y,15:48]))
