# Vergroten zodat de groep het vak vult (niets tekenen): 4 kolommen en 4 rijen verdubbelen, verdeeld rond het midden,
# buiten oog (x29-38, y22-35) en buiten de neuspunt. Kolommen 14,25 | 44,50; rijen 14,19 | 40,46. Daarna centreren.
import numpy as np, tool
o=np.load('rond.npy'); z=np.load('rond_zone.npy'); q=np.load('q.npy')
C=[14,25,44,50]; Rr=[14,19,40,46]
def rek(a):
    a=np.insert(a,[c+1 for c in C],a[:,C],axis=1)
    a=np.insert(a,[r+1 for r in Rr],a[Rr,:],axis=0); return a
O=rek(o); Z=rek(z); Q=rek(q)
ys,xs=np.where(O>0); print('bbox',xs.min(),xs.max(),ys.min(),ys.max(),O.shape)
w=xs.max()-xs.min()+1; h=ys.max()-ys.min()+1
ox=(64-w)//2-xs.min(); oy=(64-h)//2-ys.min()+ (1 if (64-h)%2 else 0)
def place(A):
    out=np.zeros((64,64),A.dtype)
    for j,i in zip(*np.where(A if A.dtype==bool else A>0)): out[j+oy,i+ox]=A[j,i]
    return out
O2=place(O); Z2=place(Z); Q2=place(Q)
np.save('groot.npy',O2); np.save('groot_zone.npy',Z2); np.save('groot_model.npy',Q2)
ys,xs=np.where(O2>0); print('nieuw bbox',xs.min(),xs.max(),ys.min(),ys.max(),'offset',ox,oy)
