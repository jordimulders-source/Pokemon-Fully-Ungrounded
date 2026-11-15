# Past een cirkel op de lijfrand (onder de oren) en toont rand vs cirkel
from PIL import Image; import numpy as np, sys
S=sys.argv[1]; sys.path.insert(0,S); from seg import label
a=np.asarray(Image.open(S+'/n10.png').convert('RGB')).astype(int)
lab=np.load(S+'/lab.npy'); limb=np.isin(lab,[1,7,8,11])
bg=a.min(axis=2)>=232; reach=bg|limb; l2,n=label(reach)
e=set(l2[0,:])|set(l2[-1,:])|set(l2[:,0])|set(l2[:,-1]); e.discard(0)
body=~np.isin(l2,list(e))
ys,xs=np.where(body)
# randpixels onder y=40 (onder de oren)
pts=[(x,y) for y,x in zip(ys,xs) if y>=40 and (not body[y,x-1] or not body[y,x+1] or not body[y+1,x])]
P=np.array(pts,float); A=np.c_[2*P[:,0],2*P[:,1],np.ones(len(P))]; b=(P**2).sum(1)
cx,cy,c=np.linalg.lstsq(A,b,rcond=None)[0]; r=np.sqrt(c+cx*cx+cy*cy)
print('cirkel',round(cx,1),round(cy,1),round(r,1))
for x,y in pts:
    d=np.hypot(x-cx,y-cy)-r
    if abs(d)>1.2: print('afwijking',x,y,round(d,1))
np.save(S+'/body.npy',body); np.save(S+'/circ.npy',np.array([cx,cy,r]))
