import numpy as np,sys
o=np.load(sys.argv[1]); ch='KDsmlrRL'+'yYpPoO'
y0,y1,x0,x1=map(int,sys.argv[2:6])
print('   '+''.join(str(i//10%10) for i in range(x0,x1)));print('   '+''.join(str(i%10) for i in range(x0,x1)))
for j in range(y0,y1): print('%2d '%j+''.join(ch[v] if v>=0 else '.' for v in o[j,x0:x1]))
