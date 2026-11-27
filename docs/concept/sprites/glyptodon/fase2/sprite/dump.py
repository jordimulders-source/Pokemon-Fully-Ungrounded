import sys,numpy as np
I=np.load(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6])
ch='.K234567893abcdef'
sym={0:'.',1:'#',2:'o',3:'y',4:'Y',5:'b',6:'m',7:'l',8:'e',9:'E',10:'-',11:'g',12:'G',13:'H',14:'O',15:'r'}
print('    '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print(f'{y:3d} '+''.join(sym[int(v)] for v in I[y,x0:x1]))
