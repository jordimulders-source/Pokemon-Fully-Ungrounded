"""Ronde 8: voorbeeldsprite op Jordi's eigen omtrek (jordi_overtrek/omtrek_cellen.json, 1 vak = 1 pixel, kop staat vast:
"de kop gaat niet meer afwijken van deze omtrek"). Alleen weggevallen pixels bovenin en onderaan de rug ingevuld.
Lijf = ronde 3, rij voor rij (zelfde rijen 42-62) doorgetrokken vanaf Jordi's kaakpunt en ruglijn naar de staart van ronde 3.
Vlakke kleuren; halsrand, snavelhoorn en schorsstreepjes komen bij het afwerken."""
import json
from collections import deque
D=json.load(open('../../jordi_overtrek/omtrek_cellen.json'))
DY=-10
L={tuple(p) for p in D['lijn']}
# weggevallen pixels (gaten tussen lijnstukken; rug onderaan tot de rand van zijn tekening)
L|={(39,13),(40,14),(41,14),(47,17),(47,18),(56,29),(59,42),(28,31),(13,27),(59,46),(59,47),(59,48),(59,49),(59,50),(58,51)}
HALS={tuple(p) for p in D['lijn'] if p[0]>=27 and p[1]>=28 and not (p[1]<=41 and p[0]<=34) and p[0]<=43 or (p[1]==50 and 18<=p[0]<=23)}
L={(x,y+DY) for x,y in L}; HALS={(x,y+DY) for x,y in HALS}; OOG={(x,y+DY) for x,y in D['oog']}
R3=[l.rstrip('\n').ljust(64,'.') for l in open('../ronde3/raster.txt')][:64]
G=[['.']*64 for _ in range(64)]
# lijf: rijen 42..62 van ronde 3, randen van Jordi's onderkant (x 25..59 op rij 41) naar ronde 3 bij rij 55
def ext(r): xs=[i for i,c in enumerate(r) if c!='.']; return (min(xs),max(xs)) if xs else None
l42,r42=ext(R3[42])
for y in range(42,63):
    e=ext(R3[y])
    if not e: continue
    t=min(1,(y-42)/13); l=round(e[0]+(25-l42)*(1-t)); r=round(e[1]+(59-r42)*(1-t))
    src=R3[y][e[0]:e[1]+1]
    for x in range(l,r+1):
        c=src[min(len(src)-1,int((x-l)/(r-l+1)*len(src)))] if r>l else src[0]
        G[y][x]=c
    if t<1:
        G[y][l]='1'; G[y][r]='1'
# kop: binnenkant = niet bereikbaar van buiten (lijncellen en lijf als muur)
wall=lambda x,y:(x,y) in L or G[y][x]!='.'
out=set(); q=deque([(0,0)])
while q:
    x,y=q.popleft()
    if (x,y) in out or not(0<=x<64 and 0<=y<64) or wall(x,y): continue
    out.add((x,y)); q.extend([(x+1,y),(x-1,y),(x,y+1),(x,y-1)])
# muil: flood vanaf een punt in de muil
mond=set(); q=deque([(20,26)])
while q:
    x,y=q.popleft()
    if (x,y) in mond or (x,y) in L: continue
    mond.add((x,y)); q.extend([(x+1,y),(x-1,y),(x,y+1),(x,y-1)])
assert len(mond)<800, 'muil lekt'
def halsx(y):
    xs=[x for x,yy in HALS if yy==y]; return max(xs) if xs else None
for y in range(64):
    for x in range(64):
        if (x,y) in out or G[y][x]!='.' or (x,y) in L: continue
        if (x,y) in mond: G[y][x]='9' if y<=18 else 'A' if y<=28 else 'B' if y<=35 else 'C'
        else:
            hx=halsx(y)
            G[y][x]='4' if ((y>=18 and hx is not None and x>hx) or y>=40) else ('6' if y<6 else '5')
for x,y in L:
    G[y][x]='2' if (x,y) in HALS else ('2' if (x<32 and y<12) else '1')
for x,y in OOG: G[y][x]='8'
for x in range(24,33):
    if (x,40) in L: G[40][x]='2'
open('raster.txt','w').write('\n'.join(''.join(r) for r in G)+'\n')
