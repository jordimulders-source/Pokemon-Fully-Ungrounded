"""Bouwt data/layouts/Route135/map.bin (deterministisch, vaste seed).
Gebruik: python3 tools/grounded/maptools/route135.py [voorbeeld.png]
Events (items, trainers, warps) staan in data/maps/Route135/map.json; houd EVENTS hieronder gelijk."""
import os, sys, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from snowlib import *
import random
W,H=60,40
m=M(W,H); rnd=random.Random(135)
for y in range(H):
    for x in range(W):
        if rnd.random()<0.07: m.put(x,y,rnd.choice(['snow_dots','tuft0','tuft1','tuft3','snow_light','tuft5']))
L1=set(rect(-1,-1,W,21))-set(rect(12,12,36,21))
L2=set(rect(-1,-1,W,11))-set(rect(44,6,W,11))
L3=set(rect(13,-1,35,11))
terrace(m,L1); terrace(m,L2); terrace(m,L3,face=7)
EVENTS={(14,33),(24,24),(55,9),(55,10),(34,36),(38,19),(44,19),(33,3),(55,2),(10,13),(6,12),(36,34),(4,28)}
def free(x,y): return 0<=x<W and 0<=y<H and m.col[y][x]==0 and m.elev[y][x]==3
# bronvijver en waterval (3 breed, 3 terrassen hoog)
m.water(set(rect(19,1,29,3))|set(rect(20,4,28,4)),extra=set(rect(21,5,27,5)))
lake=smooth(set(blob(24,25,11.5,8,seed=7,rough=0.12))|set(blob(24,15,8.5,4.5,seed=2,rough=0.1))|set(rect(18,12,30,14))|set(blob(15,30,5,3,seed=12,rough=0.1)))
lake={c for c in lake if 12<=c[1]<=33 and 4<=c[0]<=40}
for _ in range(4):
    lake={c for c in lake if sum((c[0]+dx,c[1]+dy) in lake for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))>=2 or c[1]<=13}

m.water(lake)
inlets=[(x,y) for (x,y) in lake if (x,y+1) not in lake and (x-1,y) not in lake and (x+1,y) not in lake and (x,y-1) in lake]
print('inham(men):',sorted(inlets))
fall(m,21,5,11,w=7)
# grot (Coldstep, uitgang) in de L2-rand links
for x,n in zip((5,6,7),('cave_l','cave_door','cave_r')): m.put(x,11,n,1)
for x,n in zip((5,6,7),('cliff_front_a','cliff_front_b','cliff_front_c')): m.put(x,10,n,1)
m.put(6,11,'cave_door',0,0)
# trappen
def stairs(x0,y0,w=3,h=2):
    for x in range(x0,x0+w):
        for y in range(y0,y0+h): m.put(x,y,'stairs',0)
stairs(6,20); stairs(40,20); stairs(50,4)
# huisje
HOUSE=set(rect(54,6,57,9))
# pad
path=set(rect(5,12,7,19))|set(rect(5,22,7,36))|set(rect(5,35,52,36))|set(rect(50,35,52,H-1))|set(rect(40,22,42,34))|set(rect(40,12,42,19))|set(rect(40,12,52,14))|set(rect(50,6,52,11))|set(rect(46,2,54,3))|set(rect(53,10,56,11))
path-= {c for c in path if m.g[c[1]][c[0]]==N['stairs']}
path={c for c in path if free(*c)}
autopath(m,path,'deep')
# hoog gras
for c,seed in [((10,16,4,3),1),((13,27,4,4),2),((34,29,4,3.5),3),((46,28,5,4),4),((54,17,4,3),5),((30,38,5,2),6),((40,2,3,1.5),8)]:
    for (x,y) in blob(*c,seed=seed):
        if free(x,y) and (x,y) not in path and m.g[y][x] not in (N['stairs'],):
            m.put(x,y,'grass_snow',0)
# Birch-steen (2x2) aan de oever
for dx in range(2):
    for dy in range(2): m.put(34+dx,34+dy,f'boulder_{dx}{dy}',1)
# randbossen
def pine(x,y,g=None):
    ok=all((x+dx,y+dy) not in path and (free(x+dx,y+dy) or m.g[y+dy][x+dx] in (N['grass_snow'],)) for dx in range(2) for dy in range(3) if 0<=x+dx<W and 0<=y+dy<H)
    if ok: m.pine(x,y,green=(rnd.random()<0.35) if g is None else g)
def okf(x,y):
    return 0<=x<W and 0<=y<H and (x,y) not in path and (x,y) not in EVENTS and (free(x,y) or m.g[y][x] in PINE)
PINE={N[k] for k in N if 'pine' in k}|{N['grass_snow']}|{N[k] for k in N if k.startswith('tuft') or k.startswith('snow')}
REG=set(rect(0,0,W-1,1))|set(rect(0,12,3,H-1))|set(rect(0,H-4,W-1,H-1))|set(rect(W-4,0,W-1,H-1))|set(rect(0,0,11,9))|set(rect(14,0,17,3))|set(rect(30,0,35,3))|set(rect(36,0,43,1))
REG-=set(rect(53,5,59,12))
hforest(m,REG,okf,path)
# doorlopende bosstrook langs alle kaartranden (verbergt de uiteinden van de bergwanden)
def okb(x,y):
    return 0<=x<W and 0<=y<H and (x,y) not in path and (x,y) not in EVENTS and (x,y) not in HOUSE and m.elev[y][x]!=1 \
        and m.g[y][x] not in (N['stairs'],N['cave_door'])
BAND=set(rect(0,0,3,H-1))|set(rect(W-4,0,W-1,H-1))|set(rect(0,0,17,1))|set(rect(30,0,W-1,1))|set(rect(0,H-2,W-1,H-1))
hforest(m,BAND,okb,path)
for (x,y) in HOUSE:
    m.put(x,y,f'house_blue_{x-54}{y-6}',0 if (x,y)==(55,9) else 1)
for (x,y) in [(15,1),(31,1),(33,0),(2,1),(9,0),(40,0),(56,0),(44,13),(56,12),(12,13),(47,23),(56,24),(10,24),(14,33),(3,26),
              (1,4),(4,6),(7,2),(10,5),(2,8),(8,7),(11,1),(14,4),(16,6),(30,5),(32,4),(17,2),(29,1),(37,4),(42,1),
              (45,15),(47,13),(53,14),(55,16),(38,15),(36,17),(57,18),(9,14),(12,17),(1,17),
              (3,23),(12,23),(38,24),(45,25),(55,27),(36,30),(28,34),(42,36),(9,33),(20,34),(58,34)]:
    pine(x,y)
# rotsen en decor
decor=[(11,6,'rock_snow'),(3,7,'rock_cluster'),(16,15,'rock_snow2'),(37,16,'ice_crystal'),(46,17,'rock_snow3'),(55,21,'ice_rock'),
       (44,31,'log'),(9,30,'stump'),(38,7,'rock_snow'),(14,8,'ice_chunks'),(31,6,'bush_snow'),(18,2,'ice_crystal2'),
       (29,29,'rock_snow4'),(36,23,'bush_snow'),(52,26,'rock_cluster'),(24,37,'bush_snow'),(3,33,'ice_rock2'),(48,20,'snowball')]
for x,y,n in decor:
    if free(x,y) and (x,y) not in path: m.put(x,y,n,1)
for (x,y) in [(12,20),(13,20),(38,26),(39,27),(54,33),(55,33),(26,5),(27,5)]:
    if free(x,y) and (x,y) not in path and m.g[y][x]!=N['grass_snow']: m.put(x,y,'flowers_blue',0)
def clear_near(x,y,r=1):
    for dx in range(-r,r+1):
        for dy in range(-r,r+1):
            c=(x+dx,y+dy)
            if c in path or c in EVENTS: return False
            if 0<=c[0]<W and 0<=c[1]<H and m.g[c[1]][c[0]]==N['stairs']: return False
    return True
BLOCK=['rock_snow','rock_snow2','rock_cluster','rock_snow3','rock_snow4','ice_rock','ice_rock2','ice_chunks','ice_crystal','ice_crystal2','snowball','snowball2','log','bush_snow','stump']
SOFT=['flowers_blue','flowers_pink','tuft2','tuft4','tuft6','tuft7','tuft8','tuft9','snow_deep','snow_deep2']
cands=[(x,y) for y in range(H) for x in range(W) if free(x,y) and m.g[y][x]!=N['grass_snow'] and (x,y) not in path]
rnd.shuffle(cands)
nb=0
for (x,y) in cands:
    if not free(x,y): continue
    r=rnd.random()
    if r<0.06 and clear_near(x,y,1):
        m.put(x,y,rnd.choice(BLOCK),1); nb+=1
    elif r<0.16 and clear_near(x,y,0):
        m.put(x,y,rnd.choice(SOFT),0)
# bereikbaarheid controleren
from collections import deque
def walk(x,y): return 0<=x<W and 0<=y<H and m.col[y][x]==0 and m.elev[y][x] in (0,3)
def reach(s):
    seen={s}; q=deque([s])
    while q:
        x,y=q.popleft()
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            n=(x+dx,y+dy)
            if n not in seen and walk(*n) and n not in EVENTS-{(6,12)}: seen.add(n); q.append(n)
    return seen
R=reach((6,12))
adj=lambda p: any((p[0]+dx,p[1]+dy) in R for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
print('decor',nb,'uitgang',(51,39) in R,{p:(free(*p) or m.g[p[1]][p[0]]==N['cave_door'],adj(p)) for p in EVENTS})
m.elev[33][14]=3   # Swimmer staat in de inham op hoogte 3, zodat hij spelers op het land kan zien
open(os.path.join(REPO,'data/layouts/Route135/map.bin'),'wb').write(struct.pack(f'<{W*H}H',*m.bin()))
if len(sys.argv)>1: m.img().save(sys.argv[1])
