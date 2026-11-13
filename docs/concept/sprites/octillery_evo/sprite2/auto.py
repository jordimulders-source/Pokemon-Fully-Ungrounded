# auto.py: onder.txt -> auto.txt  (buitenlijn sluiten, binnenlijnen donkerrood, openingen zwart, selout)
import cfg,numpy as np
a=cfg.read('onder.txt'); o=a.copy()
T=np.pad(a==0,1,constant_values=True)
up=T[:-2,1:-1]; dn=T[2:,1:-1]; lf=T[1:-1,:-2]; rt=T[1:-1,2:]
border=(a>0)&(up|dn|lf|rt)
# openingen: 2x2-blokken van 1
one=(a==1); op=np.zeros_like(one)
for y in range(63):
  for x in range(63):
    if one[y:y+2,x:x+2].all(): op[y:y+2,x:x+2]=True
o[one&~op]=2
o[border]=1
sel=border&(up|lf)&~dn&~rt
o[sel]=2
cfg.write(o,'auto.txt')
n=(o>0).sum(); print('px',n,'zwart %.1f%%'%(100*(o==1).sum()/n),'donkerrood %.1f%%'%(100*(o==2).sum()/n))
