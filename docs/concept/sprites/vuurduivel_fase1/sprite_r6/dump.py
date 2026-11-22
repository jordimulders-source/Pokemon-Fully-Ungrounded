import sys, numpy as np; from PIL import Image
CH='.#dmlRrOYbBkXWHg'
o=np.asarray(Image.open(sys.argv[1]))
x0,x1,y0,y1=map(int,sys.argv[2:6]) if len(sys.argv)>2 else (10,54,12,64)
print('   '+''.join(str(x//10) for x in range(x0,x1))); print('   '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%2d %s'%(y,''.join(CH[v] for v in o[y,x0:x1])))
