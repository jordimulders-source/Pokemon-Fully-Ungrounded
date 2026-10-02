"""Bouwt data/layouts/Route136_Grotto/map.bin (Crystal Cavity): Marine Cave End (volledig, met bovenrand)
met rechts een verbrede vloer waarin het lavameer van Terra Cave End (met eigen randen) ligt, plus
blauwe/rode kristallen (metatiles 0x3A5-0x3A7 in de Cave-tileset).
Coordinaten: ingang (28,4) (warp van Route 136), duikplek meer -> Underwater_Route136, bovenkomen op (9,21).
Gebruik: python3 tools/grounded/maptools/grotto136.py"""
import json, struct, os, random
REPO=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..'))
os.chdir(REPO)
L={l['name']:l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'name' in l}
def load(n):
    l=L[n+'_Layout']; W=l['width']; v=list(struct.unpack('<%dH'%(W*l['height']),open(l['blockdata_filepath'],'rb').read()))
    return W,l['height'],[v[y*W:(y+1)*W] for y in range(l['height'])]
W,H,g=load('MarineCave_End'); TW,_,terra=load('TerraCave_End')
# N kolommen invoegen: bovenin (rij 0-9) vóór de ingang (kopie van kolom 18), daaronder bij kolom 20 (vloer)
N=8
for y in range(H):
    if y<10: g[y][19:19]=[g[y][18]]*N
    else:    g[y][20:20]=[g[y][20]]*N
W+=N
# lavameer van Terra Cave (kolommen 13-22, rijen 17-26, incl. lavaranden) op de verbrede vloer (kolom 19-28)
LAVA=range(0x35f,0x374)
for y in range(17,27):
    for x in range(13,23):
        t=terra[y][x]
        if (t&0x3ff) in LAVA: g[y][x+6]=t
# oostoever van het meer (kolom 14) surfbaar maken: botsing eraf
for y in range(19,25):
    if (g[y][14]&0x3ff)==0x288: g[y][14]&=~0xc00
# het diepe water had in Marine Cave botsing: eraf, zodat je kunt zwemmen (en duiken)
for y in range(H):
    for x in range(W):
        if (g[y][x]&0x3ff) in (0x14e,0x14f): g[y][x]&=~0xc00
# kristallen op vloer langs wanden: blauw bij het meer, rood bij de lava
BLUE,RED1,RED2=0x3a5,0x3a6,0x3a7
floor={0x211}
rnd=random.Random(1360)
cand=[(x,y) for y in range(10,H-2) for x in range(2,W-2) if (g[y][x]&0x3ff) in floor and
      sum((g[y+dy][x+dx]&0x3ff) not in floor for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))>=2]
rnd.shuffle(cand)
placed=[]
for (x,y) in cand:
    if len(placed)>=18: break
    if any(abs(x-a)+abs(y-b)<3 for a,b in placed): continue
    g[y][x]=(BLUE if x<17 else rnd.choice((RED1,RED2)))|0x400|(3<<12); placed.append((x,y))
print('kristallen:',sorted(placed))
open('data/layouts/Route136_Grotto/map.bin','wb').write(struct.pack('<%dH'%(W*H),*[t for r in g for t in r]))
print('grootte',W,H)
