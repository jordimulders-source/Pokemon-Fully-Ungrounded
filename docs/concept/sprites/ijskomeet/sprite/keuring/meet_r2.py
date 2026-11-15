# Keurder r2: silhouet-overlap sprite vs model64, zwart-percentages vs Gen 3, tintstappen
from PIL import Image; import numpy as np, sys
from collections import Counter
S='../'; G='../../../../../../graphics/pokemon/'
spr=np.array(Image.open(S+'r2.png').convert('RGBA')).astype(int)
mod=np.array(Image.open(S+'model64.png').convert('RGB')).astype(int)
sa=spr[...,3]>0
ma=(mod.min(2)<235)   # niet-wit = model
L=lambda c:0.299*c[...,0]+0.587*c[...,1]+0.114*c[...,2]
print('sprite px',sa.sum(),'model px (niet-wit<235)',ma.sum(),'overlap',(sa&ma).sum(),'alleen sprite',(sa&~ma).sum(),'alleen model',(ma&~sa).sum())
ys,xs=np.where(sa); print('sprite bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max())
ys,xs=np.where(ma); print('model bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max())
# model zonder de vage nevel: alleen echt gekleurd
md=(L(mod)<200)
print('model donker/ijs (L<200)',md.sum(),'waarvan buiten sprite',(md&~sa).sum())
yy,xx=np.where(md&~sa); print(' buiten-sprite modelpixels:',list(zip(xx.tolist(),yy.tolist()))[:60])
def stats(name,a):
    a=a.astype(int); op=a[...,3]>0 if a.shape[2]==4 else None
    l=L(a); n=op.sum()
    print(f'{name:10s} opaak {n:4d}  L<40: {100*((l<40)&op).sum()/n:4.1f}%  L<70: {100*((l<70)&op).sum()/n:4.1f}%  kleuren {len(set(map(tuple,a[op][:,:3])))}')
stats('r2',spr)
for s in ['lunatone','solrock','glalie','regice','metagross','snorunt']:
    im=Image.open(G+s+'/anim_front_gba.png'); im=im.convert('RGBA'); a=np.array(im)[:64]
    # transparant = paletkleur 0 -> neem pixel (0,0)
    bg=a[0,0,:3]; a[...,3]=np.where((a[...,:3]==bg).all(2),0,255)
    stats(s,a)
