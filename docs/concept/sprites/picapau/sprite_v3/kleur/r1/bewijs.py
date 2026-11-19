# Bewijs kleur r1: alpha-diff 0 t.o.v. r17, gewijzigde pixels per zone, alleen tintwissels binnen kleurgroepen.
from PIL import Image
import numpy as np
from collections import defaultdict
def rgba(f):
    p=Image.open(f); p.info['transparency']=0; return np.array(p.convert('RGBA')), np.array(p)
A,ia=rgba('../../r17/picapau.png'); B,ib=rgba('picapau.png')
print('alpha-diff:',int((A[...,3]!=B[...,3]).sum()))
print('palet gelijk aan r17:',Image.open('picapau.png').getpalette()[:48]==Image.open('../../r17/picapau.png').getpalette()[:48])
def g(v,y,x):
    if v in (2,3,4): return 'geel'
    if v in (7,8,9): return 'staart'
    if v==12: return 'vleugelbruin'
    if v==13: return 'D (lijn/vleugelschaduw)'
    if v==1: return 'zwart'
    return 'overig %d'%v
def zone(x,y):
    v=ia[y,x]
    if v in (7,8,9): return 'staart (tinten 7/8/9)'
    if v in (12,13) and ib[y,x]==12: return 'vleugel (D->C binnen vleugelbruin)'
    if v==13 and ib[y,x]==1: return 'buitenlijn (losse D in zwarte rand -> zwart)'
    if y<=21: return 'oren (geel 2/3/4)'
    if y<=38: return 'kop (geel 2/3/4)'
    return 'lijf (geel 2/3/4)'
d=defaultdict(list)
for y,x in np.argwhere(ia!=ib):
    d[zone(x,y)].append((int(x),int(y),'%X>%X'%(ia[y,x],ib[y,x])))
for z,l in d.items():
    print(z,len(l)); print('   ',' '.join('(%d,%d)%s'%t for t in l))
# soorten wissels
from collections import Counter
print(Counter('%X>%X'%(ia[y,x],ib[y,x]) for y,x in np.argwhere(ia!=ib)))
