import cfg,numpy as np,sys
a=cfg.read(sys.argv[1]); H,W=a.shape
print('kleuren',sorted(set(a.ravel())), 'aantal',len(set(a.ravel())))
iso=[];los1=[]
for y in range(1,63):
  for x in range(1,63):
    v=a[y,x]
    if v==0: continue
    n4=[a[y-1,x],a[y+1,x],a[y,x-1],a[y,x+1]]
    if v in (2,3,4,5,6) and v not in n4: iso.append((x,y,cfg.CH[v]))
    if v in (1,15):
      n8=a[y-1:y+2,x-1:x+2].ravel()
      if 0 not in n8 and sum(1 for t in n8 if t in (1,15))<=1: los1.append((x,y,cfg.CH[v]))
print('losse tintpixels',len(iso),iso)
print('losse lijnpixels',len(los1),los1)
# lichte kleur op buitenrand
br=[]
for y in range(64):
  for x in range(64):
    if a[y,x] and a[y,x] not in (1,15,2):
      for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if not(0<=yy<64 and 0<=xx<64) or a[yy,xx]==0: br.append((x,y,cfg.CH[a[y,x]])); break
print('lichte buitenrand',len(br),br)
