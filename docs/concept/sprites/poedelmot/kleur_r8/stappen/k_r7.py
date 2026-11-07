# vleugels en buik: tan vlakken op de plek en grootte van het model (gids = verkleind model), witte geschulpte rand
import numpy as np
from PIL import Image
g=np.array(Image.open('/home/user/pokemon-fully-ungrounded/docs/concept/sprites/poedelmot/silhouet/gids_gemiddeld.png')).astype(int)
Z=set(tuple(map(int,l.split(','))) for l in open('spriet_zone.txt'))
DIAG={y:36+round((y-29)*6/17) for y in range(30,48)}
L=lambda x,y: 0.299*g[y,x,0]+0.587*g[y,x,1]+0.114*g[y,x,2]
def toon(l):
    return 'A' if l>=238 else '9' if l>=224 else '7' if l>=205 else '6' if l>=180 else '5'
for y in range(19,47):
    for x in range(64):
        if r[y][x] in '.1234' or (x,y) in Z or x<=DIAG.get(y,37)+1: continue
        r[y][x]=toon(L(x,y))
# lichte lijn langs de kop (wit randje van de vleugelvoet)
for y,x in DIAG.items():
    if y<46 and r[y][x+1] not in '.1234': r[y][x+1]='A'
    if r[y][x]!='.': r[y][x]='4'
# brede witte geschulpte buitenrand: 2 px binnen de rechterrand van beide vleugels wit
for y in range(20,46):
    xs=[x for x in range(40,64) if r[y][x]!='.']
    if not xs: continue
    e=max(xs)
    for x in (e-1,e-2):
        if r[y][x] in '5679': r[y][x]='A'
# buik tussen de pluimen: kleiner en lichter, losse tan plaatjes volgens het model
for y in range(46,57):
    for x in range(28,43):
        if r[y][x] in '4567': r[y][x]=toon(L(x,y)+12)
