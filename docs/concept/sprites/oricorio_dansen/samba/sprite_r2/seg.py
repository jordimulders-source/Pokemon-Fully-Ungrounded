# Natief model opdelen in vlakken: samenhangende stukken zonder lijn (zwart O of donkergroene lijn L) -> seg.npy
import numpy as np; from PIL import Image
from scipy import ndimage as nd
from palet import KM, I
lab=np.load('km_lab.npy'); cl=np.zeros(lab.shape,int)
for k,v in KM.items(): cl[lab==k]=I[v]
fill=(cl>0)&~np.isin(cl,[I['O'],I['L']])
seg,n=nd.label(fill)
sz=nd.sum(np.ones_like(seg),seg,range(1,n+1))
print(n,'vlakken; >=12 px:',(sz>=12).sum())
np.save('seg.npy',seg); np.save('cl.npy',cl)
rng=np.random.default_rng(3); col=rng.integers(60,255,(n+1,3)); col[0]=255
im=col[seg].astype('uint8'); im[np.isin(cl,[I['O'],I['L']])]=0
Image.fromarray(im[12:122,66:181]).resize((115*7,110*7),Image.NEAREST).save('/tmp/claude-0/seg.png')
