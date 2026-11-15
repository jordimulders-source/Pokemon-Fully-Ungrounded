import numpy as np
from PIL import Image
a=np.array(Image.open('../rond/rond_A.png')).astype(int)
H,W=a.shape
cx,cy,R=39.5,36.5,13.6
def reg(y,x):
    v=a[y,x]
    if v==0: return 'T'
    if v in (9,10): return 'V'
    if v in (14,8,13,11,12): return 'B'
    if v in (3,4,6): return 'L'
    if v==7: return 'B' if (x-cx)**2+(y-cy)**2<R*R else 'L'
    return None
R_=np.full(a.shape,' ',dtype='<U1')
for y in range(H):
    for x in range(W):
        r=reg(y,x)
        if r: R_[y,x]=r
# line pixels
L=np.isin(a,[1,2])
info={}
for y,x in zip(*np.nonzero(L)):
    nb=[]
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if dy==dx==0: continue
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W:
                r=reg(yy,xx) if a[yy,xx]!=0 else 'T'
                if r: nb.append(r)
            else: nb.append('T')
    info[(y,x)]=set(nb)
if __name__=='__main__':
    for y in range(22,61):
        row=''
        for x in range(8,56):
            if L[y,x]:
                s=info[(y,x)]-{'T'}
                k=''.join(sorted(s))
                row+={'B':'b','L':'l','V':'v','':'?'}.get(k, {'BL':'X','LV':'Y','BV':'Z','BLV':'W'}.get(k,'?'))
            else: row+=R_[y,x] if R_[y,x]!='T' else '.'
        print('%2d '%y+row)
