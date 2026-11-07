# sprieten: zwart vlak, lichte nerf, baarden als doorlopende schuine streepjes (ongelijke afstand 2-3),
# licht (5) bij de nerf en tussentint (3) verder weg; belichte bovenrand donkerbruin (2)
Z=set(tuple(map(int,l.split(','))) for l in open('spriet_zone.txt'))
def boog(x0,y0,x1,y1,p):
    pts=[]; st=1 if x1>x0 else -1
    for x in range(x0,x1+st,st):
        f=abs(x-x0)/abs(x1-x0); y=round(y0+(y1-y0)*f**p)
        if pts and y-pts[-1][1]>1:
            for yy in range(pts[-1][1]+1,y): pts.append((x-st,yy))
        pts.append((x,y))
    return pts
NERF=[p for p in boog(3,18,19,28,1.5)+boog(51,19,29,29,1.7) if p in Z]
N=set(NERF); nerfy={}
for x,y in NERF: nerfy.setdefault(x,[]).append(y)
def buiten(x,y): return not (0<=x<64 and 0<=y<64) or r[y][x]=='.'
def rand(x,y): return [(dx,dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if (x+dx,y+dy) not in Z]
SPATIE={0,2}                      # streep op fase 0 en 2 van 5: afstand 2-3-2-3
for (x,y) in Z:
    rd=rand(x,y)
    if (x,y) in N: c='C'
    elif rd:
        lit=any(buiten(x+dx,y+dy) and dy<0 for dx,dy in rd)
        c='2' if lit else '1'
    else:
        top=min(nerfy.get(x,[99]))
        rib=((x - y) % 3 == 0)                                         # ribben schuin zoals in het model (beide sprieten)
        c='4' if rib else '1'                                             # één tint per rib
    r[y][x]=c
