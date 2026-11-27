# Schrijft pachamama_r2.png uit gezicht2.npy (kap.py -> gezicht2.py) en telt de afwijking t.o.v. r1.
import sys; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image
o=np.load('gezicht2.npy'); r1=np.asarray(Image.open('../r1/pachamama_r1.png')).astype(int)
assert ((o>0)==(r1>0)).all(), 'silhouet gewijzigd'
d=o!=r1; print('afwijkend t.o.v. r1:',int(d.sum()),'| buiten r9-28/c17-44:',int(d[:9].sum()+d[29:].sum()+d[:,:17].sum()+d[:,45:].sum()))
print('kleuren',len(set(o.ravel()))-1)
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-48)); p.save('pachamama_r2.png',transparency=0)
