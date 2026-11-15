# r7b: bolbinnenkant opnieuw (coördinator na r7): barst = enige donkere lijn (Y, modelpad, d);
# storm = witte krullende banen (e met w-kern) + losse vlokken op doorkijktint b; glasrand c/e en glans zoals r7. Geen a binnen de bol.
# Basis raster_r7.txt (buiten de bol = r6). Vanuit sneeuwbolslak_fase2/: python3 sprite/maker/r7b_bouw.py
import math
R=[list(l.rstrip('\n')) for l in open('sprite/maker/raster_r7.txt')]
O=[r[:] for r in R]
CX,CY=31.5,31.0
BARST=[(36,25),(35,26),(35,27),(35,28),(34,29),(33,30),(32,30),(31,31),(30,32),(30,33),   # stam + linkertak
       (36,29),(36,30),(37,31),(37,32),(37,33),(36,34),(36,35),(36,36),(37,37)]           # rechtertak
def binnen(x,y):
    return 22<=x<=41 and 23<=y<=38 and O[y][x] not in '#.' and math.hypot(x-CX,y-CY)<=10.2 and not (O[y][x]=='d' and (x<=23 or y<=24))
P={}
for y in range(23,39):
    for x in range(22,42):
        if not binnen(x,y): continue
        r=math.hypot(x-CX,y-CY); h=math.degrees(math.atan2(y-CY,x-CX))
        P[(x,y)]=('e' if (-60<=h<=150 and r>8.8) else 'c') if r>8.3 else 'b'
for p in BARST: P[p]='d'
def zet(ch,pts,over_barst=False):
    for p in pts:
        if p in P and (over_barst or P[p]!='d'): P[p]=ch
# glans linksboven (zoals r7)
zet('e',[(x,y) for x in range(23,29) for y in range(25,29) if math.hypot(x-25.3,y-26.5)<=2.6]); zet('w',[(25,26),(26,26),(25,27)])
# stormbanen: krullende bogen rond het midden (gebogen, trappen 1-2-3)
A=[(27,24),(28,24),(29,23),(30,23),(31,24),(32,24),(33,25),(34,25)]            # boven, van links naar de barst
A2=[(37,26),(38,27),(38,28),(39,29),(39,30)]                                         # loopt rechts door achter de barst omlaag
B=[(23,30),(24,31),(24,32),(25,33),(26,34),(27,34),(28,35),(29,35),(30,36),(31,36),(32,35),(33,35),(34,34)]  # links omlaag en onderlangs naar rechts
C=[(29,28),(30,28),(31,27),(32,27),(33,28),(28,29),(27,30),(27,31),(28,32)]             # binnenkrul (draait linksom rond het midden)
zet('e',A+A2+B+C)
zet('w',[(30,23),(28,35),(31,27),(39,29)])                                           # kern van de banen
# losse vlokken op de doorkijktint
zet('w',[(26,31),(33,32),(35,33),(29,26),(32,33),(38,33),(24,35),(34,37)])
zet('e',[(32,34),(29,31)])
for (x,y),ch in P.items(): R[y][x]=ch
for y in range(64):
    for x in range(64):
        if R[y][x]!=O[y][x] and not (22<=x<=41 and 23<=y<=38): raise SystemExit(f'buiten bol {x},{y}')
open('sprite/maker/raster_r7b.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
print('a in de bol:',[(x,y) for (x,y),c in P.items() if c=='a'])
print('d in de bol buiten barst:',[(x,y) for (x,y),c in P.items() if c=='d' and (x,y) not in BARST])
