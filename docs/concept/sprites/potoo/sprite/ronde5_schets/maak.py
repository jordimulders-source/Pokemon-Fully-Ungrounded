"""Ronde 5: vormschets naar Jordi's tekening (7 nov), vlakke kleuren, alleen de vorm.
Lijf = ronde 3 (goedgekeurd). Kop hangt voorover voor de borst; kruin-achterkop-nek-rug één doorgaande boog; bek als brede
ronde U met één punt onderaan (snavelpunt linksboven, bol omlaag, rechts terug tot onder het oog); oog naar voren, liggend ovaal."""
import sys, math
G=[list(l.rstrip('\n')) for l in open('../ronde3/raster.txt')][:64]
def ell(cx,cy,rx,ry,x,y): return ((x-cx)/rx)**2+((y-cy)/ry)**2<=1
# kop/hals van ronde 3 weg
for y in range(0,38):
    for x in range(0,64):
        if y<28 and x<=37: G[y][x]='.'
        elif y<17 and x<=47: G[y][x]='.'
        elif y<32 and x<=27: G[y][x]='.'
        elif y<38 and x<=23: G[y][x]='.'
F=set()   # nieuw geschilderde pixels
def paint(x,y,c): G[y][x]=c; F.add((x,y))
# nek/rug-boog: kruin (28,3) -> achterkop -> nek -> rug (46,21), één bolle curve
for y in range(0,32):
    for x in range(16,48):
        if x>=25 and y<=27 and ell(26,27,20.5,24.5,x,y) and G[y][x]=='.': paint(x,y,'4' if x>38 else '5')
# kop: bol, voorover/omlaag voor de borst
for y in range(0,32):
    for x in range(10,40):
        if ell(25,15,11.5,11,x,y): paint(x,y,'6' if ell(22,11,6,5,x,y) else '5')
# keel tussen bek en borst
for y in range(24,38):
    for x in range(22,37):
        if G[y][x]=='.': paint(x,y,'5')
# bek: brede ronde U met één punt onderaan (polygoon met de hand: snavelpunt, bol omlaag, punt, terug tot onder het oog)
from PIL import Image, ImageDraw
PT=[(16,16),(13.5,19),(12.5,23),(13.5,27),(16.5,31),(21,34),(24.5,36),(27,33),(30,29),(32.5,24),(34,19.5),(34,17)]
m=Image.new('L',(64*8,64*8),0); ImageDraw.Draw(m).polygon([(x*8+4,y*8+4) for x,y in PT],fill=255)
m=m.resize((64,64),Image.BOX)
M={(x,y) for y in range(64) for x in range(64) if m.getpixel((x,y))>=128}
for x,y in M:
    paint(x,y,'9' if y<=18 else 'A' if y<=27 else 'B' if y<=31 else 'C')
for x,y in M:
    if any((x+dx,y+dy) not in M for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): G[y][x]='D'
# snijrand + bovensnavel met haak (linksboven)
for x in range(16,35):
    if (x,16) in M: G[16][x]='1'
for x,y in [(14,13),(15,13),(16,13),(17,13),(13,14),(12,15),(12,16),(12,17),(13,18),(14,18)]: paint(x,y,'1')
for x,y in [(14,14),(15,14),(16,14),(17,14),(18,14),(13,15),(14,15),(15,15),(16,15),(17,15),(13,16),(14,16),(15,16),(13,17)]: paint(x,y,'7')
for x,y in [(14,17),(15,17)]: paint(x,y,'E')
# punt onderkaak
for x,y in [(24,35),(25,35),(24,34),(25,34),(23,34)]:
    if (x,y) in M: G[y][x]='E'
# oog: naar voren, liggend ovaal, puur zwart
for y in range(4,16):
    for x in range(18,34):
        if ell(25,10.5,4.2,3.2,x,y): paint(x,y,'8')
# buitenlijn om alles wat nieuw is
def at(x,y): return G[y][x] if 0<=x<64 and 0<=y<64 else '.'
O=[r[:] for r in G]
for x,y in F:
    if G[y][x]=='.': continue
    nb=[at(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
    if '.' in nb: O[y][x]='2' if (x<30 and y<16) else '1'
    elif (x,y) not in M and any((x+dx,y+dy) in M for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) and y>17: O[y][x]='1'
G=O
open(sys.argv[1] if len(sys.argv)>1 else 'raster.txt','w').write('\n'.join(''.join(r) for r in G)+'\n')
