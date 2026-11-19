# Meting: per spritepixel (x,y op 64x64) gemiddelde en minimale helderheid van het natieve model (zelfde geometrie als r2/bouw.py).
import sys, numpy as np; from PIL import Image
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); Lum=N.mean(2)
Z=np.load('zones_nat.npy'); fgn=Z!='.'; ys,xs=np.nonzero(fgn)
x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
TH=48; s=(y1-y0)/TH; TW=int(np.ceil((x1-x0)/s)); OX=-((TW*s-(x1-x0))/2)
PY,PX=14,16
def cell(x,y):
    j=y-PY; i=x-PX
    a=x0+OX+i*s; b=y0+j*s
    return a,a+s,b,b+s
def meet(x,y):
    ax,bx,ay,by=cell(x,y)
    sub=Lum[int(np.floor(ay)):int(np.ceil(by)),int(np.floor(ax)):int(np.ceil(bx))]
    zs=Z[int(np.floor(ay)):int(np.ceil(by)),int(np.floor(ax)):int(np.ceil(bx))]
    return sub.mean(),sub.min(),''.join(sorted(set(zs.ravel())))
if __name__=='__main__':
    X0,X1,Y0,Y1=map(int,sys.argv[1:5]); print('s=',round(s,3))
    print('     '+''.join('%8d'%x for x in range(X0,X1)))
    for y in range(Y0,Y1):
        print('%3d  '%y+''.join('%4d/%3d'%meet(x,y)[:2] for x in range(X0,X1)))
    print('zones'); 
    for y in range(Y0,Y1): print('%3d  '%y+''.join('%8s'%meet(x,y)[2] for x in range(X0,X1)))
