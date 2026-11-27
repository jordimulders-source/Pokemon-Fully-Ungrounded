# python3 dekking.py raster x0 y0 x1 y1 : per pixel sprite-teken | modeldekking 0-9
import sys; from lib import *
R=lees(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6]); C=dekking()
print('   '+''.join(str(x%10) for x in range(x0,x1))+'   '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1):
    print('%2d '%y+''.join(R[y][x0:x1])+'   '+''.join('.' if C[y,x]<0.05 else str(min(9,int(C[y,x]*10))) for x in range(x0,x1)))
