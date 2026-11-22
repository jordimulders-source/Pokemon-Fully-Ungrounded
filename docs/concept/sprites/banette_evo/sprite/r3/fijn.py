# Fijne klasse per spritepixel in een zone: python3 fijn.py x0 y0 x1 y1
import sys; from PIL import Image; import numpy as np
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(int); r,g,b=a[...,0],a[...,1],a[...,2]; L=a.sum(2)/3
C=np.full(L.shape,'.',dtype='<U1')
sat=a.max(2)-a.min(2)
C[(sat<30)&(L>=100)&(L<180)]='g'; C[(sat<30)&(L>=45)&(L<100)]='d'; C[(sat<30)&(L>=180)]='w'
C[(r-np.maximum(g,b)>40)]='r'; C[(r>200)&(g>95)&(g<180)&(b<140)]='o'; C[(r>190)&(g>170)&(b<170)&(r-b>30)]='y'
C[(b-r>12)&(b>=g)]='b'
C[L<45]='k'; C[a.min(2)>=235]='.'
x0,y0,x1,y1=[int(v) for v in sys.argv[1:5]]; S=968/62
print('     '+''.join('%-5d'%i for i in range(x0,x1)))
for j in range(y0,y1):
    row=[]
    for i in range(x0,x1):
        xa,ya=int(round(24+(i-1)*S)),int(round(1+(j-4)*S)); blk=C[max(ya,0):ya+int(S),max(xa,0):xa+int(S)].ravel()
        u,c=np.unique(blk,return_counts=True); o=np.argsort(-c)
        s=''.join(u[o[k]]+str(min(9,int(10*c[o[k]]/c.sum()))) for k in range(min(2,len(u))))
        row.append('%-5s'%s)
    print('%3d  '%j+''.join(row))
