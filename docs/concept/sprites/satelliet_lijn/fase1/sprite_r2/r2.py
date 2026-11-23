# r2: keurdersreparaties (keuring_r1/KEURING.md, lijst uit keuring_r1/voorstel.py) op r1 -> sprite_r2/sprite.png
import numpy as np
from PIL import Image
r1=np.load('sprite_r1/sprite.npy'); s=r1.copy()
E=[ # (rij,kol,oud,nieuw,code)
 (22,5,2,0,'R1'),(24,4,2,0,'R1'),(24,5,6,2,'R1'),(25,3,2,0,'R1'),(25,4,6,2,'R1'),(26,3,2,0,'R1'),(26,4,6,2,'R1'),
 (48,9,0,1,'R2'),(47,9,1,8,'R2'),
 (29,38,0,1,'R3'),(29,37,1,8,'R3'),
 (22,22,5,6,'T1'),(18,20,5,6,'T1'),(19,21,5,6,'T1'),(24,21,5,6,'T1'),
 (26,12,6,5,'T2'),(27,14,6,5,'T2'),(26,7,5,6,'T2'),(36,37,7,8,'T2'),(25,36,7,8,'T2'),(26,36,7,8,'T2'),(41,6,4,3,'T2'),
 (12,23,3,2,'T3'),
]
for y,x,o,n,c in E:
    assert s[y,x]==o,(y,x,s[y,x],o); s[y,x]=n
mask=np.zeros_like(s,bool)
for y,x,*_ in E: mask[y,x]=True
print('diff r1->r2:',int((s!=r1).sum()),'| diff buiten reparatiepixels:',int(((s!=r1)&~mask).sum()))
np.save('sprite_r2/sprite.npy',s)
PAL=[(152,208,160),(24,20,32),(84,46,108),(118,70,150),(168,118,202),(255,255,255),(226,220,244),(184,174,226),(140,126,194),(56,128,140),(140,204,200)]
p=Image.fromarray(s.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(48-len(pal))); p.save('sprite_r2/sprite.png',transparency=0,bits=4)
print('kleuren',len(set(s.ravel()))-1)
