# Spleet tussen de benen S natieve rijen hoger: rijen 62-64 (kreuk + kap) kols 46-60 schuiven S omhoog,
# rijen 65-S..64 krijgen modelrij 65 (binnenranden benen + gat). Niets getekend: alles gekopieerd uit het model.
import sys; from PIL import Image; import numpy as np
S=int(sys.argv[1]) if len(sys.argv)>1 else 6
src=np.asarray(Image.open('n_model.png')).copy(); a=src.copy()
C=slice(46,61)
for r in (62,63,64): a[r-S,C]=src[r,C]
for r in range(65-S,65): a[r,C]=src[65,C]
Image.fromarray(a).save('n_edit.png')
d=np.abs(a.astype(int)-src.astype(int)).sum(2)>0
ys,xs=np.where(d); print('S',S,'gewijzigde natieve pixels',d.sum(),'zone rijen',ys.min(),ys.max(),'kols',xs.min(),xs.max())
m=np.zeros_like(d); m[62-S:65,46:61]=True; print('diff buiten zone:',(d&~m).sum())
