import sys; sys.path.insert(0,'.')
import sys; sys.path.insert(0,'r7w')
from proj import *
lum=A.mean(2); L=lum<60
F=np.zeros((64,64))
for j in range(64):
  for i in range(64):
    x0,y0,x1,y1=box(i,j)
    b=L[max(0,int(round(y0))):max(0,int(round(y1))),max(0,int(round(x0))):max(0,int(round(x1)))]
    F[j,i]=b.mean() if b.size else 0
np.save('r7w/F.npy',F)
from gio import from_txt,CH
o=from_txt('r5.txt')
for y in range(10,64):
  print('%2d '%y+''.join(('.' if o[y,x]<0 else ' ') if F[y,x]<0.08 else str(min(9,int(F[y,x]*10))) for x in range(0,64))+'   '+''.join('.' if v<0 else CH[v] for v in o[y]))
