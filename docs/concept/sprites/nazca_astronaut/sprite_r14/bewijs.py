# Bewijs r14: t.o.v. r13-P_rood: alpha 0, kop (rij 0-25) 0, romp + naden 0, alles buiten ledemaatstof en hun buitenlijn 0.
import numpy as np; from PIL import Image
from r14 import stuk, LEDE
def rgba(f): return np.asarray(Image.open(f).convert('RGBA')).astype(int)
r13=rgba('../sprite_r13/astro_P_rood.png')
rand=np.array([[not stuk[j,i] and any(LEDE[min(j+p,63),min(i+q,63)] for p,q in ((0,1),(1,0),(0,-1),(-1,0))) for i in range(64)] for j in range(64)])
for v in range(1,6):
    f='astro_S%d.png'%v; x=rgba(f); d=np.abs(x-r13).sum(-1)>0
    print('%s: %d kleuren | alpha %d | kop %d | romp+naden %d | buiten ledematen+rand %d | ledematen gewijzigd %d px'%(
        f,len(set(np.asarray(Image.open(f)).ravel())),((x[...,3]>0)!=(r13[...,3]>0)).sum(),d[:26].sum(),
        (d&(stuk=='RO')).sum()+(d&(stuk!='')&~LEDE&(stuk!='RO')).sum(),(d&~LEDE&~rand).sum(),(d&LEDE).sum()))
