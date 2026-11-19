import numpy as np,sys;o=np.load(sys.argv[1]);z=np.load('lucht.npy');H,W=o.shape
bz=np.zeros((H,W),bool); bz[27:44,0:11]=True; bz[44:49,0:13]=True
e=[];lit=0;litblack=0
for y in range(H):
  for x in range(W):
    if not o[y,x] or z[y,x] or bz[y,x]: continue
    bg=[(not(0<=a<H and 0<=b<W)) or o[a,b]==0 for a,b in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))]
    if not any(bg): continue
    e.append(o[y,x])
    y0,y1,x0,x1=max(0,y-2),min(H,y+3),max(0,x-2),min(W,x+3); w=o[y0:y1,x0:x1]==0; yy,xx=np.mgrid[y0:y1,x0:x1]
    up=(w&(yy<y)).sum()+(w&(xx<x)).sum(); dn=(w&(yy>y)).sum()+(w&(xx>x)).sum()
    if up>dn: lit+=1; litblack+=o[y,x]==1
e=np.array(e);print('lijfrand',len(e),'zwart %.0f%%'%(100*(e==1).mean()),'lichtkant',lit,'waarvan zwart',litblack)
for y in range(H):
  for x in range(W):
    if o[y,x]!=1 or z[y,x] or bz[y,x]: continue
    bg=[(not(0<=a<H and 0<=b<W)) or o[a,b]==0 for a,b in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))]
    if not any(bg): continue
    y0,y1,x0,x1=max(0,y-2),min(H,y+3),max(0,x-2),min(W,x+3); w=o[y0:y1,x0:x1]==0; yy,xx=np.mgrid[y0:y1,x0:x1]
    up=(w&(yy<y)).sum()+(w&(xx<x)).sum(); dn=(w&(yy>y)).sum()+(w&(xx>x)).sum()
    if up>=dn: print((x,y),up,dn,sorted(set(int(v) for v in o[max(0,y-1):y+2,max(0,x-1):x+2].ravel())))
