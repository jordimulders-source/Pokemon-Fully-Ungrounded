# pupildekking per spritepixel: donkere modelpixels binnen de iris (rond het zwaartepunt van de teal-pixels per oog)
import numpy as np, kaal
from common import load
a,bg=load(); s=3.515625; OH=kaal.reduce()[0].shape[0]
teal=(a[:,:,1]>a[:,:,0]+25)&(a[:,:,2]>a[:,:,0]+20)&~bg
Y,X=np.mgrid[0:a.shape[0],0:a.shape[1]]
dark=(a.sum(2)<180)&~bg
pup=np.zeros_like(bg); OGEN=[]
BOX={'voor':(X<110)&(Y>100),'links':(X<110)&(Y<=100),'rechts':(X>=150)}
for nm,bx in BOX.items():
    t=teal&bx
    if t.sum()<10: continue
    cy,cx=Y[t].mean(),X[t].mean(); r=np.sqrt(t.sum()/np.pi)
    OGEN.append((cx,cy,r)); pup|=dark&((X-cx)**2+(Y-cy)**2<=(0.75*r)**2)
Wx=kaal.overlap(64,3,s,a.shape[1]); Wy=kaal.overlap(OH,3,s,a.shape[0])
PUP=Wy@pup.astype(float)@Wx.T/(s*s)
if __name__=='__main__':
    print(OGEN)
    ys,xs=np.where(PUP>0.03)
    for y,x in zip(ys,xs): print(x,y,round(PUP[y,x],2))
