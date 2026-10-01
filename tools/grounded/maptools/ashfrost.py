"""Bouwt data/layouts/AshfrostTown/map.bin: Ashfrost Village ligt in een dal boven op de berg.
Een hoge rotswand rondom (bos erop), het dorp op de bovenste ring, en een slingerpad met trappen
twee lagen omlaag naar een meer met een strandje. Pokémon Center centraal boven het dal.
Tilesets: snow_town_base (primary) + snow_town (secondary), zie snow_tileset.py --town.
Ingang: een smalle kloof linksonder (x 5-8), warp naar Route 136 (coord-triggers op y 33).
Gebruik: python3 tools/grounded/maptools/ashfrost.py [voorbeeld.png]"""
import os, sys, struct, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from snowlib import *
use_tileset('snow_town')
W,H=44,34
m=M(W,H,base='cliff_c'); rnd=random.Random(2024)
ALL={(x,y) for x in range(-4,W+4) for y in range(-4,H+6)}
inmap=lambda c: 0<=c[0]<W and 0<=c[1]<H

# --- vormen: kloof (dorp), weide 1 laag lager, meeroever 2 lagen lager ---
# Strakke vormen (rechthoeken met afgeschuinde hoeken) geven duidelijke, doorlopende klifwanden.
def rrect(x0,y0,x1,y1,cut=2):
    # alleen de bovenhoeken afschuinen: onderhoeken van een kuil worden anders losse klifstukjes
    return {(x,y) for (x,y) in rect(x0,y0,x1,y1) if min(x-x0,x1-x)+(y-y0)>=cut}
GORGE=set(rect(5,30,8,H+5))
crater=rrect(3,5,40,29,0)|GORGE                    # dorp; ingang via een kloof linksonder
pit1=rrect(10,15,33,29,3)                        # weide
pit0=rrect(14,21,31,29,2)                        # meeroever
lake=smooth(set(blob(22.8,25.9,6.9,3.0,seed=3,rough=0.10)))
RIM=ALL-crater
terrace(m,ALL-pit0,face=2)
terrace(m,ALL-pit1,face=2)
terrace(m,RIM,face=4)               # hoge kloofwand
for c in list(pit0):
    if inmap(c): m.put(*c,'snow',0)
m.water({c for c in lake if inmap(c)})

def top(S,x): return min(y for (xx,y) in S if xx==x)
# trappen midden in een rechte klifwand (niet bij een hoek): dorp -> weide links, weide -> meeroever rechts
S1=(17,top(pit1,17)-2); S0=(26,top(pit0,26)-2)
assert all(top(pit1,x)==top(pit1,17) for x in range(15,21)) and all(top(pit0,x)==top(pit0,26) for x in range(25,29))
for (sx,sy) in (S1,S0):
    for y in (sy,sy+1): m.put(sx,y,'hstairs_l',0); m.put(sx+1,y,'hstairs_r',0)
print('trappen',S1,S0)

# --- gebouwen en grote objecten ---
def level(c):
    return 2 if c in pit0 else 1 if c in pit1 else 0
FLOOR=lambda c: inmap(c) and m.g[c[1]][c[0]] in (N['cliff_c'],N['snow']) and m.col[c[1]][c[0]]==0
def obj(name,x0,y0,w,h,door=None,free=()):
    cells=[(x0+dx,y0+dy) for dx in range(w) for dy in range(h)]
    lv={level(c) for c in cells}
    bad=[c for c in cells if not FLOOR(c)]+([] if door is None else [c for c in [(x0+door[0],y0+door[1]+1)] if not FLOOR(c)])
    if os.environ.get('SOFT') and (bad or len(lv)>1): print('PAST NIET',name,bad,lv); return None
    assert not bad and len(lv)==1,(name,bad,lv)
    for dy in range(h):
        for dx in range(w):
            m.put(x0+dx,y0+dy,f'{name}_{dx}{dy}',0 if (dx,dy)==door or (dx,dy) in free else 1)
    return None if door is None else (x0+door[0],y0+door[1])
DOORS={}
DOORS['lodge']=obj('lodge',5,5,5,5,(1,4))              # grote lodge linksboven
DOORS['house_blue']=obj('house_blue',11,6,4,4,(1,3))
DOORS['pc']=obj('pc',19,5,5,5,(2,4))                  # centraal boven het dal
DOORS['house_pink']=obj('house_pink',27,6,4,4,(2,3))
DOORS['house_yellow']=obj('house_yellow',35,6,4,4,(1,3))
DOORS['house_green']=obj('house_green',37,17,4,4,(2,3))
DOORS['mart']=obj('mart',3,20,4,4,(2,3))               # bij de ingang
print('deuren',DOORS)

# --- paden ---
path=set()
def line(a,b,w=2):
    (x0,y0),(x1,y1)=a,b
    for x in range(min(x0,x1),max(x0,x1)+1):
        for y in range(min(y0,y1),max(y0,y1)+1):
            for k in range(w):
                path.add((x+k,y) if x0==x1 else (x,y+k))
line((7,H-1),(7,10))                  # vanuit de kloof omhoog langs de Mart
line((7,10),(36,10))                  # dorpsstraat onder de huizen
line((35,10),(35,24))                 # rechterkant omlaag
for (dx_,dy_) in DOORS.values():
    if dx_<10 and dy_>15: line((dx_,dy_+1),(7,dy_+1),1)
    elif dx_>35 and dy_>15: line((dx_,dy_+1),(35,dy_+1),1)
    else: line((dx_,dy_+1),(dx_,10),1)
line((S1[0],12),(S1[0],S1[1]-1))      # naar de trap
line((S1[0],S1[1]+2),(S1[0],17))      # weide
line((S1[0],17),(S0[0]+1,17))
line((S0[0],17),(S0[0],S0[1]-1))
line((S0[0],S0[1]+2),(S0[0],22))      # strand
path={c for c in path if FLOOR(c)}
autopath(m,path,'path_stone')

# --- bewoners/objecten (vrijhouden) ---
# visser, kind bij de sneeuwpop, oude vrouw bij het standbeeld, hiker bij de ingang, vrouw in de dorpsstraat
EVENTS={(19,22),(7,13),(24,15),(6,27),(33,12)}
print('events',sorted(EVENTS))

def free(c): return FLOOR(c) and c not in path and c not in EVENTS
def put_if(x,y,name,col=1):
    if free((x,y)): m.put(x,y,name,col); return True
    return False
for (x,y) in [(10,9),(18,9),(25,9),(32,9),(4,19),(39,14),(39,22),(8,27)]:
    if free((x,y)) and free((x,y-1)): m.put(x,y-1,'lamp_0',1); m.put(x,y,'lamp_1',1)
for (dx_,dy_) in DOORS.values():
    put_if(dx_-1,dy_+1,'pot_red'); put_if(dx_+1,dy_+1,'pot_white')
obj('stall',15,6,3,3)                                 # marktkraampje naast het Center
obj('statue',20,15,3,2)                               # standbeeld op de weide
obj('igloo',37,24,3,3,(1,2))                          # iglo (deur als decor)
if m.g[26][38]==N['igloo_12']: m.col[26][38]=1
for (x,y) in [(16,21),(17,21),(22,21),(23,21)]:       # boomstammen als bankjes aan het meer
    put_if(x,y,'log')
obj('bigtree',10,21,3,6)
for (x,y,n) in [(6,12,'snowman'),(5,15,'bunny')]:      # 1x2: hoofd erboven
    if free((x,y)) and free((x,y+1)): m.put(x,y,n+'_0',1); m.put(x,y+1,n+'_1',1)
for (x,y,n) in [(38,13,'snowball_big'),(32,6,'barrel'),(33,6,'crate'),(39,16,'rock_round'),(18,8,'sign_wood')]:
    put_if(x,y,n)

# --- bos op de kloofrand, dennen en keien ---
def okb(x,y):
    return inmap((x,y)) and (x,y) not in path and (x,y) not in EVENTS and m.g[y][x]==N['cliff_c'] and m.col[y][x]==0 and (x,y) in RIM
EDGE={c for c in RIM if inmap(c) and not any((c[0]+dx,c[1]+dy) in crater for dx in (-1,0,1) for dy in (-1,0,1,2))}
hforest(m,EDGE,okb,path)
for x in range(0,W,2):                 # bovenrand: onderkant van de bomen die boven de kaart staan (border)
    if m.g[0][x]==N['cliff_c'] and m.g[0][x+1]==N['cliff_c']:
        m.put(x,0,'htree_1e4',1); m.put(x+1,0,'htree_1e5',1)
def okd(x,y): return free((x,y))
def pine(x,y,g):
    cells=[(x+dx,y+dy) for dx in range(2) for dy in range(3)]
    if all(okd(*c) for c in cells) and len({level(c) for c in cells})==1: m.pine(x,y,green=g); return True
    return False
for (x,y,g) in [(2,31,True),(3,12,True),(4,15,False),(39,26,True),(31,24,True),(11,15,False),(32,15,True),(16,25,True),(14,27,False)]: pine(x,y,g)
for (x,y) in [(4,26),(39,19),(26,26)]:
    if all(okd(x+dx,y+dy) for dx in (0,1) for dy in (0,1)):
        for dx in (0,1):
            for dy in (0,1): m.put(x+dx,y+dy,f'boulder_{dx}{dy}',1)
# de weide en het strand zijn groen en bloeien (het beschutte 'paradijs'), het dorp is besneeuwd
for c in sorted(pit1):
    if not inmap(c): continue
    x,y=c
    if m.g[y][x] in (N['cliff_c'],N['snow']) and m.col[y][x]==0 and c not in EVENTS and c not in path:
        r=rnd.random()
        if r<0.22: m.put(x,y,rnd.choice(['flowers_blue','flowers_pink']),0)
        elif r<0.48: m.put(x,y,'grass_green',0)
        elif r<0.58: m.put(x,y,rnd.choice(['tuft0','tuft1','tuft3']),0)
for c in sorted(crater-pit1):
    if inmap(c) and okd(*c) and rnd.random()<0.06: m.put(*c,rnd.choice(['tuft2','tuft5','snow_dots','flowers_blue']),0)

# --- bereikbaarheid ---
from collections import deque
def walk(x,y): return inmap((x,y)) and m.col[y][x]==0
start=(5,H-1); seen={start}; q=deque([start])
while q:
    x,y=q.popleft()
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        n=(x+dx,y+dy)
        if n not in seen and walk(*n) and n not in EVENTS: seen.add(n); q.append(n)
print('deuren bereikbaar:',{k:(d[0],d[1]+1) in seen for k,d in DOORS.items() if d})
print('events bereikbaar:',{p:any((p[0]+dx,p[1]+dy) in seen for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) for p in sorted(EVENTS)})
shore={c for c in seen if any((c[0]+dx,c[1]+dy) in lake for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))}
print('meeroever bereikbaar:',len(shore))
d=os.path.join(REPO,'data/layouts/AshfrostTown')
if os.path.isdir(d):
    open(os.path.join(d,'map.bin'),'wb').write(struct.pack(f'<{W*H}H',*m.bin()))
    open(os.path.join(d,'border.bin'),'wb').write(struct.pack('<4H',*[N['htree_'+k]|(1<<10) for k in ('1d4','1d5','1dc','1dd')]))
if len(sys.argv)>1: m.img().save(sys.argv[1])
