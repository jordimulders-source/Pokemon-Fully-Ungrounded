# r2 = r1 + pixelwissels uit de keuring (x,y,van,naar); controleert oude waarden.
import numpy as np; from PIL import Image
W=[(16,30,1,5),(16,31,1,5),(16,32,1,5),(16,33,1,5),(16,37,1,5),  # selout lichtkant
   (19,27,8,7),(19,28,8,7),(21,26,7,8),(22,26,7,8),               # hooglicht van kelpschaduw af
   (42,30,14,12),                                                 # kelpspleet rechts
   (46,30,12,14),(43,29,14,13),(15,39,6,7)]                       # KAN
im=Image.open('r1/gloom_r1.png'); o=np.array(im)
for x,y,a,b in W:
    assert o[y,x]==a,(x,y,o[y,x],a); o[y,x]=b
p=Image.fromarray(o,'P'); p.putpalette(im.getpalette()); p.save('r2/gloom_r2.png',transparency=0)
print('ok',len(W))
