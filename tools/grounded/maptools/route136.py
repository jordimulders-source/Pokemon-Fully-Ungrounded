"""Bouwt data/layouts/Route136/map.bin: een bergklim van west naar oost en omhoog naar het noorden.
Ingang bovenaan links (x 10-13, verbonden met de uitgang van Route 135), uitgang bovenaan rechts (x 49, bergpas naar Ashfrost).
Gebruik: python3 tools/grounded/maptools/route136.py [voorbeeld.png]"""
import os, sys, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from snowlib import *
import random
W,H=60,44
m=M(W,H); rnd=random.Random(136)
for y in range(H):
    for x in range(W):
        if rnd.random()<0.06: m.put(x,y,rnd.choice(['snow_dots','tuft0','tuft1','tuft3','snow_light','tuft5']))
# events (vrij houden): trainers, items, deuren
EVENTS={(17,13),(16,29),(25,21),(33,10),(31,4),(43,6),(49,2),(51,20),(52,18),(27,2),(51,25),(51,26),(8,8),(36,40),(13,40)}
# --- terrassen: dal (L0) -> L1 -> hoge rotswand -> L2-richel -> L3-richel -> top (L4) ---
L1=set(rect(18,-1,55,25))|set(rect(30,26,36,28))
L2=set(rect(26,-1,55,17))|set(rect(34,18,38,19))
L3=set(rect(36,-1,55,10))
L4=set(rect(46,-1,55,5))
terrace(m,L1); terrace(m,L2,face=4); terrace(m,L3,face=3); terrace(m,L4)
# rotsheuvels in het dal en de wei
for r in (set(rect(4,12,8,17)),set(rect(27,34,33,38)),set(rect(42,29,47,33)),set(rect(13,30,17,33))): terrace(m,r)
def free(x,y): return 0<=x<W and 0<=y<H and m.col[y][x]==0 and m.elev[y][x]==3
STL,STR=175,207   # Hoenn-stenen trap uit de General-tileset (zoals Route 119): links, rechts
STAIRS={STL,STR}
def stairs(x0,y0,h=2):
    for y in range(y0,y0+h): m.put(x0,y,STL,0); m.put(x0+1,y,STR,0)
stairs(21,24); stairs(29,14,4); stairs(38,8,3); stairs(48,4)
# verborgen grot in de L1-rand, rechtsonder in de wei (van het pad af)
for x,n in zip((50,51,52),('cliff_front_a','cliff_front_b','cliff_front_c')): m.put(x,24,n,1)
for x,n in zip((50,51,52),('cave_l','cave_door','cave_r')): m.put(x,25,n,1)
m.put(51,25,'cave_door',0,0)
# --- pad (zigzag omhoog) ---
path=(set(rect(10,0,12,9))|set(rect(10,8,16,10))|set(rect(14,8,16,18))|set(rect(10,16,16,18))|set(rect(10,16,12,28))|set(rect(10,26,23,28))|set(rect(21,18,23,23))|set(rect(21,18,30,20))
      |set(rect(28,11,30,13))|set(rect(28,11,40,13))|set(rect(38,6,40,7))|set(rect(38,6,49,7))
      |set(rect(48,0,50,5)))
path-= {c for c in path if m.g[c[1]][c[0]] in STAIRS}
path={c for c in path if free(*c)}
autopath(m,path,'deep')
# grote keien (2x2) als obstakels op de plateaus
for (bx,by) in [(33,19),(44,19),(24,2),(31,8),(42,1),(52,1),(36,29),(30,37)]:
    if all(free(bx+dx,by+dy) and (bx+dx,by+dy) not in path and (bx+dx,by+dy) not in EVENTS for dx in (0,1) for dy in (0,1)):
        for dx in (0,1):
            for dy in (0,1): m.put(bx+dx,by+dy,f'boulder_{dx}{dy}',1)
# --- Keccles: een rij rotsen met precies een leeg gat (50,21), het item erachter ---
for x in range(48,56):
    if x!=51: m.put(x,20,'rock_snow2' if x%2 else 'rock_cluster',1)
for y in (18,19): m.put(47,y,'rock_snow',1)
# --- bossen ---
def okf(x,y):
    return 0<=x<W and 0<=y<H and (x,y) not in path and (x,y) not in EVENTS and m.elev[y][x]!=1 and \
        m.g[y][x] not in STAIRS|{N['cave_door']} and (free(x,y) or m.g[y][x]==N['grass_snow'])
REG=set(rect(4,2,7,10))|set(rect(4,19,7,25))|set(rect(14,2,17,6))|set(rect(13,21,17,24))|set(rect(4,30,9,41))|set(rect(20,30,31,33))|set(rect(38,36,47,41))|set(rect(18,2,21,15))|set(rect(34,22,41,23))
hforest(m,REG,okf,path)
def okb(x,y):
    return 0<=x<W and 0<=y<H and (x,y) not in path and (x,y) not in EVENTS and m.elev[y][x]!=1 and \
        m.g[y][x] not in STAIRS|{N['cave_door']}
BAND=set(rect(0,0,3,H-1))|set(rect(W-4,0,W-1,H-1))|set(rect(0,0,9,1))|set(rect(14,0,47,1))|set(rect(52,0,W-1,1))|set(rect(0,H-2,W-1,H-1))
hforest(m,BAND,okb,path)
# hoog gras (niet direct tegen de randbomen aan)
HT={N[k] for k in N if k.startswith('htree')}
for c,seed in [((6,10,2.5,6),1),((14,36,5,3),2),((33,34,5,3),3),((46,31,5,3),4),((24,6,4,3),5),((33,4,3,2.5),6),((40,2,3,1.5),7),((44,21,4,1.5),8),((7,30,2.5,4),9)]:
    for (x,y) in blob(*c,seed=seed):
        if free(x,y) and (x,y) not in path and m.g[y][x]!=N['cliff_c'] and not any(0<=x+dx<W and 0<=y+dy<H and m.g[y+dy][x+dx] in HT for dx in (-1,0,1) for dy in (-1,0,1)): m.put(x,y,'grass_snow',0)
# losse dennen en decor
def pine(x,y,g=None):
    cells=[(x+dx,y+dy) for dx in range(2) for dy in range(3)]
    if all(free(*c) and c not in path and c not in EVENTS for c in cells): m.pine(x,y,green=rnd.random()<0.4 if g is None else g)
for (x,y) in [(15,20),(13,33),(26,21),(36,14),(52,11),(44,2),(20,37),(34,26),(25,34),(38,3),(54,28),(27,8),(32,1),(16,38),(41,27),(48,35)]: pine(x,y)
def clear_near(x,y,r=1):
    for dx in range(-r,r+1):
        for dy in range(-r,r+1):
            c=(x+dx,y+dy)
            if c in path or c in EVENTS: return False
            if 0<=c[0]<W and 0<=c[1]<H and m.g[c[1]][c[0]] in STAIRS|{N['cave_door']}: return False
    return True
BLOCK=['rock_snow','rock_snow2','rock_cluster','rock_snow3','rock_snow4','ice_rock','ice_rock2','ice_chunks','ice_crystal','ice_crystal2','snowball','log','bush_snow','stump']
SOFT=['flowers_blue','flowers_pink','tuft2','tuft4','tuft6','tuft7','tuft8','tuft9','snow_deep','snow_deep2']
# doorgangen die vrij moeten blijven van decor (naar Keccles en de grot, de oostkant van L1)
KEEP=set(rect(36,20,39,21))|set(rect(49,21,53,23))
cands=[(x,y) for y in range(H) for x in range(W) if free(x,y) and m.g[y][x]!=N['grass_snow'] and (x,y) not in path and (x,y) not in KEEP]
rnd.shuffle(cands)
for (x,y) in cands:
    if not free(x,y): continue
    r=rnd.random()
    if r<0.07 and clear_near(x,y,1): m.put(x,y,rnd.choice(BLOCK),1)
    elif r<0.17 and clear_near(x,y,0): m.put(x,y,rnd.choice(SOFT),0)
# bereikbaarheid
from collections import deque
def walk(x,y): return 0<=x<W and 0<=y<H and m.col[y][x]==0 and m.elev[y][x] in (0,3)
seen={(11,0)}; q=deque([(11,0)])
while q:
    x,y=q.popleft()
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        n=(x+dx,y+dy)
        if n not in seen and walk(*n) and n not in EVENTS: seen.add(n); q.append(n)
adj=lambda p: any((p[0]+dx,p[1]+dy) in seen for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
print('uitgang (49,0):',(49,0) in seen or adj((49,0)),{p:(free(*p) or m.g[p[1]][p[0]]==N['cave_door'],adj(p)) for p in sorted(EVENTS)})
open(os.path.join(REPO,'data/layouts/Route136/map.bin'),'wb').write(struct.pack(f'<{W*H}H',*m.bin())) if os.path.isdir(os.path.join(REPO,'data/layouts/Route136')) else None
if len(sys.argv)>1: m.img().save(sys.argv[1])
