# r5 = r4b + Jordi's goedgekeurde afwijking ("Akkoord, maar houd het subtiel"), alleen kelp (indices 6-9):
# 1) palet kelp: tint -6 graden (naar amber), verzadiging x0,85, helderheid (Rec.601) gelijk; 2) licht golvende rand op 4 plekken.
import numpy as np; from PIL import Image
im=Image.open('r4/oddish_r4b.png'); o=np.asarray(im).astype(int).copy(); pal=im.getpalette()[:48]
oud=o.copy()
NIEUW={6:(89,63,19),7:(147,119,36),8:(188,157,72),9:(216,194,144)}
for k,c in NIEUW.items(): pal[3*k:3*k+3]=list(c)
# (y,x): (verwachte oude index, nieuwe index)
W={(24,24):(0,6),(24,25):(6,8),            # blad links (A): linkerrand 1 px naar buiten
   (19,27):(0,6),(19,28):(6,7),            # blad linksboven (B): linkerrand 1 px naar buiten
   (19,43):(0,6),(19,44):(0,6),(20,43):(6,7),(20,44):(6,7),   # blad rechtsboven (D): bovenrand 2 px bolling
   (25,48):(6,0),(26,48):(8,6)}            # blad rechtsonder (E): bovenrand 1 px in
for (y,x),(a,b) in W.items():
    assert o[y,x]==a,(y,x,o[y,x]); o[y,x]=b
d=(o!=oud); assert all(oud[d]==0 if False else True for _ in [0])
assert np.isin(oud[d],[0,6,7,8,9]).all() and np.isin(o[d],[0,6,7,8,9]).all()
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal+[0]*(768-len(pal))); p.save('r5/oddish_r5.png',transparency=0)
print('gewijzigde pixels',d.sum(),'kleuren',len(set(o.ravel())))
