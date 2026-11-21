# Onderlaag: k-means-klassen -> spriteklassen; dan per paar natieve rijen/kolommen de rij/kolom SCHRAPPEN die het meest op zijn buur lijkt
# (Gengas/cumbia-methode, hier 2->1 omdat de Gemini-kunstpixel 2 microcellen is). Elke pixel = modelpixel.
import numpy as np, sys
lab=np.load('km_lab.npy')
NAMEN=['_','O','D0','D1','D2','D3','D4','R1','R2','R3','K1','K2','K3','W']
KL={0:'O',1:'O',2:'O',3:'R3',4:'D4',5:'D4',6:'D3',7:'D3',8:'R3',9:'D2',10:'D2',11:'D1',12:'D1',13:'R2',14:'D0',15:'R1',16:'K2',17:'K1',18:'W',19:'K1'}
I={n:i for i,n in enumerate(NAMEN)}
cl=np.zeros(lab.shape,int)
for k,v in KL.items(): cl[lab==k]=I[v]
def kies(a,axis,start,G=2):
    n=a.shape[axis]; keep=[]
    def diff(i,j): return (np.take(a,i,axis)!=np.take(a,j,axis)).sum()
    for b in range(start,n,G):
        grp=list(range(b,min(b+G,n)))
        if len(grp)<G: keep+=grp[:1]; continue
        cost=[min(diff(g,g-1) if g>0 else 999,diff(g,g+1) if g+1<n else 999) for g in grp]
        drop=grp[int(np.argmin(cost))]; keep+=[g for g in grp if g!=drop]
    return keep
if __name__=='__main__':
    sy=int(sys.argv[1]) if len(sys.argv)>1 else 0; sx=int(sys.argv[2]) if len(sys.argv)>2 else 0
    r=kies(cl,0,sy); c=kies(cl[r],1,sx)
    o=cl[r][:,c]; np.save('schrap.npy',o); np.save('schrap_rc.npy',np.array([r+[-1]*(len(c)-len(r)) if len(r)<len(c) else r, c+[-1]*(len(r)-len(c)) if len(c)<len(r) else c]))
    np.save('klassen_natief.npy',cl)
    ys,xs=np.where(o>0); print(o.shape,'bbox',xs.max()-xs.min()+1,ys.max()-ys.min()+1,'px',(o>0).sum())
