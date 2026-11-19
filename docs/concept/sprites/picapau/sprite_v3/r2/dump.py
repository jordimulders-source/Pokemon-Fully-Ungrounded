import sys,numpy as np
o=np.load(sys.argv[1]); ch='.Z#gdWwSsTrRvVc?ObM'
y0,y1,x0,x1=[int(v) for v in sys.argv[2:6]] if len(sys.argv)>2 else (0,64,0,64)
print('   '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%2d '%y+''.join(ch[v] for v in o[y,x0:x1]))
