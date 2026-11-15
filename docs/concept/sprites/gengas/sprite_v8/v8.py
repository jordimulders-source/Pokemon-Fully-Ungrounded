# v8 (15 nov), twee varianten vanaf v7. Jordi over v7: "nu is het een soort vlak om de ogen heen wat totaal niet meer
# bij de rest van de sprite past" · "ja het moet er allemaal consistent uit zien ook".
#  v8a: bandenpatroon in de gezichtszone weer zoals het model (= v5-lijftinten: model met het gezichtsblok +5/+1
#       verschoven), Gengars ogen/grijns erop; Gengars d-pixels krijgen de bandtint eronder.
#  v8b: donkere band als golvende strook over het voorhoofd net boven de ogen; ogen op de lichtere bandtint (m);
#       onder de grijns de modelbanden.
#  Beide: Gengar-gezicht als blok op (x-6, y+5) (zoals v7); krul: haakse hoeken binnenlus afgerond + losse pixels
#  opgenomen; slot u vrijgemaakt (u -> b) voor Gengars tandlijn (106,98,123).
# Diffgrens t.o.v. v7: gezicht x 6-36, y 24-48; krul x 34-47, y 27-40.
import os, sys
import numpy as np
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))+'/'
V5=[list(l.rstrip('\n')) for l in open(D+'../sprite_v5/raster.txt')][:64]
V7=[l.rstrip('\n') for l in open(D+'../sprite_v7/raster.txt')][:64]
def zone(x,y): return (6<=x<=36 and 24<=y<=48) or (34<=x<=47 and 27<=y<=40)
g=np.array(Image.open(D+'../../../../../graphics/pokemon/gengar/anim_front.png'))[:64]
MAP={1:'W',2:'H',3:'u',5:'R',6:'E',7:'H',14:'a',15:'K'}       # 13 (d) niet: die krijgt de bandtint eronder
FACE={1,2,3,4,5,6,7,14,15}
delen=[('linkeroog',18,23,28,32),('rechteroog',28,36,26,31),('grijns',18,38,32,40)]
def gezicht():
    for nm,x0,x1,y0,y1 in delen:
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):
                v=int(g[y,x]); nb=g[y-1:y+2,x-1:x+2].flatten()
                if v in FACE or (v==13 and any(int(n) in {1,2,3,4,5,6,7} for n in nb)):
                    if nm=='grijns' and y==32 and x<30: continue
                    yield nm,x-6,y+5,v
def bouw(variant):
    R=[r[:] for r in V5]; log=[]
    def zet(x,y,c,reden):
        assert zone(x,y),(x,y)
        if R[y][x]!=c: log.append(f'({x},{y}) {R[y][x]}->{c}  {reden}'); R[y][x]=c
    # 1) slot u vrij: oude u (rand linksboven, wig) -> b
    for y in range(64):
        for x in range(64):
            if R[y][x]=='u': zet(x,y,'b','u -> b (slot vrij voor tandlijn)')
    # 2) oud modelgezicht van v5 weg, gaten vullen met de lijftint van de buren
    gat=set()
    for x0,x1,y0,y1 in [(12,18,29,36),(23,32,29,37),(13,32,37,46)]:
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):
                if R[y][x] in 'KERWHa': gat.add((x,y))
    open_=set(gat)
    while open_:
        nieuw={}
        for (x,y) in open_:
            b=[R[y+dy][x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if (dx or dy) and (x+dx,y+dy) not in open_ and R[y+dy][x+dx] in 'mbl']
            if b: nieuw[(x,y)]=max(set(b),key=lambda c:(b.count(c),c=='b'))
        for (x,y),c in nieuw.items(): zet(x,y,c,'oud modelgezicht weg, lijftint buren'); open_.discard((x,y))
    if variant=='b':
        # onderrand (laatste b-rij) en bovenrand van de voorhoofdband per kolom; golvend, sluit rechts aan op de
        # bestaande band (34,29)/(35,28) en links op de randvlek (x9-13, rij 25-28)
        lo={8:32,9:32,10:31,11:31,12:31,13:31,14:30,15:30,16:31,17:31,18:32,19:32,20:32,21:32,22:31,23:31,24:31,
            25:30,26:30,**{x:29 for x in range(27,34)}}
        hi={8:29,**{x:25 for x in range(9,14)},**{x:28 for x in range(14,18)},**{x:29 for x in range(18,24)},24:28,25:28}
        for x in range(8,34):
            for y in range(hi.get(x,28),lo[x]+1):
                if R[y][x] in 'mlba': zet(x,y,'b','voorhoofdband')
            t=hi.get(x)
            if t and R[t-1][x]=='l' and zone(x,t-1): zet(x,t-1,'m','overgang l-m-b boven de band')
            for y in range(lo[x]+1,41):
                if R[y][x]=='b' or (R[y][x]=='a' and (x==8 or (x,y)==(10,37))): zet(x,y,'m','lichtere band onder de voorhoofdband')
    # 3) Gengar-gezicht als blok op (x-6, y+5)
    for nm,x,y,v in gezicht():
        if v==13: continue
        zet(x,y,MAP[v],f'Gengar {nm} idx {v:x}')
    # 4) krul: haakse hoeken binnenlus afronden, losse pixels opnemen
    for (x,y,c,r) in [(38,34,'l','hoek binnenlus afgerond'),(38,36,'l','hoek binnenlus afgerond'),
                      (38,28,'m','losse l opgenomen'),(36,29,'m','losse l opgenomen'),(39,37,'l','losse m opgenomen'),
                      (39,33,'l','losse m opgenomen'),(43,34,'l','losse m opgenomen')]:
        zet(x,y,c,'krul: '+r)
    buiten=[(x,y) for y in range(64) for x in range(64) if V7[y][x]!=R[y][x] and not zone(x,y)]
    open(D+f'raster_v8{variant}.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
    open(D+f'raster_v8{variant}.txt.log','w').write('\n'.join(log)+'\n')
    print(f'v8{variant}: {len(log)} wijzigingen t.o.v. v5; pixels anders dan v7 buiten de diffgrens: {len(buiten)}')
for v in 'ab': bouw(v)
