import sys,numpy as np
o=np.load(sys.argv[1]); x0,y0,x1,y1=[int(v) for v in sys.argv[2:6]]
print('    '+''.join('%3d'%x for x in range(x0,x1)))
for y in range(y0,y1): print('%3d '%y+''.join('%3s'%('.' if o[y,x]==0 else o[y,x]) for x in range(x0,x1)))
