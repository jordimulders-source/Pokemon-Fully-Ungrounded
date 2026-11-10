# sub.py x0 y0 x1 y1: model op 2x2 per spritepixel (128-raster) als tekens; kolom/rij-labels in spritecoords
# '#' L<20 omlijning, 'k' <60 zwart vlak, 'D' <110, 'C' <150, 'B' <190, 'A' <232, '-' wit, 'R' rood
import sys,os,numpy as np; H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H+'/../silhouet')
from geo import *
c=model().astype(float); L=c.mean(2)
x0,y0,x1,y1=map(int,sys.argv[1:5])
def ch(b):
    v=b.reshape(-1,3); l=np.median(v.mean(1)); m=np.median(v,0)
    if m[0]>m[2]+40: return 'R'
    return '#' if l<20 else 'k' if l<60 else 'D' if l<110 else 'C' if l<150 else 'B' if l<190 else 'A' if l<232 else '-'
print('    '+''.join(f'{x%100:<2d}' for x in range(x0,x1)))
for Y in range(y0,y1):
  for h in (0,1):
    r=''
    for X in range(x0,x1):
      for w in (0,1):
        ya=int(OY+(Y+h/2)*S); xa=int(OX+(X+w/2)*S); hs=int(S/2)
        r+=ch(c[ya+1:ya+hs-1,xa+1:xa+hs-1])
    print(f'{Y:2d}{"ab"[h]} '+r)
