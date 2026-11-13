import sys
from PIL import Image
import numpy as np
P=10.24; O=-1.31
def load(fn): return np.asarray(Image.open(fn).convert('RGB')).astype(int)
def cell(a,i,j):
    x0,y0=int(round(O+i*P)),int(round(O+j*P)); return np.median(a[max(y0+3,0):y0+8,max(x0+3,0):x0+8].reshape(-1,3),0)
def cls(c):
    L=c.mean()
    return '.' if L>240 else ('W' if L>222 else ('o' if L<40 else ('k' if L<95 and c[2]-c[0]<14 else ('d' if L<118 else ('c' if L<152 else ('b' if L<182 else 'a'))))))
if __name__=='__main__':
    a=load(sys.argv[1]); x0,x1,y0,y1=map(int,sys.argv[2:6])
    print('   '+''.join(str(i%10) for i in range(x0,x1)))
    for j in range(y0,y1): print('%2d '%j+''.join(cls(cell(a,i,j)) for i in range(x0,x1)))
