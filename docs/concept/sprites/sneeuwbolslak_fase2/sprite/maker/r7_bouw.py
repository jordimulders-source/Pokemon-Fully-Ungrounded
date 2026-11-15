# r7: EINDKEURING_r6. Basis = raster_r7_m3a.txt (eindkeuring_r6_moet.py: M1-M3a op r6).
# M3b: alleen de bolbinnenkant (x22-41, y23-38), barst (d) en buitenlijn blijven staan.
# Glas: lichte rand (c, rechts/onder e = licht dat door het glas valt), glans linksboven (w-kern in e).
# Inhoud: doorkijktint b, storm als drie wervelbanen a (A boven, B midden die links omkrult, D onder terug naar de barst),
# lichte sneeuwsliert c ertussen, lichte kern e onder de barstvork, losse vlokken w.
# Vanuit sneeuwbolslak_fase2/: python3 sprite/maker/r7_bouw.py
import math
R=[list(l.rstrip('\n')) for l in open('sprite/maker/raster_r7_m3a.txt')]
O=[r[:] for r in R]
CX,CY=31.5,31.0
BARST={(35,26),(35,27),(35,28),(34,29),(36,29),(32,30),(33,30),(36,30),(31,31),(37,31),(30,32),(37,32),(37,33),(36,34),(36,35),(36,36),(37,37),(36,25),(30,33)}
def binnen(x,y):
    return 22<=x<=41 and 23<=y<=38 and R[y][x] not in '#.' and (x,y) not in BARST and math.hypot(x-CX,y-CY)<=10.2 and not (R[y][x]=='d' and (x<=23 or y<=24))
P={}
for y in range(23,39):
    for x in range(22,42):
        if not binnen(x,y): continue
        r=math.hypot(x-CX,y-CY); hoek=math.degrees(math.atan2(y-CY,x-CX))  # 0 = rechts, 90 = onder
        if r>8.3: P[(x,y)]='e' if (-60<=hoek<=150 and r>8.8) else 'c'
        else: P[(x,y)]='b'
def zet(ch,pts):
    for p in pts:
        if p in P: P[p]=ch
# glans linksboven
zet('e',[(x,y) for x in range(23,29) for y in range(25,29) if math.hypot(x-25.3,y-26.5)<=2.6])
zet('w',[(25,26),(26,26),(25,27)])
# lichte sneeuwsliert (c) tussen de banen: boven langs A en de band op y29
zet('c',[(28,23),(29,23),(30,23),(31,23),(32,23),(33,23),(27,24),(32,24),(33,24),(34,24),(35,24),(36,24),(29,25),(30,25),(36,26),(37,26),(37,27),
         (29,26),(30,26),(31,26),(32,26),(33,26),
         (24,29),(25,29),(26,29),(27,29),(28,29),(29,29),(30,29),(29,28),(30,28),(31,28),(32,28),(33,28),(34,28),
         (26,31),(27,31),(28,31),(29,31),(27,32),(28,32),(29,32),(26,33),(28,33),(29,33),
         (27,34),(28,34),(29,34),(30,34),(31,34),(30,35),(31,35),(32,35),(32,36),(33,36),(34,36),(35,36)])
# lichte kern onder de barstvork
zet('e',[(32,31),(33,31),(34,31),(31,32),(32,32),(33,32),(34,32),(35,32),(31,33),(32,33),(33,33),(34,33),(32,34),(33,34),(34,34),(35,34),(33,35),(34,35)])
zet('e',[(35,31),(36,31),(36,32),(35,33),(36,33)]); zet('c',[(35,35)])
# stormbanen (a = kern, b = rand)
zet('a',[(28,24),(29,24),(30,24),(31,25),(32,25),(33,25),(34,25),(36,27),(37,28),(38,29)])          # A, buigt rechts omlaag (C)
zet('a',[(29,30),(28,30),(27,30),(26,30),(25,30),(24,31),(23,32),(23,33),(24,34)])                  # B, krult links omlaag
zet('a',[(25,35),(26,35),(27,36),(28,36),(29,36),(30,37),(31,37)])                                 # D, onder terug naar rechts
zet('b',[(38,30),(38,31),(39,32),(39,33)])                                                        # C dun
# opruimen: tintvlakjes < 3 px die geen vlok zijn
zet('a',[(31,24)]); zet('b',[(39,27)]); zet('e',[(39,35),(27,38),(36,38)])
# vlokken
zet('w',[(27,33),(33,37),(26,29),(30,27)])
for (x,y),ch in P.items(): R[y][x]=ch
for y in range(64):
    for x in range(64):
        if R[y][x]!=O[y][x] and not (22<=x<=41 and 23<=y<=38): raise SystemExit(f'buiten bol {x},{y}')
open('sprite/maker/raster_r7.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
print('gewijzigd t.o.v. M3a-basis:',sum(R[y][x]!=O[y][x] for y in range(64) for x in range(64)))
