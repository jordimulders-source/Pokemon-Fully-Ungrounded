# Keurder r3: kleuren op de buitenrand + kleine clusters (<3 px) per index
import numpy as np; from PIL import Image; from collections import Counter
from scipy import ndimage
a=np.asarray(Image.open('../r3.png'))
o=a>0; pad=np.pad(o,1); rand=o & ~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
print('buitenrand per index:',sorted(Counter(a[rand]).items()))
for i in range(1,16):
    lab,n=ndimage.label(a==i); s=ndimage.sum(np.ones_like(a),lab,range(1,n+1))
    k=[(int(ndimage.center_of_mass(a==i,lab,j+1)[1]),int(ndimage.center_of_mass(a==i,lab,j+1)[0])) for j,v in enumerate(s) if v<3]
    if k: print(i,'clusters<3:',len(k),k[:12])
