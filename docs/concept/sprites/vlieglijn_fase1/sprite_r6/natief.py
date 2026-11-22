# r9 (1024^2, raster 16 px, offset 0) -> natief 64x64: mediaan van het midden van elke cel,
# dan dichtstbijzijnde kleur uit het r5-palet (wit/lichte achtergrond -> 0)
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../gemini/r9.png').convert('RGB')).astype(float)
pal=[tuple(map(int,l.split())) for l in open('normal.pal').read().split('\n')[3:19]]
P=np.array(pal,float)
nat=np.zeros((64,64,3)); idx=np.zeros((64,64),int); spread=np.zeros((64,64))
for y in range(64):
  for x in range(64):
    c=a[y*16+4:y*16+12,x*16+4:x*16+12].reshape(-1,3)
    m=np.median(c,0); nat[y,x]=m; spread[y,x]=np.abs(c-m).sum(1).mean()
    if m.min()>238: idx[y,x]=0; continue
    d=((P[1:]-m)**2).sum(1); idx[y,x]=1+int(d.argmin())
np.savetxt('r9_nat_idx.txt',idx,fmt='%2d')
Image.fromarray(nat.astype(np.uint8)).save('r9_natief.png')
print('cellen met veel spreiding (>25):',int((spread>25).sum()))
