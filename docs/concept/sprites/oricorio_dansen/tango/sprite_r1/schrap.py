# Onderlaag: per blok van 5 natieve rijen/kolommen de 2 rijen/kolommen schrappen die het meest op hun buur lijken (Gengas/cumbia-methode, 5->3). Elke pixel = modelpixel (klasse).
import numpy as np, sys
lab=np.load('km_lab.npy')
# k-means-centra (km.py, K=16): 0 (3) 1 (18) 2 (27) 3 (29) 4 (36) 5 (48) 6 (53) 7 roze (108,43,56) 8 (68) 9 roze (146,69,82) 10 (101) 11 roze (183,98,112) 12 roze (214,119,133) 13 (154) 14 roze (240,155,168) 15 (217)
KL={0:'O',1:'D1',2:'D2',3:'D2',4:'D3',5:'D3',6:'D4',7:'K3',8:'D5',9:'K3',10:'D6',11:'K2',12:'K2',13:'D6',14:'K1',15:'W'}
NAMEN=['_','O','D1','D2','D3','D4','D5','D6','K1','K2','K3','W','R']
I={n:i for i,n in enumerate(NAMEN)}
cl=np.zeros(lab.shape,int)
for k,v in KL.items(): cl[lab==k]=I[v]
def kies(a,axis,start,blok=5,weg=2):
    n=a.shape[axis]; keep=[]
    def diff(i,j): return (np.take(a,i,axis)!=np.take(a,j,axis)).sum()
    for b in range(start,n,blok):
        grp=list(range(b,min(b+blok,n)))
        if len(grp)<blok: keep+=grp; continue
        drops=[]
        for _ in range(weg):
            rest=[g for g in grp if g not in drops]
            cost=[min(diff(g,g-1) if g>0 else 99,diff(g,g+1) if g+1<n else 99) for g in rest]
            # niet twee naast elkaar schrappen
            cost=[c+(1000 if (g-1 in drops or g+1 in drops) else 0) for g,c in zip(rest,cost)]
            drops.append(rest[int(np.argmin(cost))])
        keep+=[g for g in grp if g not in drops]
    return list(range(0,start))+keep
sy=int(sys.argv[1]) if len(sys.argv)>1 else 0; sx=int(sys.argv[2]) if len(sys.argv)>2 else 0
r=kies(cl,0,sy); c=kies(cl[r],1,sx)
o=cl[r][:,c]; np.save('schrap.npy',o); np.save('schrap_rc.npy',np.array([r+[-1]*(len(c)-len(r)) if len(r)<len(c) else r, c+[-1]*(len(r)-len(c)) if len(c)<len(r) else c],dtype=object),allow_pickle=True)
ys,xs=np.where(o>0); print(o.shape,'bbox',xs.max()-xs.min()+1,ys.max()-ys.min()+1)
