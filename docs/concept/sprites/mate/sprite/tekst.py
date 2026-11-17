import sys,numpy as np; from PIL import Image
a=np.asarray(Image.open(sys.argv[1])); ch='.#abcdGHIstu'
x0,y0,x1,y1=map(int,sys.argv[2:6])
print('   '+''.join(str(x//10) for x in range(x0,x1+1))); print('   '+''.join(str(x%10) for x in range(x0,x1+1)))
for y in range(y0,y1+1): print('%2d '%y+''.join(ch[v] for v in a[y,x0:x1+1]))
