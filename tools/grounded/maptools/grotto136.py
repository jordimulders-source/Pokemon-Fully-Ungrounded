"""Bouwt data/layouts/Route136_Grotto/map.bin: klein grotje met water (Marine Cave), lava (Terra Cave)
en blauwe/rode kristallen (Cave of Origin, op de bruine vloer; metatiles 0x3A5-0x3A7 in de Cave-tileset).
Gebruik: python3 tools/grounded/maptools/grotto136.py"""
import json, struct, os
REPO=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..'))
os.chdir(REPO)
L={l['name']:l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'name' in l}
def load(n):
    l=L[n+'_Layout']; W=l['width']; v=list(struct.unpack('<%dH'%(W*l['height']),open(l['blockdata_filepath'],'rb').read()))
    return W,l['height'],v
W,H,marine=load('MarineCave_End'); _,_,terra=load('TerraCave_End')
Y0=2; GH=H-Y0
g=[marine[(y+Y0)*W:(y+Y0+1)*W] for y in range(GH)]
# lavapoel van Terra Cave (kolommen 13-22, rijen 16-26) rechts naast het meer
for y in range(16,27):
    for x in range(13,23):
        t=terra[y*W+x]
        if (t&0x3ff) in range(0x35f,0x374) or (t&0x3ff) in (0x360,0x361,0x362):
            g[y-Y0][x+2]=t
# kristallen (blauw 0x3A5, rood 0x3A6/0x3A7) op vloer langs de wanden
BLUE,RED1,RED2=0x3a5,0x3a6,0x3a7
spots=[(3,11,BLUE),(4,14,BLUE),(2,17,BLUE),(15,11,RED1),(21,12,RED2),(24,16,RED1),(12,21,BLUE),(20,20,RED2),(7,19,BLUE),(18,14,RED1)]
floor={0x211}
placed=[]
for (x,y,c) in spots:
    if (g[y][x]&0x3ff) in floor:
        g[y][x]=c|0x400|(3<<12); placed.append((x,y))
import random
rnd=random.Random(1360)
cand=[(x,y) for y in range(8,GH-2) for x in range(2,W-2) if (g[y][x]&0x3ff) in floor and
      sum((g[y+dy][x+dx]&0x3ff) not in floor for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))>=2 and (x,y)!=(20,3)]
rnd.shuffle(cand)
for (x,y) in cand:
    if len(placed)>=16: break
    if any(abs(x-a)+abs(y-b)<3 for a,b in placed): continue
    g[y][x]=(BLUE if x<14 else rnd.choice((RED1,RED2)))|0x400|(3<<12); placed.append((x,y))
print('kristallen geplaatst:',placed)
# pad tussen meer en lava: K kolommen invoegen bij x=15 (alles vanaf de lava schuift K naar rechts)
K=3; FLOOR=0x211|(3<<12)
for y in range(GH):
    if y<7: ins=g[y][15]
    elif y==7: ins=g[y][13]
    elif y<GH-2: ins=FLOOR
    else: ins=g[y][14]
    g[y][15:15]=[ins]*K
W+=K
# oostoever van het meer (kolom 14) surfbaar maken: botsing eraf
for y in range(17,23):
    if (g[y][14]&0x3ff)==0x288: g[y][14]&=~0xc00
# het diepe water zelf had in Marine Cave botsing: eraf, zodat je kunt zwemmen (en duiken)
for y in range(GH):
    for x in range(W):
        if (g[y][x]&0x3ff) in (0x14e,0x14f): g[y][x]&=~0xc00
open('data/layouts/Route136_Grotto/map.bin','wb').write(struct.pack('<%dH'%(W*GH),*[t for r in g for t in r]))
# ladder (ingang) zoeken
lad=[(x,y) for y in range(GH) for x in range(W) if (g[y][x]>>0)&0x3ff in (0x2f5,0x2f6,0x2f7,0x29b,0x28f)]
print('grootte',W,GH)
