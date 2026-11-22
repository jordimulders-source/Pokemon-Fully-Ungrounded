# Alternatieve onderlaag: per blok van 4 natieve rijen/kolommen de rij/kolom schrappen die het meest op zijn buur lijkt (Gengas-methode). Elke pixel = modelpixel.
import numpy as np
lab=np.load('km_lab.npy')
KL={0:'O',1:'O',2:'O',3:'N',4:'N',5:'N',6:'B3',7:'M',8:'B3',9:'M',10:'K2',11:'M',12:'R',13:'B2',14:'L1',15:'G',16:'B1',17:'L2',18:'L2',19:'K1',20:'Y',21:'P'}
NAMEN=['_','O','B1','B2','B3','N','M','L1','L2','P','K1','K2','R','G','Y']
I={n:i for i,n in enumerate(NAMEN)}
cl=np.zeros(lab.shape,int)
for k,v in KL.items(): cl[lab==k]=I[v]
def kies(a,axis,start):
    n=a.shape[axis]; keep=[]
    for b in range(start,n,4):
        grp=list(range(b,min(b+4,n)))
        if len(grp)<4: keep+=grp; continue
        # kosten van schrappen = aantal verschillen met de buur (vorige/volgende)
        def diff(i,j): return (np.take(a,i,axis)!=np.take(a,j,axis)).sum()
        cost=[min(diff(g,g-1) if g>0 else 99,diff(g,g+1) if g+1<n else 99) for g in grp]
        drop=grp[int(np.argmin(cost))]; keep+=[g for g in grp if g!=drop]
    return list(range(0,start))+keep
import sys
sy=int(sys.argv[1]) if len(sys.argv)>1 else 0; sx=int(sys.argv[2]) if len(sys.argv)>2 else 0
r=kies(cl,0,sy); c=kies(cl[r],1,sx)
o=cl[r][:,c]; np.save('schrap.npy',o)
ys,xs=np.where(o>0); print(o.shape,'bbox',xs.max()-xs.min()+1,ys.max()-ys.min()+1)
