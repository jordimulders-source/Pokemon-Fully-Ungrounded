import numpy as np; from PIL import Image
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(float); L=a.sum(2)/3
S=968/62
def covm(M,box):
    x0,y0,x1,y1=box; o=np.zeros((64,64))
    for j in range(y0,y1):
        for i in range(x0,x1):
            xa,ya=24+(i-1)*S,1+(j-4)*S
            o[j,i]=M[int(round(ya)):int(round(ya+S)),int(round(xa)):int(round(xa+S))].mean()
    return o
if __name__=='__main__':
    import sys; thr=float(sys.argv[1]) if len(sys.argv)>1 else 70
    c=covm(L<thr,(12,22,46,47))
    print('    '+''.join('%x'%(i%16) for i in range(12,46)))
    for j in range(22,47): print('%3d '%j+''.join(' ' if c[j,i]<0.05 else str(min(9,int(c[j,i]*10))) for i in range(12,46)))
    np.save('mondcov.npy',c)
