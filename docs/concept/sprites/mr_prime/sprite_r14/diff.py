# Diff r14 tegen r13: per zone tellen, en bewijzen dat buiten de drie zones alles pixel-gelijk is.
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../sprite_r13/mr_prime.png').convert('RGBA')).astype(int)
b=np.asarray(Image.open('mr_prime.png').convert('RGBA')).astype(int)
A=a[...,3]>0; B=b[...,3]>0
d=(A!=B)|(A&B&np.any(a[...,:3]!=b[...,:3],axis=-1))
Z={'1 verre arm':(44,58,26,42),'2 achterbeen':(41,64,44,64),'3 rokpanden':(36,44,49,55)}
seen=np.zeros_like(d)
for n,(x0,x1,y0,y1) in Z.items():
    m=np.zeros_like(d); m[y0:y1,x0:x1]=1; m&=~seen; seen|=m
    print(n,'x%d-%d y%d-%d'%(x0,x1-1,y0,y1-1),'gewijzigd:',int((d&m).sum()))
print('buiten de zones gewijzigd:',int((d&~seen).sum()))
ys,xs=np.where(b[...,3]>0); print('bbox r14: x%d-%d y%d-%d'%(xs.min(),xs.max(),ys.min(),ys.max()))
