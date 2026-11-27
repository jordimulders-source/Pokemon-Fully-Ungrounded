# 74x68 natief -> <=64 hoog door hele rijen/kolommen te schrappen (zoals gengas/model/schrap.py).
# Achtergrond = bijna-wit dat met de rand verbonden is; witte glanspunten binnen de figuur blijven.
from PIL import Image; import numpy as np, sys
from scipy import ndimage
D='docs/concept/sprites/hitmonlee_regional/sprite/'
a=np.asarray(Image.open(D+'natief.png').convert('RGB')).astype(int)
H,W,_=a.shape
lichte=(a.min(2)>=226)
lab,n=ndimage.label(lichte)
rand=set(lab[0])|set(lab[-1])|set(lab[:,0])|set(lab[:,-1]); rand.discard(0)
bg=np.isin(lab,list(rand))
fig=~bg
np.save(D+'fig_natief.npy',fig)
A=a.copy(); A[bg]=255
def kies(A,M,n,axis,verboden=()):
    X=A if axis==0 else A.transpose(1,0,2); Mx=M if axis==0 else M.T
    cost=[]
    for i in range(len(X)-1):
        d=np.abs(X[i]-X[i+1]).sum(1)
        d=d+ (Mx[i]!=Mx[i+1])*300   # silhouetverandering zwaar
        cost.append(d.sum())
    order=np.argsort(cost); gek=[]
    for i in order:
        if i in verboden or i==0 or i>=len(X)-2: continue
        if all(abs(i-j)>=4 for j in gek): gek.append(int(i))
        if len(gek)==n: break
    return sorted(gek), cost
nr=H-64; nc=int(sys.argv[1]) if len(sys.argv)>1 else 9
# oog beschermen (rijen 35-40 / kolommen 18-27 in natief): zie oog.txt
oogr=set(range(int(sys.argv[2]),int(sys.argv[3]))) if len(sys.argv)>3 else set()
oogc=set(range(int(sys.argv[4]),int(sys.argv[5]))) if len(sys.argv)>5 else set()
rows,_=kies(A,fig,nr,0,oogr); cols,_=kies(A,fig,nc,1,oogc)
B=np.delete(np.delete(A,rows,0),cols,1); F=np.delete(np.delete(fig,rows,0),cols,1)
print('rijen',rows,'kolommen',cols,B.shape)
Image.fromarray(B.astype('uint8')).save(D+'r1/geschrapt.png'); np.save(D+'r1/fig.npy',F)
