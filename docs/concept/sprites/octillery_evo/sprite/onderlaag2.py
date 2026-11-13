import cfg,numpy as np,sys
from onderlaag import kleur
c=cfg.model(); fg=cfg.fgmask(c); L=c.mean(2)
a=np.zeros((64,64),int); A=np.zeros((64,64)); dark=np.zeros((64,64))
for y in range(cfg.TOP,64):
  for x in range(cfg.LEFT,cfg.LEFT+cfg.W):
    sl=cfg.cell(x,y); f=fg[sl]; A[y,x]=f.mean()
    if f.mean()<0.45: continue
    d=(L[sl]<48)&f; dark[y,x]=d.sum()/f.sum()
    nd=f&~d
    a[y,x]=kleur(np.median(c[sl][nd],0)) if nd.sum()>3 else 1
m=a>0
pad=np.pad(m,1); edge=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
a[edge]=1
a[(dark>=0.45)&m]=1
np.save('dark.npy',dark); np.save('A.npy',A)
cfg.write(a,sys.argv[1]); print('px',m.sum())
