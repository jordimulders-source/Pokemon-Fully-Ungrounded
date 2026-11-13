# check.py raster : kleuren, aandeel zwart, lichte kleur op buitenrand, losse tintpixels, losse lijnpixels
import cfg,numpy as np,sys
a=cfg.read(sys.argv[1]); n=(a>0).sum()
print('px',n,'bbox x',np.where(a.any(0))[0][[0,-1]],'y',np.where(a.any(1))[0][[0,-1]],'kleuren',sorted(set(a.ravel())-{0}))
print('zwart(1) %.1f%%  donkerrood(2) %.1f%%  geel %.1f%%'%(100*(a==1).sum()/n,100*(a==2).sum()/n,100*np.isin(a,[9,10,11]).sum()/n))
P=np.pad(a,1); br=[];iso=[];los=[]
for y in range(64):
  for x in range(64):
    v=a[y,x]
    if not v: continue
    n4=[P[y,x+1],P[y+2,x+1],P[y+1,x],P[y+1,x+2]]
    if 0 in n4 and v not in (1,2,12): br.append((x,y,cfg.CH[v]))
    if v in (3,4,5,6) and v not in n4: iso.append((x,y,cfg.CH[v]))
    if v in (1,2):
      n8=P[y:y+3,x:x+3].ravel()
      if 0 not in n8 and sum(1 for t in n8 if t in (1,2))<=1: los.append((x,y,cfg.CH[v]))
print('lichte buitenrand',len(br),br); print('losse tintpixels',len(iso),iso); print('losse lijnpixels',len(los),los)
