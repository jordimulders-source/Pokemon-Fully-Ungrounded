# r17c: sprietbaardjes als doorlopende steile strepen (tan 6 op zwart, periode 3), richting gemeten op het model:
# links '/' (±75 graden, helling 3), rechts '\' (±63 graden, helling 2). Rand (2/1 op de buitenrand) en nerf C blijven;
# geen streep 4-naast de nerf. Linkeroog: onderste rij/linkeronderhoek terug naar het model (y33-39).
import os
H=os.path.dirname(os.path.abspath(__file__))
R=[l.rstrip('\n') for l in open(os.path.join(H,'basis.txt'))]
Z=set(tuple(map(int,l.split(','))) for l in open(os.path.join(H,'..','spriet_zone.txt')))
PH_L=int(os.environ.get('PH_L',0)); PH_R=int(os.environ.get('PH_R',1))
def ch(x,y): return R[y][x] if 0<=x<64 and 0<=y<64 else '.'
F={}
for (x,y) in Z:
    c=R[y][x]
    if c not in '14': continue
    nb=[ch(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
    if '.' in nb or 'C' in nb: F[(x,y)]='1'; continue
    if x<24: s=(x+y//3)%3==PH_L
    else: s=(x-y//2)%3==PH_R
    F[(x,y)]='6' if s else '1'
# linkeroog
F[(16,38)]='7'; F[(17,39)]='7'; F[(19,40)]='A'
W={}
for (x,y),c in F.items(): W.setdefault(y,[]).append((x,c))
