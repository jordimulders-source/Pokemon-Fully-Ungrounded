# punt.py x0 y0 x1 y1 : modelcel in het midden van elke spritepixel (puntmonster) -> letter, naast raster.txt
import sys, numpy as np, geom, raster2png
cls=np.load('cls.npy'); N=geom.N
PAL={k:v for k,v in raster2png.PAL.items() if k!='.'}
PAL['h']=(120,152,184)
x0,y0,x1,y1=map(int,sys.argv[1:5]); R=raster2png.lees(sys.argv[5] if len(sys.argv)>5 else 'raster.txt')
def letter(i,j,dx=0.5,dy=0.5):
    x=geom.X0+(i+dx-geom.OX)/geom.F; y=geom.Y0+(j+dy-geom.OY)/geom.F
    cx,cy=int(x),int(y)
    if geom.BG[cy,cx]: return '.'
    c=N[cy,cx]
    if cls[cy,cx]==16: return 'Y'
    if cls[cy,cx]==17: return 'P'
    if cls[cy,cx]==18: return 'W'
    return min(PAL,key=lambda k:sum((a-b)**2 for a,b in zip(PAL[k],c)) if k not in 'YPW' else 1e9)
print('    '+''.join(str(i%10) for i in range(x0,x1))+'   '+''.join(str(i%10) for i in range(x0,x1)))
for j in range(y0,y1):
    print('%2d  '%j+''.join(letter(i,j) for i in range(x0,x1))+'   '+R[j][x0:x1])
