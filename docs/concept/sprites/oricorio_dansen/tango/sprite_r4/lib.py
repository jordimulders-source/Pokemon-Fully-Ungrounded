import numpy as np
NAMEN=['_','O','D1','D2','D3','D4','D5','D6','K1','K2','K3','W','R']
I={n:i for i,n in enumerate(NAMEN)}
SYM='.O123456abcWRr'
def show(o,y0=0,y1=None,x0=0,x1=None):
    y1=y1 or o.shape[0]; x1=x1 or o.shape[1]
    print('    '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d  '%y+''.join(SYM[o[y,x]] for x in range(x0,x1)))
def nb4(o,y,x):
    H,W=o.shape
    for dy,dx in((-1,0),(1,0),(0,-1),(0,1)):
        yy,xx=y+dy,x+dx
        yield (yy,xx) if (0<=yy<H and 0<=xx<W) else (None,None)
def comps(mask):
    H,W=mask.shape; seen=np.zeros(mask.shape,bool); out=[]
    for y in range(H):
        for x in range(W):
            if mask[y,x] and not seen[y,x]:
                st=[(y,x)]; seen[y,x]=True; pts=[]
                while st:
                    a,b=st.pop(); pts.append((a,b))
                    for dy,dx in((-1,0),(1,0),(0,-1),(0,1)):
                        yy,xx=a+dy,b+dx
                        if 0<=yy<H and 0<=xx<W and mask[yy,xx] and not seen[yy,xx]: seen[yy,xx]=True; st.append((yy,xx))
                out.append(pts)
    return out
def ori(v):
    from PIL import Image
    return np.asarray(Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/oricorio/%sanim_front.png'%v))[:64]
