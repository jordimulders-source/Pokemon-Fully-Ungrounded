# dekking.py x0 y0 x1 y1 : per spritecel de modeldekking (in %) van: lichtroze oog (e), violet oog (E), zwart (#)
import sys,numpy as np; from PIL import Image
x0,y0,x1,y1=map(int,sys.argv[1:5])
nat=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); grp=np.load('ngrp.npy'); L=nat.mean(-1)
R,G,B=nat[...,0],nat[...,1],nat[...,2]
e=(R-G>20)&(L>180)&(nat.min(-1)<235); E=(grp=='e')&~e; K=grp=='#'
X0,Y0,fx,fy,OX,OY=21,12,109/56,123/63,4,1
def ov(a0,a1,n):
    w=np.zeros(n)
    for k in range(int(np.floor(a0)),int(np.ceil(a1))):
        if 0<=k<n: w[k]=min(a1,k+1)-max(a0,k)
    return w
for nm,m in (('licht e',e),('violet E',E),('zwart',K)):
    print(nm); print('     '+''.join(f'{x:4d}' for x in range(x0,x1)))
    for y in range(y0,y1):
        wy=ov(Y0+(y-OY)*fy,Y0+(y-OY+1)*fy,nat.shape[0]); s=''
        for x in range(x0,x1):
            wx=ov(X0+(x-OX)*fx,X0+(x-OX+1)*fx,nat.shape[1]); w=np.outer(wy,wx)
            s+=f'{int(100*(w*m).sum()/w.sum()):4d}'
        print(f'{y:4d} '+s)
