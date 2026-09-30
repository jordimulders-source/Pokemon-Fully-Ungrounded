"""Bouwt data/layouts/AshfrostTown/map.bin: een beschut dal boven op de berg, met een meertje in het midden,
huizen eromheen (twee op een verhoging), Pokémon Center en Mart. Tileset: snow_town (zie snow_tileset.py --town).
Ingang onderaan (x 18-21, verbonden met de bergpas van Route 136, offset 30).
Gebruik: python3 tools/grounded/maptools/ashfrost.py [voorbeeld.png]"""
import os, sys, struct, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from snowlib import *
use_tileset('snow_town')
W,H=40,30
m=M(W,H); rnd=random.Random(2024)
STL,STR=175,207   # stenen Hoenn-trap (General), zoals op Route 136
# events: (vrij houden) visser, sneeuwpop-omgeving, NPC's, deuren
EVENTS={(12,12),(26,15),(15,24),(33,12),(8,23),(30,23)}
# --- verhoging rechtsboven met twee huizen ---
PLAT=set(rect(24,-1,36,9))
terrace(m,PLAT)
for y in (8,9): m.put(29,y,STL,0); m.put(30,y,STR,0)
# --- meertje in het midden ---
lake=smooth(set(blob(19,14,6.5,3.6,seed=3,rough=0.12)))
m.water(lake)
# visser op de noordoever (kijkt naar beneden het water in)
FISH=(19,min(y for (x,y) in lake if x==19)-1); EVENTS.add(FISH); print('visser',FISH)
# --- gebouwen ---
def building(name,x0,y0,w,h,door):
    for dy in range(h):
        for dx in range(w):
            m.put(x0+dx,y0+dy,f'{name}_{dx}{dy}',0 if (dx,dy)==door else 1)
    return (x0+door[0],y0+door[1])
DOORS={}
DOORS['pc']=building('pc',6,17,5,5,(2,4))          # deur (8,21)
DOORS['mart']=building('mart',28,18,4,4,(2,3))     # deur (30,21)
DOORS['house_blue']=building('house_blue',5,4,4,4,(1,3))    # deur (6,7), oud huis linksboven
DOORS['house_yellow']=building('house_yellow',25,2,4,4,(1,3))  # op de verhoging, deur (26,5)
DOORS['house_pink']=building('house_pink',31,3,4,3,(2,2))      # op de verhoging, deur (33,5)
print('deuren',DOORS)
# --- paden ---
path=(set(rect(19,22,20,H-1))|set(rect(8,22,31,23))|set(rect(6,8,7,23))|set(rect(29,10,30,21))
      |set(rect(26,6,26,7))|set(rect(26,7,33,7))|set(rect(33,6,33,7))|set(rect(26,6,33,7))-set(rect(29,6,30,6)))
path={c for c in path if m.col[c[1]][c[0]]==0 and m.g[c[1]][c[0]] in (N['snow'],N['cliff_c'])}
autopath(m,path,'path_stone')
# --- sneeuwpop bij het meer ---
m.put(12,11,'snowman',1)
# --- bosrand rondom (besneeuwde Hoenn-bomen), met opening onderaan voor de ingang ---
def okb(x,y):
    return 0<=x<W and 0<=y<H and (x,y) not in path and (x,y) not in EVENTS and m.g[y][x]==N['snow']
BAND=set(rect(0,0,3,H-1))|set(rect(W-4,0,W-1,H-1))|set(rect(0,0,W-1,1))|set(rect(0,H-2,17,H-1))|set(rect(22,H-2,W-1,H-1))
hforest(m,BAND,okb,path)
# groene dennen: het dal is een beschut, groener plekje
def pine(x,y,g):
    cells=[(x+dx,y+dy) for dx in range(2) for dy in range(3)]
    if all(okb(*c) for c in cells): m.pine(x,y,green=g)
for (x,y,g) in [(10,3,True),(14,4,True),(4,11,True),(12,25,True),(24,24,True),(34,14,True),(35,19,False),(16,17,True),(25,11,False),(9,13,True),(13,2,True),(16,3,False),(19,2,True),(21,4,True),(35,23,True),(3,24,True)]: pine(x,y,g)
# bloemen en groen gras rond het meer (paradijselijk), wat plukjes elders
ring={(x+dx,y+dy) for (x,y) in lake for dx in (-2,-1,0,1,2) for dy in (-2,-1,0,1,2)}-lake
for (x,y) in sorted(ring):
    if okb(x,y) and not any((x+dx,y+dy) in lake for dx in (-1,0,1) for dy in (-1,0,1)):
        r=rnd.random()
        if r<0.35: m.put(x,y,rnd.choice(['flowers_blue','flowers_pink']),0)
        elif r<0.45: m.put(x,y,rnd.choice(['tuft0','tuft1','tuft3']),0)
for (x,y) in [(x,y) for y in range(H) for x in range(W)]:
    if okb(x,y) and rnd.random()<0.05: m.put(x,y,rnd.choice(['snow_dots','tuft2','tuft5','snow_light']),0)
# --- bereikbaarheid ---
from collections import deque
def walk(x,y): return 0<=x<W and 0<=y<H and m.col[y][x]==0 and m.elev[y][x]==3
start=(19,H-1); seen={start}; q=deque([start])
while q:
    x,y=q.popleft()
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        n=(x+dx,y+dy)
        if n not in seen and walk(*n) and n not in EVENTS: seen.add(n); q.append(n)
print('deuren bereikbaar:',{k:(d[0],d[1]+1) in seen for k,d in DOORS.items()})
print('events bereikbaar:',{p:any((p[0]+dx,p[1]+dy) in seen for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) for p in sorted(EVENTS)})
d=os.path.join(REPO,'data/layouts/AshfrostTown')
if os.path.isdir(d):
    open(os.path.join(d,'map.bin'),'wb').write(struct.pack(f'<{W*H}H',*m.bin()))
if len(sys.argv)>1: m.img().save(sys.argv[1])
