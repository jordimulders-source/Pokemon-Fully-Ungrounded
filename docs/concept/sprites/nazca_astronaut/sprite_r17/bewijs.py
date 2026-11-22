# Bewijs r17: t.o.v. r16-a_L1: alpha 0, kop (rij 0-25) 0, alles buiten de lichaamszone en haar buitenlijn 0.
# alles buiten de lichaamszone (tuniek) en haar buitenlijn 0 (= onderarmen, onderbenen, strepen).
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite_r9'); from gen import stuk
def rgba(f): return np.asarray(Image.open(f).convert('RGBA')).astype(int)
r13=rgba('../sprite_r16/astro_a_L1.png')   # referentie hier: r16-a_L1
zone=stuk!=''
rand=np.array([[not zone[j,i] and any(zone[min(j+p,63),min(i+q,63)] for p,q in ((0,1),(1,0),(0,-1),(-1,0))) for i in range(64)] for j in range(64)])
borst=np.zeros((64,64),bool); borst[26:33]=(stuk[26:33]=='RO')
for v in ('L1',):
    f='astro_a_%s.png'%v; x=rgba(f); d=np.abs(x-r13).sum(-1)>0
    print('%s: %d kleuren | alpha %d | kop %d | buiten lichaamszone+rand %d | zone gewijzigd %d | buitenlijn gewijzigd %d'%(
        f,len(set(np.asarray(Image.open(f)).ravel())),((x[...,3]>0)!=(r13[...,3]>0)).sum(),d[:26].sum(),(d&~zone&~rand).sum(),(d&zone).sum(),(d&rand).sum()))
