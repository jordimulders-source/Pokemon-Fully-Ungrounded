import sys, numpy as np
from palet import NAMEN
CH={'_':'.','O':'#','L':'l','G1':'1','G2':'2','G3':'3','G4':'4','G5':'5','K3':'r','K2':'k','K1':'p','K0':'q','Y2':'y','Y1':'Y','W':'W'}
o=np.load(sys.argv[1])
if len(sys.argv)<3: ys,xs=np.where(o>0); o=o[ys.min():ys.max()+1,xs.min():xs.max()+1]
y0,y1,x0,x1=(map(int,sys.argv[2].split(',')) if len(sys.argv)>2 else (0,o.shape[0],0,o.shape[1]))
print('   '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%2d '%y+''.join(CH[NAMEN[v]] for v in o[y,x0:x1]))
