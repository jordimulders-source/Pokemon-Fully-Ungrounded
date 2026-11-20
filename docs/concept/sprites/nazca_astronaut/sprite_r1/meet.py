# Bewijs + tellingen: (1) spleetbewerking natief diff 0 buiten zone, (2) kale reductie model vs bewerkt alleen in spleetzone,
# (3) afwijking eindsprite t.o.v. kale reductie per zone (vorm/klasse; tint telt niet), (4) spleetbovenkant r9/r10/doel/resultaat
import numpy as np; from PIL import Image
from reduceer import reduceer
a=np.asarray(Image.open('n_model.png')).astype(int); b=np.asarray(Image.open('n_edit.png')).astype(int)
d=np.abs(a-b).sum(2)>0; ys,xs=np.where(d)
print('(1) natief gewijzigd:',d.sum(),'px, rijen %d-%d kols %d-%d'%(ys.min(),ys.max(),xs.min(),xs.max()))
km=reduceer('n_model.png',0,0.5); ke=reduceer('n_edit.png',0,0.5)
d2=km!=ke; ys,xs=np.where(d2); print('(2) kale reductie model vs bewerkt:',d2.sum(),'px, rijen %d-%d kols %d-%d'%(ys.min(),ys.max(),xs.min(),xs.max()))
kaal=np.load('kaal.npy'); s=np.load('schoon.npy')
eq=lambda c:{'k':'K','o':'K'}.get(c,c)
E=np.vectorize(eq)
sil=(kaal=='.')!=(s=='.'); kl=(E(kaal)!=E(s))&~sil
Z={'kop+ogen':(0,20),'romp/armen':(20,48),'benen/voeten':(48,58)}
for n,(r0,r1) in Z.items(): print('(3)',n,'silhouet',sil[r0:r1].sum(),'klasse',kl[r0:r1].sum())
def top(g):
    for j in range(25,g.shape[0]):
        r=''.join(g[j,14:19]).strip()
        if '.' in r: return j
for n in ('n_r9.png','n_r10.png','n_edit.png'): print('(4)',n,'eerste spleetrij (sprite):',top(reduceer(n,0,0.5)))
