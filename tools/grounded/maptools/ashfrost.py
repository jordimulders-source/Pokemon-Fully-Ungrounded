"""Bouwt data/layouts/AshfrostTown/map.bin: Ashfrost ligt in een kloof boven op de berg (een beetje zoals Sootopolis).
Een hoge rotswand rondom (bos erop), het dorp op een ring langs de wand, en in het midden twee lagen omlaag
naar een meertje met een strandje. Pokémon Center centraal boven het meer, Mart in een hoek.
Tileset: snow_town (zie snow_tileset.py --town). Ingang: een smalle kloof onderaan (x 20-23), warp naar Route 136.
Gebruik: python3 tools/grounded/maptools/ashfrost.py [voorbeeld.png]"""
import os, sys, struct, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from snowlib import *
use_tileset('snow_town')
W,H=44,34
m=M(W,H,base='cliff_c'); rnd=random.Random(2024)
STL,STR=175,207   # stenen Hoenn-trap (General), zoals op Route 136
ALL={(x,y) for x in range(-4,W+4) for y in range(-4,H+6)}
inmap=lambda c: 0<=c[0]<W and 0<=c[1]<H

# --- vormen: kloof (dorp), ring 1 lager, strand 2 lager, meer ---
crater=smooth(set(blob(22,15.5,19.5,13.2,seed=11,rough=0.07)))|set(rect(20,26,23,H+5))   # + smalle kloof als ingang
pit1=smooth(set(blob(22,18.5,11,6.8,seed=5,rough=0.06)))
pit0=smooth(set(blob(22,19.5,8,4.6,seed=8,rough=0.06)))
lake=smooth(set(blob(23,20.6,6.2,3.1,seed=3,rough=0.10)))
RIM=ALL-crater
terrace(m,ALL-pit0,face=2)          # strand + meer liggen 2 lagen onder het dorp
terrace(m,ALL-pit1,face=2)
terrace(m,RIM,face=4)               # hoge kloofwand
for c in list(pit0):
    if inmap(c): m.put(*c,'snow',0)
m.water({c for c in lake if inmap(c)})

def top(S,x): return min(y for (xx,y) in S if xx==x)
# trappen: dorp -> ring (midden, onder het Pokémon Center), ring -> strand (links, zodat je over de ring loopt)
S1=(21,top(pit1,21)-2); S0=(15,top(pit0,15)-2)
for (sx,sy) in (S1,S0):
    for y in (sy,sy+1): m.put(sx,y,STL,0); m.put(sx+1,y,STR,0)
print('trappen',S1,S0)

# --- gebouwen (alleen op de dorpsvloer) ---
FLOOR=lambda c: inmap(c) and m.g[c[1]][c[0]]==N['cliff_c'] and m.col[c[1]][c[0]]==0
def building(name,x0,y0,w,h,door):
    cells=[(x0+dx,y0+dy) for dx in range(w) for dy in range(h)]
    bad=[c for c in cells+[(x0+door[0],y0+door[1]+1)] if not FLOOR(c)]
    assert not bad,(name,bad)
    for dy in range(h):
        for dx in range(w):
            m.put(x0+dx,y0+dy,f'{name}_{dx}{dy}',0 if (dx,dy)==door else 1)
    return (x0+door[0],y0+door[1])
DOORS={}
DOORS['pc']=building('pc',19,5,5,5,(2,4))              # centraal boven het meer, deur (21,9)
DOORS['mart']=building('mart',7,21,4,4,(2,3))          # linksonder in de hoek
DOORS['house_blue']=building('house_blue',6,8,4,4,(1,3))
DOORS['house_yellow']=building('house_yellow',33,7,4,4,(1,3))
DOORS['house_pink']=building('house_pink',33,19,4,4,(2,3))
print('deuren',DOORS)

# --- paden: een ring om de kuil, met aftakkingen naar de deuren en de kloof ---
ring=set(blob(22,17.2,14.6,9.8,seed=5,rough=0.04))-set(blob(22,17.2,12.6,7.8,seed=5,rough=0.04))
spokes=set()
for (dx_,dy_) in DOORS.values():
    x,y=dx_,dy_+1
    for _ in range(12):                   # recht naar beneden/boven tot op de ring
        if (x,y) in ring: break
        spokes|={(x,y),(x+1,y)}; y+=1 if y<17 else -1
spokes|=set(rect(20,24,23,H-1))|set(rect(21,10,22,S1[1]-1))
path={c for c in ring|spokes if FLOOR(c)}
autopath(m,path,'path_stone')

# --- bewoners/objecten (vrijhouden) ---
FISH=(22,top(lake,22)-1)
EVENTS={FISH,(12,14),(28,11),(17,27),(30,26),(33,15)}
SNOWMAN=(11,14)
m.put(*SNOWMAN,'snowman',1)
print('visser',FISH)

# --- bos op de kloofrand, dennen en keien ---
def okb(x,y):
    return inmap((x,y)) and (x,y) not in path and (x,y) not in EVENTS and m.g[y][x]==N['cliff_c'] and m.col[y][x]==0 and (x,y) in RIM
EDGE={c for c in RIM if inmap(c) and not any((c[0]+dx,c[1]+dy) in crater for dx in (-1,0,1) for dy in (-1,0,1,2))}
hforest(m,EDGE,okb,path)
def okd(x,y): return FLOOR((x,y)) and (x,y) not in path and (x,y) not in EVENTS
def pine(x,y,g):
    cells=[(x+dx,y+dy) for dx in range(2) for dy in range(3)]
    if all(okd(*c) for c in cells): m.pine(x,y,green=g); return True
    return False
for (x,y,g) in [(4,13,True),(5,17,True),(14,6,True),(26,5,False),(29,6,True),(38,12,True),(38,23,True),(26,26,True),(13,25,False),(16,3,True),(9,4,False),(34,3,True)]: pine(x,y,g)
for (x,y) in [(15,8),(30,9),(10,18),(36,16)]:
    if all(okd(x+dx,y+dy) for dx in (0,1) for dy in (0,1)):
        for dx in (0,1):
            for dy in (0,1): m.put(x+dx,y+dy,f'boulder_{dx}{dy}',1)
# bloemen en gras: de ring rond het meer is groen en bloeit (het beschutte 'paradijs'), het strandje ook
for c in sorted(pit1):
    if not inmap(c): continue
    x,y=c
    if m.g[y][x] in (N['cliff_c'],N['snow']) and m.col[y][x]==0 and c not in EVENTS and c not in path:
        r=rnd.random()
        if r<0.30: m.put(x,y,rnd.choice(['flowers_blue','flowers_pink']),0)
        elif r<0.55: m.put(x,y,'grass_green',0)
        elif r<0.65: m.put(x,y,rnd.choice(['tuft0','tuft1','tuft3']),0)
for c in sorted(crater-pit1):
    if okd(*c) if inmap(c) else False:
        if rnd.random()<0.06: m.put(*c,rnd.choice(['tuft2','tuft5','snow_dots','flowers_blue']),0)

# --- bereikbaarheid ---
from collections import deque
def walk(x,y): return inmap((x,y)) and m.col[y][x]==0 and m.elev[y][x]==3
start=(21,H-1); seen={start}; q=deque([start])
while q:
    x,y=q.popleft()
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        n=(x+dx,y+dy)
        if n not in seen and walk(*n) and n not in EVENTS: seen.add(n); q.append(n)
print('deuren bereikbaar:',{k:(d[0],d[1]+1) in seen for k,d in DOORS.items()})
print('events bereikbaar:',{p:any((p[0]+dx,p[1]+dy) in seen for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) for p in sorted(EVENTS)})
print('strand bereikbaar:',(FISH[0]-1,FISH[1]) in seen)
d=os.path.join(REPO,'data/layouts/AshfrostTown')
if os.path.isdir(d):
    open(os.path.join(d,'map.bin'),'wb').write(struct.pack(f'<{W*H}H',*m.bin()))
if len(sys.argv)>1: m.img().save(sys.argv[1])
