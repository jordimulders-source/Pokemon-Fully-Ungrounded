import numpy as np; from PIL import Image; from palet import pal
from rood import varianten
o=varianten()['B']; ys,xs=np.where(o>0); crop=o[ys.min():ys.max()+1,xs.min():xs.max()+1]; h,w=crop.shape
f=np.zeros((64,64),'uint8'); y0=61-h+1; x0=(64-w)//2; f[y0:y0+h,x0:x0+w]=crop
im=Image.fromarray(f,'P'); fl=[c for t in pal() for c in t]; im.putpalette(fl+[0]*(768-len(fl))); im.save('tango_r4.png',transparency=0)
print('bbox',w,h,'rij',y0,'-',y0+h-1,'kleuren',len(set(f.ravel()))-1)
