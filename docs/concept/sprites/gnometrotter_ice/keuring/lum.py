import sys; sys.path.insert(0,'../../gnometrotter_rock/sprite')
from kijk import model_op_schaal
import numpy as np
S=8; m=np.asarray(model_op_schaal(sys.argv[1],64*S)).astype(float)
L=m@[.299,.587,.114]; x0,y0,x1,y1=[int(v) for v in sys.argv[2:6]]; mode=sys.argv[6] if len(sys.argv)>6 else 'mean'
print('     '+' '.join('%3d'%x for x in range(x0,x1)))
for y in range(y0,y1):
  r=[]
  for x in range(x0,x1):
    b=L[y*S:(y+1)*S,x*S:(x+1)*S]
    r.append(b.mean() if mode=='mean' else np.percentile(b,15))
  print('%3d  '%y+' '.join('%3d'%v for v in r))
