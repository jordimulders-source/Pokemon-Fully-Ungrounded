# vlaklum.py: per vlak een binnen dat vlak uitgevlakte helderheid (textuur/vlekken van het model weg, schaduwverloop blijft)
import numpy as np, sys
from PIL import Image, ImageFilter
M='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp'
c=np.asarray(Image.open(M).convert('RGB')).astype(float); L=c.mean(2)
def box(A,r):
    P=np.pad(A,r+1,mode='constant'); S=P.cumsum(0).cumsum(1)
    h,w=A.shape; k=2*r+1
    return S[k:k+h,k:k+w]-S[0:h,k:k+w]-S[k:k+h,0:w]+S[0:h,0:w]
lab=np.load('labels.npy'); R=int(sys.argv[1]) if len(sys.argv)>1 else 24
SL=np.zeros_like(L); med=np.zeros(lab.max()+1)
for k in range(1,lab.max()+1):
    ys,xs=np.where(lab==k)
    if len(ys)==0: continue
    med[k]=np.median(L[ys,xs])
    y0,y1,x0,x1=max(ys.min()-R,0),ys.max()+R+1,max(xs.min()-R,0),xs.max()+R+1
    mk=(lab[y0:y1,x0:x1]==k).astype(float)
    a=box(L[y0:y1,x0:x1]*mk,R); b=box(mk,R)
    v=a/np.maximum(b,1e-3)
    SL[y0:y1,x0:x1][mk>0]=v[mk>0]
np.save('SL.npy',SL); np.save('med.npy',med)
o=np.where(lab>0,SL,255).astype('uint8'); Image.fromarray(o).save('vlaklum.png')
