# Natief model opdelen in veren: lijnmasker (O + donkergroene lijn L) 1 px verdikt om kleine gaten te dichten, dan samenhangende vlakken.
import numpy as np, sys; from PIL import Image, ImageDraw
from scipy import ndimage as nd
from palet import KM, I
lab=np.load('km_lab.npy'); cl=np.zeros(lab.shape,int)
for k,v in KM.items(): cl[lab==k]=I[v]
lijn=np.isin(cl,[I['O'],I['L']])
D=int(sys.argv[1]) if len(sys.argv)>1 else 1
lijn_d=nd.binary_dilation(lijn,iterations=D) if D else lijn
fill=(cl>0)&~lijn_d
seg,n=nd.label(fill)
sz=nd.sum(np.ones_like(seg),seg,range(1,n+1))
keep=[i+1 for i in range(n) if sz[i]>=15]; print(n,'vlakken; >=15 px:',len(keep))
np.save('seg.npy',seg); np.save('cl.npy',cl)
rng=np.random.default_rng(5); col=rng.integers(70,255,(n+1,3)); col[0]=255
im=col[seg].astype('uint8'); im[lijn]=0; im[(cl>0)&lijn_d&~lijn]=(120,120,120)
x0,y0=66,12; Z=7
big=Image.fromarray(im[y0:122,x0:181]).resize((115*Z,110*Z),Image.NEAREST); d=ImageDraw.Draw(big)
for i in keep:
    ys,xs=np.where(seg==i); d.text(((xs.mean()-x0)*Z-6,(ys.mean()-y0)*Z-5),str(i),fill='black')
big.save('/tmp/claude-0/seg.png')
