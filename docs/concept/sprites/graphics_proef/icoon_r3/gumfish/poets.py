"""Poetsen per zone op de gekozen onderlaag (D: lijf 0,42, kop 0,62, staartvin 0,58).
Elke pixel komt uit de onderlaag of uit een benoemde regel hieronder (zone + reden).
python3 poets.py -> icon_f1.png (32x32)"""
import sys,os,numpy as np
from collections import Counter
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))+'/'
sys.argv=['bouw.py','D','0.42','0.62','0.58']; __file__=H+'bouw.py'
exec(open(H+'bouw.py').read().split("if __name__")[0])
c=np.array(Image.open(H+'D.png')); b=c.copy(); LOG=Counter()
def put(zone,pts,v):
    for x,y in pts:
        if c[y,x]!=v: c[y,x]=v; LOG[zone]+=1
def ic(x,y,n): p=naar_icoon(x+0.5,y+0.5,n); return int(np.floor(p[0])),int(np.floor(p[1]))
binnen=lambda x,y: c[y,x]>0 and all(c[y+dy,x+dx]>0 for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
fpad=np.pad(fr>0,1); frand=(fr>0)&~(fpad[:-2,1:-1]&fpad[2:,1:-1]&fpad[1:-1,:-2]&fpad[1:-1,2:])
# 1 vorm: rugdal tussen kop en lijf dicht (front: dal van 1-2 px, geen gat)
put('vorm rugdal',[(15,18)],15)
# 2 binnenlijnen: alleen waar de front een donkere lijn binnen het silhouet heeft (deel over deel: borstvin, staartaanzet)
for n,zone in (('borstvin','binnenlijn borstvin'),('staartvin','binnenlijn staartaanzet')):
    i=names.index(n)
    for y,x in zip(*np.nonzero((lab==i)&np.isin(fr,[1,2])&~frand)):
        X,Y=ic(x,y,n)
        if binnen(X,Y) and c[Y,X] not in (15,14): put(zone,[(X,Y)],14)
# 3 strepen borstvin: lichtroze frontpixels (index 11) van de borstvin, zelfde transformatie
i=names.index('borstvin')
for y,x in zip(*np.nonzero((lab==i)&(fr==11))):
    X,Y=ic(x,y,'borstvin')
    if binnen(X,Y) and c[Y,X]==6: put('strepen borstvin',[(X,Y)],11)
# 4 strepen opschonen: de stralen in de front liggen om de rij (front-rijen 40/43/45/48 -> icoon 22/23/24/25);
#   een vlek van 2x3 is blur, dus één streep per straal op de oneven-vrije rijen 22, 24, 26 en lijfkleur ertussen
put('strepen borstvin',[(16,23),(17,23),(18,23),(19,23)],6)
put('strepen borstvin',[(17,24)],11)
# 5 oog: opbouw van het front-oog (2x2: witte glans linksboven, rest donker), op de berekende plek (19,45)->(11,24)
put('oog',[(11,24)],3); put('oog',[(12,24),(11,25),(12,25)],15)
# 6 mond: lachlijn uit de front (10,48)-(12..18,49)-(19,48) -> (5,26),(6..10,27),(11,26)
put('mond',[(5,26),(11,26)]+[(x,27) for x in range(6,11)],15)
# 7 lippen: bovenlip front rij 48 (roze/lichtrood) -> rij 26 x6-10 roze; onderlip front rij 49-50 -> rij 28 x7-11 roze
put('lippen',[(x,26) for x in range(6,11)],10); put('lippen',[(x,28) for x in range(7,12)],10)
# 8 losse pixel: lichtroze stip (front-glansje (9,41) van 1 px) naast de omlijning -> lijfkleur (13a: klein detail)
put('losse pixels',[(4,24)],6)
# 9 oog: front-oog is 2 breed x 3 hoog donker (rij 45-47) en loopt over in de mondhoek -> (12,26) donker
put('oog',[(12,26)],15)
# 10 mondopening links: front (10-11,48) donker op de rij van de bovenlip -> (6,26)
put('mond',[(6,26)],15)
# 11 rond (bol, geen rechte stukken van >= 4): kopkruin en kin afronden met 45-graden-trapjes, rug van de romp idem
for x,y in [(7,16),(13,16),(7,29),(13,29),(18,17)]: c[y,x]=0; LOG['rond']+=1
put('rond',[(13,17),(18,18)],15); put('rond',[(7,28)],14)
# 12 binnenlijn lipeinde: front (21,48-50) donker = lip over het lijf -> (12,27)
put('binnenlijn lipeinde',[(12,27)],14)
# 13 rugdal als dal: de kopkoepel loopt door tot de lijn kop-over-lijf (15,19) -> (15,17) omlijning, (14,18) kopkleur
put('vorm rugdal',[(15,17)],15); put('vorm rugdal',[(14,18)],10)
if __name__=='__main__':
    im=Image.fromarray(c,'P'); im.putpalette(IP.flatten().tolist()); im.save(H+'icon_f1.png',transparency=0)
    print(dict(LOG))
