"""Lader overworld (192x32, frames 0/2/4) + hexraster om punten af te lezen.
python3 laad_ow.py soort [frames]  -> palet + hexrasters (index in hex, . = leeg) met absolute coordinaten"""
import os,sys,numpy as np
from PIL import Image
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'../../../../../..'))
def pal(sp):
    L=open(ROOT+'/graphics/pokemon/%s/overworld_normal.pal'%sp).read().split('\n'); n=int(L[2])
    return [tuple(int(v) for v in L[3+k].split()[:3]) for k in range(n)]
def frame(sp,k):
    o=np.array(Image.open(ROOT+'/graphics/pokemon/%s/overworld.png'%sp)); return o[:32,32*k:32*k+32]
def rgba(ix,P):
    o=np.zeros(ix.shape+(4,),np.uint8)
    for k in range(1,16):
        if k<len(P): o[ix==k]=P[k]+(255,)
    return o
def hexr(ix):
    ys,xs=np.nonzero(ix); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    out=['    '+''.join(str(x//10%10) if x%10==0 else ' ' for x in range(x0,x1+1)),'    '+''.join(str(x%10) for x in range(x0,x1+1))]
    for y in range(y0,y1+1): out.append('%3d '%y+''.join('.' if ix[y,x]==0 else '%x'%ix[y,x] for x in range(x0,x1+1)))
    return '\n'.join(out)
if __name__=='__main__':
    sp=sys.argv[1]; fr=[int(c) for c in (sys.argv[2] if len(sys.argv)>2 else '024')]
    print(sp,' '.join('%x:%02x%02x%02x'%((k,)+c) for k,c in enumerate(pal(sp))))
    for k in fr: print('frame',k); print(hexr(frame(sp,k)))
