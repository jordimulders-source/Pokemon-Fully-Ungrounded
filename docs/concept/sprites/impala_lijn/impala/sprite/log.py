# Schrijft rN/log.txt: afwijkingen van de kale reductie per zone en per stap, zelf gezette pixels, oogzone, kleuren; en rN/kaal.png
import sys, json, numpy as np
from collections import Counter, defaultdict
from PIL import Image
RN=sys.argv[1]; m=json.load(open(f'{RN}/grid.json')); OX,OY=m['OX'],m['OY']; g=m['grid']; k=m['kaal']; H=len(g); W=len(g[0])
Z=np.load('kaal_zone.npy')
def anat(x,y):
    if Z[y,x]==1 or (y<=17 and 'hoorn' in str(steps.get((x,y),''))): return 'hoorns'
    if y<=30 and x<=24: return 'kop+hals'
    if y<=45: return 'lijf+staart'
    return 'poten'
steps=defaultdict(list)
for l in open(f'{RN}/wijzigingen.txt'):
    st=l.split()[0]; x,y=map(int,l.split()[1].strip('()').split(',')); steps[(x,y)].append(st)
tot=Counter(); per=defaultdict(Counter); npx=Counter()
for y in range(H):
    for x in range(W):
        if g[y][x]=='.': continue
        npx[anat(x,y)]+=1
        if g[y][x]!=k[y][x]: tot[anat(x,y)]+=1; per[anat(x,y)][steps[(x,y)][-1] if steps[(x,y)] else '?']+=1
L=[f'{RN}: afwijkingen t.o.v. de kale reductie (kaal gemapt = modelreductie met alleen de Gen 3-tintkeuze per zone)',
   ('Basis r2: per cel lijn (>=50% zwarte modellijn) of meerderheids-toonklasse van het model (celklas.py); flank: relatieve helderheid flankpixels.' if RN!='r1' else 'Basis: per cel lijn (>=50% zwarte modellijn) of vlakkleur onder de lijn (gemiddelde, niet-lijnpixels) -> tint via modelhelderheid.'),'']
for z in ['hoorns','kop+hals','lijf+staart','poten']:
    L.append(f'{z:12s} {tot[z]:3d} van {npx[z]:4d} px  ({", ".join(f"{s} {n}" for s,n in per[z].most_common())})')
L.append(f'totaal       {sum(tot.values()):3d} van {sum(npx.values())} px')
L+=['','Uitleg stappen: lijn = 1-px buitenlijn dicht + gekleurde selout op randen die naar boven/linksboven wijzen;',
    'binnenlijn = modellijn binnen het silhouet -> donkerste eigen tint (D of 1), geen zwart;',
    'hoorngrens = modellijn tussen hoorn en kuif/kop (valt bij de reductie weg) uit de zonegrens van de modelsegmentatie;',
    'ontkorrel = tintvlakje <3 px -> meest voorkomende buurtint (niet in hoorns/oog/neus);',
    'strepen_weg = de vier bilstrepen (Jordi) -> vachttint van het model naast de streep (helderheid van de lijfpixels in die cel).','',
    'ZELF GEZETTE PIXELS (niet uit het model; Jordi\'s toegestane afwijking), 64x64-coordinaten:']
for e in json.load(open(f'extra_{RN}.json')):
    zn,x,y=e[:3]
    L.append(f'  {zn}: ({x+OX},{y+OY}) -> zwart')
L+=['','OOGZONE (wordt later vervangen door een Gen 3-oog): 64x64 x %d-%d, y %d-%d (beschermd: niet ontkorreld/omgelijnd).'%(8+OX,15+OX,20+OY,26+OY),
    'Huidige oogpixels (64x64-coordinaten, rij voor rij x %d-%d):'%(8+OX,15+OX)]
for y in range(20,27): L.append('  y%2d '%(y+OY)+g[y][8:16])
pal=sorted(set(''.join(g))-{'.'}); L+=['',f'Kleuren: {len(pal)} + transparant = {len(pal)+1} ({" ".join(pal)})']
open(f'{RN}/log.txt','w').write('\n'.join(L)+'\n'); print('\n'.join(L))
kim=Image.new('RGBA',(64,64)); kk=Image.open('kaal.png').convert('RGBA'); kim.paste(kk,(OX,OY),kk); kim.save(f'{RN}/kaal.png')
