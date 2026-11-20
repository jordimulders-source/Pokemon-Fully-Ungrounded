# r2: spleet S natieve rijen hoger dan in het model. Alleen de kolommen van de spleetconstructie (49-55) worden verplaatst:
# rijen 62-64 (kreuk + kap) S omhoog, rijen 65-S..64 = modelrij 65 (binnenranden benen + gat). Niets getekend.
import sys; from PIL import Image; import numpy as np
S=int(sys.argv[1]); UIT=sys.argv[2] if len(sys.argv)>2 else 'n_edit.png'
src=np.asarray(Image.open('n_model.png')).copy(); a=src.copy()
C=slice(49,56)
for r in (62,63,64): a[r-S,C]=src[r,C]
for r in range(65-S,65): a[r,C]=src[65,C]
Image.fromarray(a).save(UIT)
d=np.abs(a.astype(int)-src.astype(int)).sum(2)>0; ys,xs=np.where(d)
m=np.zeros_like(d); m[62-S:65,49:56]=True
print('S',S,'natief gewijzigd',d.sum(),'rijen %d-%d kols %d-%d'%(ys.min(),ys.max(),xs.min(),xs.max()),'diff buiten zone',(d&~m).sum())
