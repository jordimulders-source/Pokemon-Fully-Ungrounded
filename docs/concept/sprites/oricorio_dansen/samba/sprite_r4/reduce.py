# natief (200x200 klassen) -> 3x kleiner per 3x3-blok (ijskomeet-methode: geen gemiddelde, elke spritepixel = een modelklasse):
#  lijnklasse (O) wint bij >=3 van 9; anders, bij >=4 dekkende pixels, de meest voorkomende klasse (gelijkspel: donkerste wint); anders transparant.
import numpy as np, sys
from palet import NAMEN, KL
lab=np.load('km_lab.npy'); I={n:i for i,n in enumerate(NAMEN)}
cl=np.zeros(lab.shape,int)
for k,v in KL.items(): cl[lab==k]=I[v]
np.save('klassen_natief.npy',cl)
# donkerte-rang voor gelijkspel (hoger = donkerder)
RANG={'O':9,'G4':8,'Y3':7,'K3':7,'B2':7,'G3':5,'B1':5,'K2':4,'Y2':4,'G2':3,'G1':1,'Y1':1,'K1':1,'W':0}
def red(py,px,nO=3,nd=4):
    H=(cl.shape[0]-py)//3; W=(cl.shape[1]-px)//3; o=np.zeros((H,W),int)
    for j in range(H):
        for i in range(W):
            b=cl[py+3*j:py+3*j+3,px+3*i:px+3*i+3].ravel()
            if (b==I['O']).sum()>=nO: o[j,i]=I['O']; continue
            v=b[b>0]
            if len(v)<nd: continue
            u,c=np.unique(v,return_counts=True); m=c.max()
            kand=[x for x,cc in zip(u,c) if cc==m]
            o[j,i]=max(kand,key=lambda x:RANG[NAMEN[x]])
    return o
if __name__=='__main__':
    py,px=int(sys.argv[1]),int(sys.argv[2])
    o=red(py,px); np.save('reductie.npy',o); ys,xs=np.where(o>0)
    print(o.shape,'bbox',xs.max()-xs.min()+1,ys.max()-ys.min()+1,'px',(o>0).sum())
