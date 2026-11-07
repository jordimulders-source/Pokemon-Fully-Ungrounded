# meet.py X0 Y0 X1 Y1 [mean|p15|max] : modelhelderheid per spritepixel (//10) naast de onderlaag
import sys
from tl import *
X0,Y0,X1,Y1=map(int,sys.argv[1:5]); md=sys.argv[5] if len(sys.argv)>5 else 'mean'
print('   '+''.join(f'{x:>3}' for x in range(X0,X1)))
for y in range(Y0,Y1):
  r=''
  for x in range(X0,X1):
    if not SIL[y,x]: r+='  .'; continue
    v=LUM[box(x,y)]; m={'mean':v.mean(),'p15':np.percentile(v,15),'max':v.max()}[md]
    r+=f'{int(m)//10:>3}'
  print(f'{y:>2} '+r)
