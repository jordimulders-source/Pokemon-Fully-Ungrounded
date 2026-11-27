import sys; import numpy as np; from PIL import Image
a=np.array(Image.open(sys.argv[1])); ch='.KLSMHabcdWG'
x0,y0,x1,y1=map(int,sys.argv[2:6]) if len(sys.argv)>2 else (0,0,64,64)
print('   '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%2d '%y+''.join(ch[v] for v in a[y,x0:x1]))
c=[(a==k).sum() for k in (2,3,4,5)]; t=sum(c); print('L/S/M/H %',[round(100*v/t) for v in c],t)
