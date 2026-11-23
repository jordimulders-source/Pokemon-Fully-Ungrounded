# Controle r11: tintvlekjes < 3 px (8-samenhangend: een schuine lijn telt als één vorm) en tinten per vlak.
# Gebruik: cd pinsir_evo && python3 sprite_r11/controle.py
import sys, importlib.util, numpy as np
from scipy import ndimage
sys.argv=['x']
spec=importlib.util.spec_from_file_location('b','sprite_r11/bouw.py'); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
def vlekjes(q,mask):
    out=[]
    for t in sorted(set(q[mask].ravel())-{0,b.C['K']}):
        lb,n=ndimage.label((q==t)&mask,structure=np.ones((3,3)))
        for k in range(1,n+1):
            m=lb==k
            if m.sum()<3: ys,xs=np.where(m); out.append((b.CH[t],[(int(x),int(y)) for y,x in zip(ys,xs)]))
    return out
R10=b.R10
for v in 'AB':
    q,info=b.bouw(v)
    for naam,mask in (('kop',b.ZONE&~b.GZ),('schild+rechts',b.SH|b.RZ|b.DOORN|b.OMTREK_S)):
        o=vlekjes(q,mask); o10=vlekjes(R10,mask)
        tints=sorted(set(b.CH[t] for t in q[mask&(q>0)].ravel()))
        print('%s %-14s tinten %-28s vlekjes<3: r11 %2d (r10 %2d)'%(v,naam,''.join(tints),len(o),len(o10)))
        for x in o: print('      ',x)
