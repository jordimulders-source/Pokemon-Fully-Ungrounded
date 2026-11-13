# kaart.py x0 y0 x1 y1: raster (basis) naast modelklasse per spritepixel: # lijn (fo>=.3), K zwart (L<60), D (60-115), C (115-150), B (150-190), A (190-232), W
import sys,numpy as np,pal
R=pal.load(sys.argv[5] if len(sys.argv)>5 else 'basis_L1.txt'); d=np.load('meet5.npz'); L=d['med'].mean(2); fo=d['fo']; sil=d['sil']
def k(x,y):
    if not sil[y,x]: return '.'
    if fo[y,x]>=.3: return '#'
    l=L[y,x]; return 'K' if l<60 else 'D' if l<115 else 'C' if l<150 else 'B' if l<190 else 'A' if l<232 else 'W'
x0,y0,x1,y1=map(int,sys.argv[1:5])
print('    '+''.join(str(x%10) for x in range(x0,x1))+'   '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print(f'{y:2d}  '+R[y][x0:x1]+'   '+''.join(k(x,y) for x in range(x0,x1)))
