from PIL import Image; import numpy as np
from collections import Counter
g=np.asarray(Image.open('grid128.png')).astype(int)
P=np.array([(0,0,0),(24,16,40),(140,148,200),(116,122,178),(80,84,138),(56,52,96),(48,40,64),(214,162,190),(144,98,130),
 (240,246,250),(196,210,232),(184,192,224),(154,162,194),(110,116,150),(170,234,236),(44,138,150)])
bg=(g.min(2)>236)&(np.ptp(g,2)<16)
d=((g[:,:,None,:]-P[None,None,1:])**2).sum(3); idx=d.argmin(2)+1; idx[bg]=0
np.save('i128.npy',idx)
def save(ix,fn,s):
  out=np.full(ix.shape+(3,),255); m=ix>0; out[m]=P[ix[m]]
  Image.fromarray(out.astype('uint8')).resize((ix.shape[1]*s,ix.shape[0]*s),Image.NEAREST).save(fn)
save(idx,'p128_6x.png',6)
s=np.zeros((64,64),int)
for j in range(64):
  for i in range(64):
    b=idx[2*j:2*j+2,2*i:2*i+2].ravel()
    if (b>0).sum()<2: continue
    if (b==1).sum()>=2: s[j,i]=1; continue
    c=Counter(v for v in b if v>1)
    s[j,i]=c.most_common(1)[0][0] if c else 1
# outline on boundary
m=s>0
for j in range(64):
  for i in range(64):
    if m[j,i]:
      for dj,di in((0,1),(1,0),(0,-1),(-1,0)):
        jj,ii=j+dj,i+di
        if not(0<=jj<64 and 0<=ii<64) or not m[jj,ii]: s[j,i]=1
np.save('s64.npy',s); save(s,'s64_8x.png',8)
print(m[:, :].any(1).nonzero()[0][[0,-1]], m.any(0).nonzero()[0][[0,-1]])
