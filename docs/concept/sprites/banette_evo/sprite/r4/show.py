import sys,numpy as np
CH='.klmdorRMyLCBwne'
def show(g,x0=0,y0=0,x1=64,y1=64):
    print('    '+''.join(str(i%10) for i in range(x0,x1)))
    for j in range(y0,y1): print('%3d '%j+''.join(CH[v] for v in g[j,x0:x1]))
if __name__=='__main__':
    g=np.load(sys.argv[1]); a=[int(v) for v in sys.argv[2:]] or [0,0,64,64]; show(g,*a)
