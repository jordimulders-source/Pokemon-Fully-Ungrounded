# python3 maker/naarpng.py raster.txt uit.png  -> geindexeerde PNG (index 0 transparant) + controles
import sys,numpy as np; sys.path.insert(0,'maker'); from pal import PAL
from PIL import Image
R=[l.rstrip('\n') for l in open(sys.argv[1])]
assert len(R)==64 and all(len(r)==64 for r in R), [len(r) for r in R]
keys=list(PAL); idx={k:i for i,k in enumerate(keys)}
a=np.array([[idx[c] for c in r] for r in R],'uint8')
im=Image.fromarray(a,'P'); pal=[]
for k in keys: pal+=list(PAL[k])
pal+= [0]*(768-len(pal)); im.putpalette(pal); im.save(sys.argv[2],transparency=0)
SIL=np.load('sil56_rond.npy'); diff=int(((a>0)!=SIL).sum())
print('silhouetdiff',diff,'kleuren gebruikt',len(np.unique(a)),'(incl. transparant)')
