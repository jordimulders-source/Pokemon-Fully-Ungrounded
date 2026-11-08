import sys; from tools import *
a=load(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6])
print('   '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in a[y,x0:x1]))
