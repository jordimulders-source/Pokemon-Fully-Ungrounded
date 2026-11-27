# telt per spritecel (3x3 natief) de modelpixels die een dunne donkere lijn zijn (donkerder dan de mediaan van 5x5 rondom)
import sys; from PIL import Image; import numpy as np
a=np.asarray(Image.open(sys.argv[1])).astype(float); L=a@[.299,.587,.114]
MY,MX=np.load('fase/f01_map.npy'); H,W=L.shape
from numpy.lib.stride_tricks import sliding_window_view as sw
P=np.pad(L,2,mode='edge'); med=np.median(sw(P,(5,5)),axis=(-1,-2))
lijn=(L<100)&(L>=40)&(med-L>18)
np.save('lijn_natief.npy',lijn)
y0,y1,x0,x1=12,33,21,38
print('    '+''.join('%2d'%(x%100) for x in range(x0,x1)))
for sy in range(y0,y1):
  r=''
  for sx in range(x0,x1):
    b=lijn[MY+3*sy:MY+3*sy+3, MX+3*sx:MX+3*sx+3]; n=b.sum()
    r+=' '+('.' if n==0 else str(n))
  print('%3d'%sy+r)
