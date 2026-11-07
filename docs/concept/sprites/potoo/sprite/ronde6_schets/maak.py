"""Ronde 6: vormschets naar Jordi's schets 2 (7 nov): volle hoge koepel die achter in één boog in de mantel loopt, bevederde wang/kaak rechts van de muil die in de borst doorloopt, bovenrand muil bol omhoog naar de snavelpunt. Verder als ronde 5, vlakke kleuren, alleen de vorm.
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
        if x>=27 and y<=31 and ell(27,26,19.5,22.5,x,y) and G[y][x]=='.': paint(x,y,'4' if x>38 else '5')
# kop: bol, voorover/omlaag voor de borst
for y in range(0,32):
    for x in range(10,40):
        if ell(27,17,15.5,13.5,x,y) and not (y>=17 and x>=36 and G[y][x] in '23F4'): paint(x,y,'6' if ell(22,10,7,5,x,y) else '5')
# keel tussen bek en borst
for y in range(26,42):
    for x in range(21,37):
        if G[y][x]=='.': paint(x,y,'5')
# bek: brede ronde U met één punt onderaan (polygoon met de hand: snavelpunt, bol omlaag, punt, terug tot onder het oog)
from PIL import Image, ImageDraw
PT=[(13,19.5),(17,18.6),(21,18.6),(25,19.3),(28.5,20.5),(30,23),(30,27),(28.5,31),(26,34.5),(23.5,38.5),(21,35.5),(17,33),(13.5,29),(11.8,25),(12,21.5)]
m=Image.new('L',(64*8,64*8),0); ImageDraw.Draw(m).polygon([(x*8+4,y*8+4) for x,y in PT],fill=255)
m=m.resize((64,64),Image.BOX)
M={(x,y) for y in range(64) for x in range(64) if m.getpixel((x,y))>=128}
for x,y in M:
    paint(x,y,'9' if y<=22 else 'A' if y<=31 else 'B' if y<=35 else 'C')
for x,y in M:
    if any((x+dx,y+dy) not in M for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): G[y][x]='D'
# snijrand + bovensnavel met haak (linksboven)
for x,y in M:
    if (x,y-1) not in M and x>=14: G[y][x]='1'
for x,y in [(13,16),(14,16),(15,16),(16,16),(12,17),(11,18),(10,19),(10,20),(10,21),(11,22),(12,22)]: paint(x,y,'1')
for x,y in [(13,17),(14,17),(15,17),(16,17),(17,17),(12,18),(13,18),(14,18),(15,18),(11,19),(12,19),(11,20),(12,20),(11,21)]: paint(x,y,'7')
for x,y in [(13,19),(12,21),(13,20)]: paint(x,y,'E')
# punt onderkaak
for x,y in [(23,38),(24,38),(23,37),(24,37),(22,37)]:
    if (x,y) in M: G[y][x]='E'
# oog: naar voren, liggend ovaal, puur zwart
for y in range(8,20):
    for x in range(16,32):
        if ell(23.5,12.8,4.7,3.5,x,y): paint(x,y,'8')
# wang/kaaklijn: van onder het oog langs de rechterkant van de muil omlaag en naar links onder de bek (binnenlijn)
W=[(31,20),(33,24),(34,27),(33.5,30),(31.5,33),(28.5,35.5),(25.5,37.5),(22,39)]
for (x0,y0),(x1,y1) in zip(W,W[1:]):
    for i in range(21):
        x=round(x0+(x1-x0)*i/20); y=round(y0+(y1-y0)*i/20)
        if (x,y) not in M and G[y][x] not in '.': paint(x,y,'2')
# buitenlijn om alles wat nieuw is
def at(x,y): return G[y][x] if 0<=x<64 and 0<=y<64 else '.'
O=[r[:] for r in G]
for x,y in F:
    if G[y][x]=='.': continue
    nb=[at(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
    if '.' in nb: O[y][x]='2' if (x<32 and y<20) else '1'
    elif (x,y) not in M and any((x+dx,y+dy) in M for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) and y>21: O[y][x]='1'
G=O
open(sys.argv[1] if len(sys.argv)>1 else 'raster.txt','w').write('\n'.join(''.join(r) for r in G)+'\n')
