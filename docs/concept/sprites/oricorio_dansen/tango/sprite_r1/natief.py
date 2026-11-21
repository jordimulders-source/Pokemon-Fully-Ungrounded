# Natief raster van gemini_r5 terughalen: per as pitch/fase zoeken met de kleinste reconstructiefout (median per cel, nearest terug) -> natief.png
from PIL import Image; import numpy as np, sys
a=np.asarray(Image.open('../model/gemini_r5.png').convert('RGB')).astype(float)
Y0,Y1,X0,X1=50,520,340,690
sub=a[Y0:Y1,X0:X1]
def recon_err(axis,P,ph):
    g=sub.mean(2); g=g if axis==1 else g.T          # cellen langs kolommen
    n=g.shape[1]; edges=np.arange(ph,n+P,P); err=0
    for i in range(len(edges)-1):
        c0,c1=int(round(edges[i])),int(round(edges[i+1]))
        if c1<=c0 or c0>=n: continue
        blk=g[:,c0:min(c1,n)]; err+=np.abs(blk-np.median(blk,axis=1,keepdims=True)).sum()
    return err
best={}
for ax in (0,1):
    r=min(((recon_err(ax,P,ph),P,ph) for P in np.arange(4.8,5.5,0.02) for ph in np.arange(0,P,0.5)))
    best[ax]=r; print('as',ax,r)
PY,FY=best[0][1],best[0][2]+Y0; PX,FX=best[1][1],best[1][2]+X0
cy=np.arange(FY%PY+PY/2,559,PY); cx=np.arange(FX%PX+PX/2,1024,PX)
out=np.zeros((len(cy),len(cx),3),'uint8')
for j,y in enumerate(cy):
    for i,x in enumerate(cx):
        y0,y1=int(y-1),int(y+2); x0,x1=int(x-1),int(x+2)
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('natief.png'); print(out.shape,PY,FY,PX,FX)
bg=out.min(2)>=225; ys,xs=np.where(~bg); print('bbox',xs.min(),xs.max(),ys.min(),ys.max())
Image.fromarray(out).resize((out.shape[1]*6,out.shape[0]*6),Image.NEAREST).crop((xs.min()*6-12,ys.min()*6-12,xs.max()*6+18,ys.max()*6+18)).save('natief_6x.png')
