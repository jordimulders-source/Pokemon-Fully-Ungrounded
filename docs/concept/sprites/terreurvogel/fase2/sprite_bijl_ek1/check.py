# bevroren-checks ek1 t.o.v. r4: silhouet, oog B (r4 en r2/oog_B.png), palet
import numpy as np; from PIL import Image
r4i=Image.open('../sprite_bijl_r4/terreurvogel_bijl_r4.png'); eki=Image.open('terreurvogel_ek1.png')
r4=np.array(r4i).astype(int); ek=np.array(eki).astype(int)
print('alpha-diff (silhouet):',int(((r4>0)!=(ek>0)).sum()))
OOG=[(29,17),(29,18),(30,14),(30,15),(30,16),(30,17),(30,18),(31,15),(31,16),(31,17),(31,18),(32,16),(32,17)]
print('oog index-diff:',sum(r4[p]!=ek[p] for p in OOG))
print('palet gelijk:',r4i.getpalette()[:48]==eki.getpalette()[:48])
ob=np.array(Image.open('../sprite_bijl_r2/oog_B.png').convert('RGB')).astype(int); er=np.array(eki.convert('RGB')).astype(int)
if ob.shape==er.shape: print('oog RGB-diff t.o.v. r2/oog_B.png:',sum(int((ob[p]!=er[p]).any()) for p in OOG))
else: print('oog_B.png formaat',ob.shape)
d=np.argwhere(r4!=ek); print('pixels gewijzigd:',len(d))
print('gewijzigde pixels die zwart(1) of buitenrand waren:',sum(r4[tuple(p)]==1 for p in d))
