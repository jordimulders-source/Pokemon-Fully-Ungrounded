# Onderlaag: natief (136x148, raster 5,12) -> 2x2-reductie met lijnregel -> 68x74 -> schrappen naar 64 hoog
# (hele rijen/kolommen die het meest op hun buur lijken, >=4 uit elkaar, oogzone beschermd), zoals gengas/model/schrap.py.
# gebruik: onderlaag.py <uitmap> <mindonker 1|2> <ncol>
from PIL import Image; import numpy as np, sys
from scipy import ndimage
D='docs/concept/sprites/hitmonlee_regional/sprite/'
out=D+sys.argv[1]+'/'; md=int(sys.argv[2]); nc=int(sys.argv[3])
a=np.asarray(Image.open(D+'natief.png').convert('RGB')).astype(float)
lum=a.mean(2)
# achtergrond natief: bijna-wit verbonden met de rand
lab,n=ndimage.label(a.min(2)>=226)
rand=set(lab[0])|set(lab[-1])|set(lab[:,0])|set(lab[:,-1]); rand.discard(0)
bgn=np.isin(lab,list(rand))
H,W=lum.shape
R=np.zeros((H//2,W//2,3)); F=np.zeros((H//2,W//2),bool)
for y in range(H//2):
    for x in range(W//2):
        blk=a[2*y:2*y+2,2*x:2*x+2].reshape(-1,3); bl=lum[2*y:2*y+2,2*x:2*x+2].ravel(); bb=bgn[2*y:2*y+2,2*x:2*x+2].ravel()
        if bb.sum()>=3: continue          # meer dan de helft achtergrond -> achtergrond
        F[y,x]=True
        fig=~bb
        dk=(bl<80)&fig
        if dk.sum()>=md: R[y,x]=blk[dk][bl[dk].argmin()] if dk.sum()>=2 else blk[dk][0]
        else:
            nd=fig&~dk
            R[y,x]=np.median(blk[nd],0)
# schrappen
def kies(A,M,n,axis,verboden=()):
    X=A if axis==0 else A.transpose(1,0,2); Mx=M if axis==0 else M.T
    cost=[np.abs(X[i]-X[i+1]).sum(1).sum()+(Mx[i]!=Mx[i+1]).sum()*300 for i in range(len(X)-1)]
    gek=[]
    for i in np.argsort(cost):
        if i in verboden or i<1 or i>=len(X)-2: continue
        if all(abs(i-j)>=4 for j in gek): gek.append(int(i))
        if len(gek)==n: break
    return sorted(gek)
A=R.copy(); A[~F]=255
oogr=set(range(29,42)); oogc=set(range(17,35))
rows=kies(A,F,F.shape[0]-64,0,oogr); cols=kies(A,F,nc,1,oogc)
B=np.delete(np.delete(A,rows,0),cols,1); FF=np.delete(np.delete(F,rows,0),cols,1)
print('2x',F.shape,'rijen',rows,'kolommen',cols,'->',B.shape)
import os; os.makedirs(out,exist_ok=True)
Image.fromarray(B.astype('uint8')).save(out+'geschrapt.png'); np.save(out+'fig.npy',FF)
Image.fromarray(A.astype('uint8')).save(out+'twee_x.png'); np.save(out+'fig2x.npy',F)
