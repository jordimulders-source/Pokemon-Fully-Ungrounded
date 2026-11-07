# r20a: C en D samengevoegd (nerf in D); C = middentint baardjes, E = zwartbruin sprietvlak.
# Baardjes steil (links '/', rechts '\', periode 3) in C op E; buitenrand blijft 1/2; nerf D de lichtste lijn.
import os
H=os.path.dirname(os.path.abspath(__file__))
R=[list(l.rstrip('\n')) for l in open(os.path.join(H,'basis.txt'))]
Z=set(tuple(map(int,l.split(','))) for l in open(os.path.join(H,'..','spriet_zone.txt')))
F={}
def put(x,y,c): F[(x,y)]=c; R[y][x]=c
for y in range(64):
    for x in range(64):
        if R[y][x]=='C': put(x,y,'D')
def ch(x,y): return R[y][x] if 0<=x<64 and 0<=y<64 else '.'
for (x,y) in Z:
    if R[y][x] not in '16': continue
    nb=[ch(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
    if '.' in nb: put(x,y,'1'); continue
    s=(x+y//3)%3==0 if x<24 else (x-y//2)%3==1
    put(x,y,'C' if s else 'E')
W={}
for (x,y),c in F.items(): W.setdefault(y,[]).append((x,c))
