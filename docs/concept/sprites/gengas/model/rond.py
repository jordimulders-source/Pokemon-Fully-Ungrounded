# Maakt het lijf weer een bol: onder de oren (y>=40) precies de gepaste cirkel; deuken gevuld met de kleur radiaal naar binnen.
from PIL import Image; import numpy as np, sys
S=sys.argv[1]
a=np.asarray(Image.open(S+'/n10.png').convert('RGB')).astype(int)
body=np.load(S+'/body.npy'); cx,cy,r=np.load(S+'/circ.npy'); H,W=body.shape
lum=0.299*a[...,0]+0.587*a[...,1]+0.114*a[...,2]
Y,X=np.mgrid[0:H,0:W]; inside=np.hypot(X+0.5-cx-0.5,Y+0.5-cy-0.5)<=r+0.3
low=Y>=40
mask=np.where(low,inside,body)
old_rim=body&~np.roll(body,1,0)|body&~np.roll(body,-1,0)|body&~np.roll(body,1,1)|body&~np.roll(body,-1,1)
rim=mask&(~np.roll(mask,1,0)|~np.roll(mask,-1,0)|~np.roll(mask,1,1)|~np.roll(mask,-1,1))
out=a.copy(); OUT=np.array([28,12,20])
def inward(y,x):
    vx,vy=cx-x,cy-y; n=np.hypot(vx,vy); vx/=n; vy/=n
    for k in range(1,12):
        yy,xx=int(round(y+vy*k)),int(round(x+vx*k))
        if body[yy,xx] and not old_rim[yy,xx] and lum[yy,xx]>45: return a[yy,xx]
    return a[int(cy),int(cx)]
for y,x in zip(*np.where(mask&low)):
    if rim[y,x]: out[y,x]=OUT
    elif (not body[y,x]) or (old_rim[y,x] and lum[y,x]<45): out[y,x]=inward(y,x)
np.save(S+'/body2.npy',mask); np.save(S+'/ba2.npy',out)
v=np.full((H,W,3),255); v[mask]=out[mask]
Image.fromarray(v.astype('uint8')).resize((W*6,H*6),Image.NEAREST).save(S+'/bol.png')
print('verschil px',int((mask!=body).sum()))
