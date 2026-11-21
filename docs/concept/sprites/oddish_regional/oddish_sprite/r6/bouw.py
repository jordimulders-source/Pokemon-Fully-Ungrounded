# r6 = r5 + subtiele golvende rand op het middelste blad (C), Jordi: "kan je het middelste blad ook nog doen?"
import numpy as np; from PIL import Image
im=Image.open('r5/oddish_r5.png'); o=np.asarray(im).astype(int).copy(); oud=o.copy(); pal=im.getpalette()
W={(17,35):(6,0),(17,36):(9,6),     # linkerrand: 1 px inham in de regelmatige trap
   (19,41):(1,0),(19,40):(8,1)}     # rechterrand (rechte zwarte rand x41, y18-21): 1 px inham
for (y,x),(a,b) in W.items():
    assert o[y,x]==a,(y,x,o[y,x]); o[y,x]=b
d=o!=oud; assert np.isin(oud[d],[0,1,6,7,8,9]).all() and d[29:].sum()==0
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal); p.save('r6/oddish_r6.png',transparency=0)
print('gewijzigd',d.sum())
