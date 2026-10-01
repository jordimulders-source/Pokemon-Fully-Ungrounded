"""Bouwt data/layouts/AshfrostTown/map.bin: Ashfrost Village ligt in een diep dal boven op de berg.
Een hoge rotswand rondom (bos erop). Vier lagen: bovenaan het dorp (Pokémon Center centraal), één laag lager
nog een huis en het heiligdom met de stenen Regi-beelden, dan een groene weide, en helemaal onderin het meer.
Een slingerpad met stenen trappen (midden in rechte klifwanden) loopt van boven naar beneden.
Tilesets: snow_town_base (primary) + snow_town (secondary), zie snow_tileset.py --town.
Ingang: een smalle kloof linksonder (x 5-8), warp naar Route 136 (coord-triggers op de onderste rij).
Gebruik: python3 tools/grounded/maptools/ashfrost.py [voorbeeld.png]   (SOFT=1: objecten die niet passen melden)"""
import os, sys, struct, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from snowlib import *
use_tileset('snow_town')
W,H=48,40
m=M(W,H,base='cliff_c'); rnd=random.Random(2024)
ALL={(x,y) for x in range(-4,W+4) for y in range(-4,H+6)}
inmap=lambda c: 0<=c[0]<W and 0<=c[1]<H

# --- vormen: kloof (dorp), laag 1 (huis + heiligdom), laag 2 (weide), laag 3 (meer) ---
def rrect(x0,y0,x1,y1,cut=2):
    # alleen de bovenhoeken afschuinen: onderhoeken van een kuil worden anders losse klifstukjes
    return {(x,y) for (x,y) in rect(x0,y0,x1,y1) if min(x-x0,x1-x)+(y-y0)>=cut}
GORGE=set(rect(5,36,8,H+5))
crater=rrect(3,5,44,35,0)|GORGE
pit1=rrect(10,15,37,35,0)
pit2=rrect(14,23,33,35,0)
pit3=rrect(17,28,30,35,0)
lake=smooth(set(blob(23.8,32.3,5.7,2.7,seed=3,rough=0.10)))
RIM=ALL-crater
for P in (pit3,pit2,pit1):
    terrace(m,ALL-P,face=2)
terrace(m,RIM,face=4)               # hoge kloofwand
for c in pit3:
    if inmap(c): m.put(*c,'snow',0)
m.water({c for c in lake if inmap(c)})

def top(S,x): return min(y for (xx,y) in S if xx==x)
# trappen midden in rechte klifwanden; het pad slingert: links omlaag, rechts omlaag, links omlaag
S1=(18,top(pit1,18)-2); S2=(26,top(pit2,26)-2); S3=(22,top(pit3,22)-2)
for (P,(sx,sy)) in ((pit1,S1),(pit2,S2),(pit3,S3)):
    assert all(top(P,x)==top(P,sx) for x in range(sx-1,sx+3)),(sx,sy)
    for y in (sy,sy+1): m.put(sx,y,'hstairs_l',0); m.put(sx+1,y,'hstairs_r',0)
print('trappen',S1,S2,S3)

# --- gebouwen en grote objecten ---
def level(c):
    return 3 if c in pit3 else 2 if c in pit2 else 1 if c in pit1 else 0
FLOOR=lambda c: inmap(c) and m.g[c[1]][c[0]] in (N['cliff_c'],N['snow']) and m.col[c[1]][c[0]]==0
def obj(name,x0,y0,w,h,door=None):
    cells=[(x0+dx,y0+dy) for dx in range(w) for dy in range(h)]
    lv={level(c) for c in cells}
    bad=[c for c in cells if not FLOOR(c)]+([] if door is None else [c for c in [(x0+door[0],y0+door[1]+1)] if not FLOOR(c)])
    if os.environ.get('SOFT') and (bad or len(lv)>1): print('PAST NIET',name,bad,lv); return None
    assert not bad and len(lv)==1,(name,bad,lv)
    for dy in range(h):
        for dx in range(w):
            m.put(x0+dx,y0+dy,f'{name}_{dx}{dy}',0 if (dx,dy)==door else 1)
    return None if door is None else (x0+door[0],y0+door[1])
class _D(dict):
    def values(s): return [v for v in dict.values(s) if v]
DOORS=_D()
# laag 0 (dorp)
DOORS['lodge']=obj('lodge',4,5,5,5,(1,4))
DOORS['house_blue']=obj('house_blue',11,6,4,4,(1,3))
DOORS['pc']=obj('pc',21,5,5,5,(2,4))                  # centraal boven het dal
DOORS['house_pink']=obj('house_pink',29,6,4,4,(2,3))
DOORS['house_yellow']=obj('house_yellow',36,6,4,4,(1,3))
DOORS['mart']=obj('mart',3,24,4,4,(2,3))              # bij de ingang
# laag 1
DOORS['house_green']=obj('house_green',12,15,4,4,(2,3))
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
line((7,10),(41,10))                  # dorpsstraat onder de huizen
for (dx_,dy_) in DOORS.values():
    if level((dx_,dy_))==1: line((dx_,dy_+1),(dx_,19),1)
    elif dx_<10 and dy_>15: line((dx_,dy_+1),(7,dy_+1),1)
    else: line((dx_,dy_+1),(dx_,10),1)
line((S1[0],12),(S1[0],S1[1]-1)); line((S1[0],S1[1]+2),(S1[0],19))
line((11,19),(S2[0]+1,19))            # straat op laag 1
line((S2[0],S2[1]+2),(S2[0],23)); line((S3[0],23),(S2[0]+1,23))   # weide
line((S3[0],24),(S3[0],S3[1]-1))     # aansluiten op de onderste trap
line((S3[0],S3[1]+2),(S3[0],29))      # strand
path={c for c in path if FLOOR(c)}
autopath(m,path,'path_stone')

# --- bewoners (vrijhouden) ---
# visser, kind bij de sneeuwpop, oude vrouw bij het heiligdom, hiker bij de ingang, vrouw in de dorpsstraat
EVENTS={(23,29),(5,14),(24,18),(6,33),(34,11)}
print('events',sorted(EVENTS))

def free(c): return FLOOR(c) and c not in path and c not in EVENTS
def put_if(x,y,name,col=1):
    if free((x,y)): m.put(x,y,name,col); return True
    return False
# heiligdom: drie stenen Regi-beelden op laag 1, lantaarns en bloemen ervoor
for i,sp in enumerate(('regirock','regice','registeel')):
    obj(sp,20+3*i,15,2,3)
for (x,y) in [(10,9),(19,9),(27,9),(34,9),(42,9),(4,22),(42,18),(19,17),(29,17)]:
    if free((x,y)) and free((x,y-1)): m.put(x,y-1,'lamp_0',1); m.put(x,y,'lamp_1',1)
for x in (20,21,23,24,26,27): put_if(x,18,'g_flowers')
for (dx_,dy_) in DOORS.values():
    put_if(dx_-1,dy_+1,'pot_red'); put_if(dx_+1,dy_+1,'pot_white')
obj('stall',15,6,3,3)                                 # marktkraampje naast het Center
obj('igloo',33,15,3,3,(1,2))                          # iglo (later de weg naar de Regigigas-grot)
if m.g[17][34]==N['igloo_12']: m.col[17][34]=1
# stenen hekje langs de klifrand boven laag 1 (niet voor de trap)
for x in range(10,38):
    if free((x,12)) and m.g[13][x] not in (N['hstairs_l'],N['hstairs_r']):
        l=not free((x-1,12)); r=not free((x+1,12))
        m.put(x,12,'g_fence_l' if l else 'g_fence_r' if r else 'g_fence_m',1)
# heggen, brievenbussen, wegwijzer en ander decor
for (x,y) in [(42,5),(42,13)]:
    if all(free((x+dx,y+dy)) for dx in range(3) for dy in range(2)):
        for dx in range(3):
            for dy in range(2): m.put(x+dx,y+dy,f'hedge_{dx}{dy}',1)
for (x,y,n) in [(10,8,'g_mailbox'),(28,8,'g_mailbox'),(35,8,'g_mailbox'),(9,30,'g_sign'),(15,18,'g_mailbox'),
                (38,12,'snowball_big'),(43,24,'rock_round'),(18,8,'sign_wood'),(30,21,'ice_plant'),
                (12,24,'stump2'),(35,27,'log'),(36,27,'log')]:
    put_if(x,y,n)
for (x,y,n) in [(4,13,'snowman'),(4,17,'bunny')]:      # 1x2: hoofd erboven
    if free((x,y)) and free((x,y+1)): m.put(x,y,n+'_0',1); m.put(x,y+1,n+'_1',1)
for (x,y) in [(22,29),(25,28),(26,28)]: put_if(x,y,'log')    # boomstammen als bankjes aan het meer
obj('bigtree',10,27,3,6)

# besneeuwd hoog gras in plukken (decor; Ashfrost heeft geen wilde Pokémon)
for (x0,y0,w,h) in [(34,20,3,2),(41,22,3,3),(4,29,2,2),(35,32,3,2)]:
    for x in range(x0,x0+w):
        for y in range(y0,y0+h):
            if free((x,y)) and rnd.random()<0.85: m.put(x,y,'grass_snow',0)
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
for (x,y,g) in [(2,37,True),(3,19,False),(42,26,True),(43,31,False),(14,26,True),(14,31,False),(34,24,True),
                (29,30,True),(10,21,False),(36,30,False)]: pine(x,y,g)
for (x,y) in [(4,31),(42,20),(33,32)]:
    if all(okd(x+dx,y+dy) for dx in (0,1) for dy in (0,1)):
        for dx in (0,1):
            for dy in (0,1): m.put(x+dx,y+dy,f'boulder_{dx}{dy}',1)
# de weide (laag 2) is groen en bloeit (het beschutte 'paradijs'), de rest is besneeuwd
for c in sorted(pit2-pit3):
    if not inmap(c): continue
    x,y=c
    if m.g[y][x] in (N['cliff_c'],N['snow']) and m.col[y][x]==0 and c not in EVENTS and c not in path:
        r=rnd.random()
        if r<0.22: m.put(x,y,rnd.choice(['flowers_blue','flowers_pink']),0)
        elif r<0.45: m.put(x,y,'grass_green',0)
        elif r<0.55: m.put(x,y,rnd.choice(['tuft0','tuft1','tuft3']),0)
for c in sorted(crater-pit2):
    if inmap(c) and okd(*c) and rnd.random()<0.06: m.put(*c,rnd.choice(['tuft2','tuft5','snow_dots','flowers_blue']),0)

# --- bereikbaarheid ---
from collections import deque
def walk(x,y): return inmap((x,y)) and m.col[y][x]==0
start=(7,H-1); seen={start}; q=deque([start])
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
