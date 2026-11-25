# Keurder r4: cirkelfit op de vrije buitenrand van de bollen (pixelcentra van randpixels die aan transparant grenzen).
from PIL import Image; import numpy as np, sys
a=np.array(Image.open('docs/concept/sprites/satelliet_fase3/sprite/r4/sprite.png'))
op=a>0
def edge(x0,x1,y0,y1):
    pts=[]
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if op[y,x]:
                nb=[op[y+dy,x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else False for dy,dx in((0,1),(1,0),(0,-1),(-1,0))]
                if not all(nb): pts.append((x,y))
    return np.array(pts,float)
def fit(p):
    A=np.c_[2*p[:,0],2*p[:,1],np.ones(len(p))]; b=(p**2).sum(1)
    cx,cy,c=np.linalg.lstsq(A,b,rcond=None)[0]; r=np.sqrt(c+cx*cx+cy*cy)
    return cx,cy,r,np.hypot(p[:,0]-cx,p[:,1]-cy)-r
# vensters (x0,x1,y0,y1) en hoekbereik (graden, 0=rechts, 90=onder) waar de bol vrij ligt
B={'grote oogbol LO':((9,24,43,55),(60,270)),
   'bol RB':((44,57,17,28),(-150,30)),
   'kleine oogbol L':((15,24,26,33),(100,260)),
   'kleine oogbol R':((45,56,34,42),(-60,140))}
for n,(w,(h0,h1)) in B.items():
    p=edge(*w)
    cx,cy,r,res=fit(p)
    ang=np.degrees(np.arctan2(p[:,1]-cy,p[:,0]-cx))
    ang=np.where(ang<h0,ang+360,ang); sel=(ang>=h0)&(ang<=h1)
    q=p[sel]; cx,cy,r,res=fit(q)
    i=np.abs(res).argmax()
    print(f'{n}: c=({cx:.1f},{cy:.1f}) r={r:.2f} n={len(q)} max|afw|={abs(res).max():.2f} bij {tuple(q[i].astype(int))}, rms={np.sqrt((res**2).mean()):.2f}')
    for (x,y),e in zip(q.astype(int),res):
        if abs(e)>0.8: print('   ',x,y,round(e,2))
