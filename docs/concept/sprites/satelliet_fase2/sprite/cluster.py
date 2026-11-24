# Tintvlakjes < 3 px (4-samenhangend) per klasse, lijnklassen 1/11/15 uitgezonderd
import numpy as np, sys; from PIL import Image
from scipy import ndimage as nd
o=np.array(Image.open(sys.argv[1]))
uit=[]
for v in sorted(set(o.ravel())-{0,1,11,15}):
    lab,n=nd.label(o==v)
    for c in range(1,n+1):
        ys,xs=np.where(lab==c)
        if len(ys)<3: uit.append((int(v),[(int(x),int(y)) for x,y in zip(xs,ys)]))
print(len(uit)); [print(u) for u in uit]
print('gebruik per klasse',{int(v):int((o==v).sum()) for v in sorted(set(o.ravel()))})
