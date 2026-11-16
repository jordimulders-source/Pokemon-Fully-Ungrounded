import sys; sys.path.insert(0,'r7w'); sys.path.insert(0,'.')
from proj import *
lum=A.mean(2); free=lum>=float(sys.argv[1])
out=np.zeros_like(free); out[0,:]=free[0,:]; out[-1,:]=free[-1,:]; out[:,0]=free[:,0]; out[:,-1]=free[:,-1]
while True:
    n=out.copy()
    n[1:]|=out[:-1]; n[:-1]|=out[1:]; n[:,1:]|=out[:,:-1]; n[:,:-1]|=out[:,1:]
    n&=free
    if (n==out).all(): break
    out=n
ice=~out
# paars binnen 'ijs' (spikes die dicht zitten) eruit: paars = b > r+25
purple=(A[:,:,2]>A[:,:,0]+25)&(A[:,:,0]<190)
np.save('r7w/ice_full.npy',ice); np.save('r7w/purple_full.npy',purple)
Fi=np.zeros((64,64)); Fp=np.zeros((64,64)); Fl=np.zeros((64,64))
L=lum<60
for j in range(64):
  for i in range(64):
    x0,y0,x1,y1=box(i,j); ys=slice(max(0,int(round(y0))),max(0,int(round(y1)))); xs=slice(max(0,int(round(x0))),max(0,int(round(x1))))
    b=ice[ys,xs]
    if b.size: Fi[j,i]=b.mean(); Fp[j,i]=(purple[ys,xs]&ice[ys,xs]).mean(); Fl[j,i]=L[ys,xs].mean()
np.save('r7w/Fi.npy',Fi); np.save('r7w/Fp.npy',Fp); np.save('r7w/Fl.npy',Fl)
for j in range(14,62): print('%2d '%j+''.join('#' if Fi[j,i]>0.5 and Fp[j,i]<0.3 else ('p' if Fi[j,i]>0.5 else '.') for i in range(0,56)))
