# Bewijs r13: alpha-diff t.o.v. r9, kop (rij 0-25) 0, alles buiten tuniek + tuniekrand 0.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite_r9'); from gen import stuk
def rgba(f): return np.asarray(Image.open(f).convert('RGBA')).astype(int)
r9=rgba('../sprite_r9/astro_V1.png'); a9=r9[...,3]>0
rand=np.array([[(not stuk[j,i]) and any(stuk[min(j+p,63),min(i+q,63)] for p,q in ((0,1),(1,0),(0,-1),(-1,0))) for i in range(64)] for j in range(64)])
for f in ['astro_P_rood.png']:
    if 1:
        x=rgba(f); ref=r9
        n=len(set(np.asarray(Image.open(f)).ravel()))
        alpha=(( x[...,3]>0)!=a9).sum(); kop=(np.abs(x[:26]-r9[:26]).sum(-1)>0).sum()
        buiten=((np.abs(x-ref).sum(-1)>0)&~(stuk!='')&~rand).sum()
        print('%s: %d kleuren | alpha-diff t.o.v. r9: %d | kop rij 0-25: %d | buiten tuniek+rand t.o.v. r9: %d'%(f,n,alpha,kop,buiten))
