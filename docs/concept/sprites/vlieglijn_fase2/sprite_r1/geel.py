# Gele componenten in het natieve model -> grootte (natieve px en spritepx) en bbox in spritecoordinaten; telt ook in de sprite.
import numpy as np,sys
from lab import label
grp=np.load('ngrp.npy'); X0,Y0,fx,fy,OX,OY=21,12,109/56,123/63,4,1
lab,n=label(grp=='y')
for k in range(1,n+1):
    yy,xx=np.where(lab==k)
    sx=(xx-X0)/fx+OX; sy=(yy-Y0)/fy+OY
    print(f'model geel {k:2d}: {len(xx):3d} nat.px = {len(xx)/fx/fy:4.1f} spritepx, x {sx.min():5.1f}-{sx.max()+1/fx:5.1f}, y {sy.min():5.1f}-{sy.max()+1/fy:5.1f}')
if len(sys.argv)>1:
    a=np.loadtxt(sys.argv[1],dtype=int); lab2,n2=label(np.isin(a,[12,13]))
    for k in range(1,n2+1):
        yy,xx=np.where(lab2==k); print(f'sprite geel {k:2d}: {len(xx)} px, x {xx.min()}-{xx.max()}, y {yy.min()}-{yy.max()}')
