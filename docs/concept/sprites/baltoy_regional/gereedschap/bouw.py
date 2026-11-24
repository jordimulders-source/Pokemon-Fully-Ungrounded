# Bouwt sprite_r1 uit de kale reductie (kaal48.txt). Alles is technisch opschonen of per pixel repareren naar het model;
# elke wijziging wordt per zone geteld (rapport onderaan). Volgorde: (1) automatisch: ruis weg, buitenlijn; (2) handreparaties per zone
# (lijst HAND, elk met reden); (3) als laatste de enige toegestane vormafwijking: de punt sluit aan op het lijf (PUNT).
import numpy as np, sys
from PIL import Image
sys.path.insert(0,'gereedschap')
PAL={'.':(0,0,0),'K':(20,17,28),'D':(62,54,50),'d':(100,90,78),'m':(136,125,108),'l':(182,172,152),'h':(208,200,180),
     'R':(202,84,83),'r':(170,48,53)}
ORDE='.KDdmlhRr'
kaal=[list(r) for r in open('gereedschap/kaal48.txt').read().split()]
H,W=len(kaal),len(kaal[0])
g=[r[:] for r in kaal]
STEEN='hlm'; LIJN='dDK'
def nb4(y,x):
    for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
        yy,xx=y+dy,x+dx
        yield (g[yy][xx] if 0<=yy<H and 0<=xx<W else '.'),dy,dx
def nb8(y,x):
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if dy or dx:
                yy,xx=y+dy,x+dx; yield g[yy][xx] if 0<=yy<H and 0<=xx<W else '.'
# (1a) ruis in de steenvulling: losse pixel van een steentint waarvan minstens 3 van de 4 buren één andere steentint hebben -> die tint
GEZICHT=lambda y,x: 12<=y<=23 and 9<=x<=31   # ogen, rood patroon, mond: geen automatische ruisfilter
for y in range(H):
    for x in range(W):
        if g[y][x] in STEEN and not GEZICHT(y,x):
            n=[c for c,_,_ in nb4(y,x)]
            for c in STEEN:
                if c!=g[y][x] and n.count(c)>=3: g[y][x]=c; break
# (1b) losse lijnpixel (d/D zonder lijnbuur in 8-buurt) midden in steen -> vulling
for y in range(H):
    for x in range(W):
        if g[y][x] in 'dD' and not GEZICHT(y,x) and not any(c in LIJN for c in nb8(y,x)) and not any(c=='.' for c,_,_ in nb4(y,x)):
            n=[c for c,_,_ in nb4(y,x) if c in STEEN]
            if n: g[y][x]=max(set(n),key=n.count)
auto=[r[:] for r in g]
# (1c) buitenlijn: transparant rechts/onder -> zwart; alleen links/boven -> gekleurde selout (d, rood: r)
for y in range(H):
    for x in range(W):
        if g[y][x] in '.K': continue   # zwart uit het model blijft zwart
        t=[(dy,dx) for c,dy,dx in nb4(y,x) if c=='.']
        if not t: continue
        if any(dy==1 or dx==1 for dy,dx in t): g[y][x]='K'
        else: g[y][x]='r' if g[y][x] in 'Rr' else ('d' if g[y][x]!='K' else 'd')
# (2) handreparaties: (rij, kolom, letter, zone, reden) -- elke pixel die niet uit de kale reductie komt staat hier met reden
HAND=[]
try:
    from hand import HAND
except ImportError: pass
for y,x,c,zone,reden in HAND: g[y][x]=c
# (3) toegestane afwijking (Jordi): punt sluit aan op het lijf
PUNT=[]
try:
    from hand import PUNT
except ImportError: pass
for y,x,c in PUNT: g[y][x]=c
def zone(y,x):
    if y<=3: return 'bovenplaat'
    if y<=11: return 'hoofdband'
    if y<=23 and x<=31: return 'gezicht'
    if y<=24: return 'kop-zijkant/kin'
    if y>=39 and 18<=x<=33: return 'punt'
    if x<=14 or x>=36: return 'armen'
    return 'lijf'
from collections import Counter
diff=Counter(); lijst=[]
for y in range(H):
    for x in range(W):
        if g[y][x]!=kaal[y][x]:
            z=zone(y,x); diff[z]+=1
            bron='auto' if auto[y][x]!=kaal[y][x] and g[y][x]==auto[y][x] else ('buitenlijn' if g[y][x]!=auto[y][x] and not any(h[0]==y and h[1]==x for h in HAND) and (y,x,g[y][x]) not in PUNT else 'hand/punt')
            lijst.append((z,y,x,kaal[y][x],g[y][x],bron))
OUT='sprite_r1/'
open(OUT+'baltoy_r1.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
# 64x64, onderaan gecentreerd (1 px marge onder), geïndexeerd
pal=[PAL[c] for c in ORDE]; flat=sum(pal,())
idx=np.zeros((64,64),'uint8'); oy=64-H-1; ox=(64-W)//2
for y in range(H):
    for x in range(W): idx[oy+y,ox+x]=ORDE.index(g[y][x])
im=Image.fromarray(idx,'P'); im.putpalette(list(flat)+[0]*(48-len(flat))); im.save(OUT+'baltoy_r1.png',transparency=0)
rgb=Image.open(OUT+'baltoy_r1.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(rgb)
bg.convert('RGB').resize((512,512),Image.NEAREST).save(OUT+'baltoy_r1_8x.png')
with open(OUT+'diff_r1.txt','w') as f:
    f.write('afwijkingen t.o.v. kale reductie per zone: %s (totaal %d)\n'%(dict(diff),sum(diff.values())))
    for z,y,x,a,b,br in sorted(lijst): f.write('%s (%d,%d) %s->%s %s\n'%(z,y,x,a,b,br))
print(dict(diff),sum(diff.values()),'kleuren',len(set(sum(g,[]))),'offset',ox,oy)
