from PIL import Image; import numpy as np
g=np.asarray(Image.open('grid128.png')).astype(int)
bg=(g.min(2)>238)&(np.ptp(g,2)<14)
px=g[~bg].astype('uint8').reshape(1,-1,3)
q=Image.fromarray(px).quantize(colors=15,method=Image.Quantize.MEDIANCUT,kmeans=5)
pal=np.array(q.getpalette()[:45]).reshape(15,3)
d=((g[:,:,None,:]-pal[None,None])**2).sum(3); idx=d.argmin(2); idx[bg]=-1
for k,c in enumerate(pal): print(k,c,(idx==k).sum())
np.save('idx128.npy',idx); np.save('pal.npy',pal)
out=np.full((128,128,3),255); m=idx>=0; out[m]=pal[idx[m]]
Image.fromarray(out.astype('uint8')).resize((768,768),Image.NEAREST).save('q128_6x.png')
