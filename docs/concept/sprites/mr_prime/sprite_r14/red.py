import numpy as np; from PIL import Image
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/mr_prime/sprite_r1')
from bgmask import bgmask
TONES=np.array([1,47,63,77,116,150,208,253]); LIJN=0.28
def red_img(path,W=80,H=72):
    a=np.asarray(Image.open(path).convert('RGB')); b=bgmask(a); L=a.astype(float).mean(axis=2)
    Lu=np.repeat(np.repeat(L,2,0),2,1); Bu=np.repeat(np.repeat(b,2,0),2,1)
    out=np.full((H,W),-1)
    for Y in range(H):
        for X in range(W):
            j=Y-3; ys=48+2+5*j; xs=14+5*X
            if ys<0 or xs<0: continue
            l=Lu[ys:ys+5,xs:xs+5]; m=~Bu[ys:ys+5,xs:xs+5]
            if l.size==0 or m.mean()<0.45: continue
            blk=(l<30)&m
            if blk.sum()/l.size>=LIJN or (m&~blk).sum()==0: out[Y,X]=0; continue
            out[Y,X]=np.abs(l[m&~blk].mean()-TONES).argmin()
    return out
def show(C,x0,x1,y0,y1):
    print('    '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d  '%y+''.join('.' if C[y,x]<0 else str(C[y,x]) for x in range(x0,x1)))
