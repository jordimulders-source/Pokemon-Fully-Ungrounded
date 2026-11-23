# modelpunten.py x0 y0 x1 y1 : per spritepixel de modelkleur (dichtstbijzijnde paletkleur) op 2x2 subpunten -> meetkaart
import sys,numpy as np; sys.path.insert(0,'sprite_r1'); from gemeen import *
from PIL import Image
a=np.asarray(Image.open('model/r10_k8.png').convert('RGB')).astype(float); fig=np.load('sprite_r1/masker.npy')
yy,xx=np.where(fig); mx0,my0=xx.min(),yy.min(); s=64/(xx.max()-mx0+1); H=round((yy.max()-my0+1)*s); oy=64-H
x0,y0,x1,y1=map(int,sys.argv[1:5]); Pp=np.array(PAL,float)
def ch(X,Y):
    X=int(mx0+X/s); Y=int(my0+(Y-oy)/s)
    if not fig[Y,X]: return '.'
    k=int(np.argmin(((Pp[1:]-a[Y,X])**2).sum(1)))+1; return '%x'%k
print('     '+''.join('%-3d'%x if x%2==0 else '   ' for x in range(x0,x1)))
for y in range(y0,y1):
    for sy in (0.25,0.75):
        print(('%3d '%y if sy<0.5 else '    ')+' '.join(ch(x+0.25,y+sy)+ch(x+0.75,y+sy) for x in range(x0,x1)))
