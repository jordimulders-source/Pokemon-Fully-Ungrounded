import sys; sys.path.insert(0,'../../gnometrotter_rock/sprite')
from kijk import model_op_schaal
import numpy as np; from PIL import Image
S=8; m=np.asarray(model_op_schaal(sys.argv[1],64*S)).astype(float).reshape(64,S,64,S,3).mean((1,3))
im=Image.open(sys.argv[2]); a=np.asarray(im); pal=np.array(im.getpalette()[:48]).reshape(-1,3).astype(float)
grp=[int(g) for g in sys.argv[3].split(',')]; x0,y0,x1,y1=[int(v) for v in sys.argv[4:8]]
print('    '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1):
  s='';t=''
  for x in range(x0,x1):
    v=a[y,x]; s+='.' if v==0 else '0123456789ABCDEF'[v]
    if v in grp: d=((pal[grp]-m[y,x])**2).sum(1); t+='0123456789ABCDEF'[grp[int(d.argmin())]]
    else: t+=' ' if v==0 else '-'
  print('%2d  %s   %s'%(y,s,t))
