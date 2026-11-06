"""Ronde 5: vormschets naar Jordi's tekening (7 nov), vlakke kleuren, alleen de vorm.
Lijf = ronde 3 (goedgekeurd). Kop hangt voorover voor de borst; kruin-achterkop-nek-rug één doorgaande boog; bek als brede
ronde U met één punt onderaan (snavelpunt linksboven, bol omlaag, rechts terug tot onder het oog); oog naar voren, liggend ovaal."""
import sys, math
G=[list(l.rstrip('\n')) for l in open('../ronde3/raster.txt')][:64]
def ell(cx,cy,rx,ry,x,y): return ((x-cx)/rx)**2+((y-cy)/ry)**2<=1
# kop/hals van ronde 3 weg
for y in range(0,42):
    for x in range(0,64):
        if y<28 and x<=37: G[y][x]='.'
        elif y<17 and x<=47: G[y][x]='.'
        elif y<32 and x<=27: G[y][x]='.'
        elif y<42 and x<=23: G[y][x]='.'
F=set()   # nieuw geschilderde pixels
def paint(x,y,c): G[y][x]=c; F.add((x,y))
# nek/rug-boog: kruin (28,3) -> achterkop -> nek -> rug (46,21), één bolle curve
for y in range(0,32):
    for x in range(16,48):
        if x>=23 and y<=31 and ell(23,33,23,25,x,y) and G[y][x]=='.': paint(x,y,'4' if x>38 else '5')
# kop: bol, voorover/omlaag voor de borst
for y in range(0,32):
    for x in range(10,40):
        if ell(23,19,11.5,11,x,y): paint(x,y,'6' if ell(20,15,6,5,x,y) else '5')
# keel tussen bek en borst
for y in range(26,42):
    for x in range(21,37):
        if G[y][x]=='.': paint(x,y,'5')
# bek: brede ronde U met één punt onderaan (polygoon met de hand: snavelpunt, bol omlaag, punt, terug tot onder het oog)
from PIL import Image, ImageDraw
PT=[(15,20),(12.5,23),(11.5,27),(12.5,31),(15.5,35),(19,37),(22,39),(23.5,41.5),(25,39),(26.5,36.5),(29,33),(31.5,28),(33,23.5),(33,21)]
m=Image.new('L',(64*8,64*8),0); ImageDraw.Draw(m).polygon([(x*8+4,y*8+4) for x,y in PT],fill=255)
m=m.resize((64,64),Image.BOX)
M={(x,y) for y in range(64) for x in range(64) if m.getpixel((x,y))>=128}
for x,y in M:
    paint(x,y,'9' if y<=22 else 'A' if y<=31 else 'B' if y<=35 else 'C')
for x,y in M:
    if any((x+dx,y+dy) not in M for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): G[y][x]='D'
# snijrand + bovensnavel met haak (linksboven)
for x in range(14,35):
    if (x,20) in M: G[20][x]='1'
for x,y in [(13,17),(14,17),(15,17),(16,17),(12,18),(11,19),(11,20),(11,21),(12,22),(13,22)]: paint(x,y,'1')
for x,y in [(13,18),(14,18),(15,18),(16,18),(17,18),(12,19),(13,19),(14,19),(15,19),(16,19),(12,20),(13,20),(14,20),(12,21)]: paint(x,y,'7')
for x,y in [(13,21),(14,21)]: paint(x,y,'E')
# punt onderkaak
for x,y in [(23,40),(24,40),(23,41),(23,39),(24,39)]:
    if (x,y) in M: G[y][x]='E'
# oog: naar voren, liggend ovaal, puur zwart
for y in range(8,20):
    for x in range(16,32):
        if ell(23,14.5,4.2,3.2,x,y): paint(x,y,'8')
# buitenlijn om alles wat nieuw is
def at(x,y): return G[y][x] if 0<=x<64 and 0<=y<64 else '.'
O=[r[:] for r in G]
for x,y in F:
    if G[y][x]=='.': continue
    nb=[at(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
    if '.' in nb: O[y][x]='2' if (x<30 and y<20) else '1'
    elif (x,y) not in M and any((x+dx,y+dy) in M for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) and y>21: O[y][x]='1'
G=O
open(sys.argv[1] if len(sys.argv)>1 else 'raster.txt','w').write('\n'.join(''.join(r) for r in G)+'\n')
