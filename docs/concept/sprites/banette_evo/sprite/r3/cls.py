# klassekaart per spritepixel (meerderheidsklasse van het model, met dekkingsdrempel): python3 cls.py x0 y0 x1 y1
import sys,numpy as np; from PIL import Image
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(int); r,gg,b=a[...,0],a[...,1],a[...,2]; L=a.sum(2)/3; sat=a.max(2)-a.min(2)
C=np.full(L.shape,'.',dtype='<U1')
C[(sat<30)&(L>=100)&(L<180)]='g'; C[(sat<30)&(L>=45)&(L<100)]='d'; C[(sat<30)&(L>=180)&(a.min(2)<235)]='w'
C[(r-np.maximum(gg,b)>40)]='r'; C[(b-r>12)&(b>=gg)&(L>=95)]='b'; C[(b-r>12)&(b>=gg)&(L<95)&(L>=45)]='n'
C[(r>190)&(gg>150)&(b<190)&(r-b>25)]='y'
C[L<45]='k'
x0,y0,x1,y1=[int(v) for v in sys.argv[1:5]]; S=968/62
print('    '+''.join('%x'%(i%16) for i in range(x0,x1)))
for j in range(y0,y1):
    s=''
    for i in range(x0,x1):
        xa,ya=int(round(24+(i-1)*S)),int(round(1+(j-4)*S)); blk=C[max(ya,0):ya+15,max(xa,0):xa+15].ravel()
        u,c=np.unique(blk,return_counts=True)
        if (blk=='.').mean()>0.5: s+='.'; continue
        u2=[(cc,uu) for uu,cc in zip(u,c) if uu!='.']; s+=max(u2)[1]
    print('%3d '%j+s)
