# rvleugel.py: rechtervleugel: de bovenste veervingers F1 (x48-51) en F2 (x52-55) waren rechte verticale stokken
# (zwarte rand x51 rij 13-20, x55 rij 16-22); top 1 px naar rechts laten buigen zodat elke vinger een boog '(' vormt
# (boven naar rechts, midden recht, onder schuin naar links), zoals de gebogen vingers in het model.
import numpy as np, sys
from render import lees
H='.123456789abcdef'
def zet(a,y,x0,s):
    for i,c in enumerate(s):
        if c!=' ': a[y,x0+i]=H.index(c)
E=[
 (13,48,'..441'),
 (14,48,'.4231'),
 (15,48,'.4231'),
 (16,48,'4231.441'),     # F1 rij 16 gelijk; F2-punt 1 px naar rechts
 (17,52,'.4231'),
 (18,52,'22341'),
]
def pas(a):
    for y,x,s in E: zet(a,y,x,s)
    return a
if __name__=='__main__':
    a=lees(sys.argv[1]); o=pas(a.copy()); np.save(sys.argv[2],o)
    for y in range(10,26): print('%02d '%y+''.join(H[v] for v in o[y,40:60]))
