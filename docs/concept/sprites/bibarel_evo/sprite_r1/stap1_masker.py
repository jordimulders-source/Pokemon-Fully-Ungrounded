# Stap 1: masker van het werkmodel (achtergrond = bijna-wit verbonden met de rand; witte tanden/ogen/staartbanden binnenin blijven figuur)
# en k-means van de modelkleuren, om de kleurgroepen te zien. Niets hertekend.
import numpy as np; from PIL import Image; from scipy import ndimage
from scipy.cluster.vq import kmeans2
a=np.asarray(Image.open('model/r10_k8.png').convert('RGB')).astype(float)
light=a.min(2)>=215
lab,n=ndimage.label(light)
rand=set(lab[0])|set(lab[-1])|set(lab[:,0])|set(lab[:,-1]); rand.discard(0)
bg=np.isin(lab,list(rand))
fig=~bg
np.save('sprite_r1/masker.npy',fig)
yy,xx=np.where(fig); print('figuur',xx.min(),xx.max(),yy.min(),yy.max(),xx.max()-xx.min()+1,yy.max()-yy.min()+1)
np.random.seed(1)
P=a[fig]
c,l=kmeans2(P,18,minit='++',seed=1)
for i in np.argsort(c.sum(1)):
    print(i,c[i].astype(int),(l==i).sum())
np.save('sprite_r1/km.npy',c)
