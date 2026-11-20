# aandeel van een modelzone per spritepixel (canvascoördinaten), x100
import sys, numpy as np; from PIL import Image
Z=np.load('zones_nat.npy'); N=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); L=N.mean(2)
ys,xs=np.where(Z!='.'); x0,y0=xs.min(),ys.min(); s=(ys.max()+1-y0)/63
zs=sys.argv[1]; x1,x2,y1,y2=map(int,sys.argv[2:6]); extra=sys.argv[6] if len(sys.argv)>6 else ''
for y in range(y1,y2+1):
    row=[]
    for x in range(x1,x2+1):
        a=y0+(y-1)*s; b=x0+(x-6)*s
        zb=Z[int(a):int(np.ceil(a+s)),int(b):int(np.ceil(b+s))]; lb=L[int(a):int(np.ceil(a+s)),int(b):int(np.ceil(b+s))]
        m=np.isin(zb,list(zs))
        if extra=='licht': m=m&(lb>=62)
        row.append('%3d'%int(100*m.mean()))
    print('%3d '%y+' '.join(row))
