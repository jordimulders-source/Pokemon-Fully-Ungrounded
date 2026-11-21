# tango_kls.npy -> tango_A/B/C.png (64x64 geïndexeerd, index 0 transparant). Varianten verschillen alleen in het rood (zones in rood.py).
import numpy as np; from PIL import Image; from palet import pal, NAMEN2
from rood import varianten
full={}
for v,o in varianten().items():
    ys,xs=np.where(o>0); crop=o[ys.min():ys.max()+1,xs.min():xs.max()+1]; h,w=crop.shape
    f=np.zeros((64,64),'uint8'); y0=61-h+1; x0=(64-w)//2; f[y0:y0+h,x0:x0+w]=crop
    im=Image.fromarray(f,'P'); fl=[c for t in pal() for c in t]; im.putpalette(fl+[0]*(768-len(fl))); im.save('tango_%s.png'%v,transparency=0)
    full[v]=f; print(v,'bbox',w,h,'rij',y0,'-',y0+h-1,'kol',x0,'kleuren',len(set(f.ravel()))-1)
import shutil; shutil.copy('tango_B.png','tango_r3.png')
