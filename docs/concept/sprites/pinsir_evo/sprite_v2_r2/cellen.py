# Print per spritepixel de natieve modelcellen (k zwart, b donkerbruin, C room, r rood, 3-6 bruintonen, . lucht) naast de sprite-index.
import sys, numpy as np
sys.path.insert(0,'sprite_v2')
from reductie import *
from PIL import Image
cx,cy=kaart(0.3,0.3); OY=63-cy[88]
x0,y0,x1,y1=map(int,sys.argv[1].split(','))
I=np.array(Image.open(sys.argv[2])) if len(sys.argv)>2 else None
def ch(y,x):
    if BG[y,x]: return '.'
    if K[y,x]==1: return 'k'
    if K[y,x]==2: return 'b'
    if K[y,x] in (7,8,11): return 'C'
    if K[y,x] in (9,10): return 'r'
    return str(K[y,x])
inv={}
for y in range(H):
    for x in range(W): inv.setdefault((cy[y]+OY,cx[x]),[]).append((y,x))
for sy in range(y0,y1):
    row=[]
    for sx in range(x0,x1):
        cl=sorted(inv.get((sy,sx),[]))
        ys=sorted(set(c[0] for c in cl)); xs=sorted(set(c[1] for c in cl))
        g=''.join(''.join(ch(y,x) for x in xs) for y in ys)
        row.append(g.ljust(4))
    print('%2d '%sy+' '.join(row)+('   |'+' '.join('%2d'%v for v in I[sy,x0:x1]) if I is not None else ''))
print('   '+' '.join(str(x).ljust(4) for x in range(x0,x1)))
