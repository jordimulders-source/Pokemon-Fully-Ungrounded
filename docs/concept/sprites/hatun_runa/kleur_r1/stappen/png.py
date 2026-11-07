# png.py raster.txt normal.pal out.png : tekstraster -> geindexeerde png (index 0 transparant) + controle silhouet
import sys
from tl import *
R=raster(sys.argv[1]); p=pal(sys.argv[2])
a=np.zeros((64,64),'uint8')
for y,l in enumerate(R):
  for x,ch in enumerate(l): a[y,x]=0 if ch=='.' else int(ch,16)
im=Image.fromarray(a,'P'); im.putpalette([v for c in p for v in c]); im.info['transparency']=0
im.save(sys.argv[3],transparency=0)
m=a>0
print('px',m.sum(),'erbij',list(zip(*np.where(m&~SIL)))[:20],'eraf',list(zip(*np.where(~m&SIL)))[:20],'kleuren',sorted(set(a[m].tolist())))
