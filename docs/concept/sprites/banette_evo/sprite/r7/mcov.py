import numpy as np; from PIL import Image
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(float); L=a.sum(2)/3
S=968/62
def cov(M,x0=0,y0=0,x1=64,y1=64):
    o=np.zeros((64,64))
    for j in range(y0,y1):
        for i in range(x0,x1):
            xa,ya=24+(i-1)*S,1+(j-4)*S
            b=M[max(0,int(round(ya))):max(0,int(round(ya+S))),max(0,int(round(xa))):max(0,int(round(xa+S)))]
            o[j,i]=b.mean() if b.size else 0
    return o
