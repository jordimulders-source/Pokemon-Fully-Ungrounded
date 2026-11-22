import numpy as np; from PIL import Image; from scipy import ndimage
def fit(a,top,bot,left):
    f=a>0; lab,n=ndimage.label(f); s=np.bincount(lab.ravel()); s[0]=0; m=lab==np.argmax(s)
    P=[]
    for x in top: P.append((x+.5,np.where(m[:,x])[0].min()))
    for x in bot: P.append((x+.5,np.where(m[:,x])[0].max()+1))
    for y in left: P.append((np.where(m[y])[0].min(),y+.5))
    P=np.array(P,float); A=np.c_[2*P,np.ones(len(P))]; b=(P**2).sum(1)
    cx,cy,c=np.linalg.lstsq(A,b,rcond=None)[0]; return cx,cy,np.sqrt(c+cx*cx+cy*cy),m
r5=np.array(Image.open('../r5/sprite.png'))
g=np.load('groot.npy')
c5=fit(r5,range(31,45),range(28,45),list(range(17,23))+list(range(35,39)))
cg=fit(g,range(24,54),range(26,46),list(range(14,22))+list(range(37,47)))
print('r5',c5[:3]); print('v16',cg[:3])
np.save('c5.npy',np.array(c5[:3])); np.save('cg.npy',np.array(cg[:3]))
cx,cy,R,m=c5
J,I=np.mgrid[0:64,0:64]
d=np.hypot(I+.5-cx,J+.5-cy)
gap=(d<R-0.7)&(r5==0)
lab,n=ndimage.label(gap)
for k in range(1,n+1):
    ys,xs=np.where(lab==k); print(k,len(ys),'x',xs.min(),xs.max(),'y',ys.min(),ys.max())
# losse stukken binnen de schijf (geen hoofdcomponent)
lab2,n2=ndimage.label(r5>0)
for k in range(1,n2+1):
    mm=lab2==k
    if mm.sum()>200: continue
    ys,xs=np.where(mm); dd=d[mm].mean()
    print('stuk',k,mm.sum(),'x',xs.min(),xs.max(),'y',ys.min(),ys.max(),'r/R',round(dd/R,2))
