# Shuppet-silhouetten uit het model: dekking van blauw (b/n) + omlijning (k) binnen de Shuppet-zone, drempel 0,5
import numpy as np; from PIL import Image; from scipy import ndimage as nd
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(int); r,gg,b=a[...,0],a[...,1],a[...,2]; L=a.sum(2)/3
blauw=((b-r>8)&(b>=gg-4))|(L<60)
S=968/62
def mask(box,ss=15):
    x0,y0,x1,y1=box; m=np.zeros((64,64)); 
    for j in range(y0,y1):
        for i in range(x0,x1):
            xa,ya=24+(i-1)*S,1+(j-4)*S
            blk=blauw[int(round(ya)):int(round(ya+S)),int(round(xa)):int(round(xa+S))]
            m[j,i]=blk.mean()
    return m
for naam,box in (('L',(1,37,17,58)),('R',(44,40,63,63))):
    m=mask(box); np.save('shup_%s.npy'%naam,m)
    x0,y0,x1,y1=box
    print(naam); print('    '+''.join('%x'%(i%16) for i in range(x0,x1)))
    for j in range(y0,y1): print('%3d '%j+''.join(' ' if m[j,i]<0.05 else str(min(9,int(m[j,i]*10))) for i in range(x0,x1)))
