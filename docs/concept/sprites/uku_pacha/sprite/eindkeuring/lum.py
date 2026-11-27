# python3 lum.py raster x0 y0 x1 y1 : sprite | modelhelderheid per pixel in tientallen (gem), '.'=achtergrond
import sys; from lib import *
R=lees(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6]); L=lum_model(); C=dekking()
print('   '+''.join(str(x%10) for x in range(x0,x1))+'   '+' '.join('%2d'%(x%100) for x in range(x0,x1)))
for y in range(y0,y1):
    print('%2d '%y+''.join(R[y][x0:x1])+'   '+' '.join(' .' if C[y,x]<0.3 else '%2d'%min(99,int(L[y,x]/2.56)) for x in range(x0,x1)))
