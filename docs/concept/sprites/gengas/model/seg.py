from PIL import Image; import numpy as np, sys
from collections import deque
def label(m):
    H,W=m.shape; lab=np.zeros((H,W),int); n=0
    for y in range(H):
        for x in range(W):
            if m[y,x] and not lab[y,x]:
                n+=1; q=deque([(y,x)]); lab[y,x]=n
                while q:
                    cy,cx=q.popleft()
                    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny,nx=cy+dy,cx+dx
                        if 0<=ny<H and 0<=nx<W and m[ny,nx] and not lab[ny,nx]:
                            lab[ny,nx]=n; q.append((ny,nx))
    return lab,n
if __name__=='__main__':
    a=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int)
    fg=a.min(axis=2)<int(sys.argv[2])
    lab,n=label(fg)
    for i in range(1,n+1):
        ys,xs=np.where(lab==i)
        if len(xs)>3: print(i,len(xs),xs.min(),xs.max(),ys.min(),ys.max())
