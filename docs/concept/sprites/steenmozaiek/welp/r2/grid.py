import sys, numpy as np
CH=dict(enumerate('.KdsmlpqrgWcTGXYZ'))
def show(a,x0=0,x1=None,y0=0,y1=None):
    x1=x1 or a.shape[1]; y1=y1 or a.shape[0]
    print('   '+''.join(str(i%10) for i in range(x0,x1)))
    for j in range(y0,y1): print('%2d '%j+''.join(CH[v] for v in a[j,x0:x1]))
if __name__=='__main__':
    a=np.load(sys.argv[1]); show(a,*map(int,sys.argv[2:]))
