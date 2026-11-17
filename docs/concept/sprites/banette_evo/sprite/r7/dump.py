import sys,numpy as np
g=np.load(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6])
ch='.k lmdcrRbyLMBwne'
ch={0:'.',1:'k',2:'l',3:'m',4:'d',5:'c',6:'r',7:'R',8:'b',9:'y',10:'L',11:'M',12:'B',13:'w',14:'n',15:'e'}
print('   '+''.join(str(i%10) for i in range(x0,x1)))
for j in range(y0,y1): print('%2d '%j+''.join(ch[int(v)] for v in g[j,x0:x1]))
