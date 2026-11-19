# check.py png [ymin]: losse pixels = kleurcluster van 1 px (8-buren), per index; vanaf ymin
import sys,numpy as np; from PIL import Image
from scipy import ndimage
a=np.array(Image.open(sys.argv[1])); ymin=int(sys.argv[2]) if len(sys.argv)>2 else 0
for v in range(1,16):
    lab,n=ndimage.label(a==v,structure=np.ones((3,3)))
    for k in range(1,n+1):
        ys,xs=np.nonzero(lab==k)
        if len(ys)==1 and ys[0]>=ymin: print('los',v,(int(xs[0]),int(ys[0])))
