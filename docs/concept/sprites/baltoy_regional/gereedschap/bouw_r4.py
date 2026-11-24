# r4A: start = kale 2x2-reductie (gereedschap/kaal34.txt, uit half_r4.py). Per zone zijn pixels gerepareerd waar de
# reductie het model kapotmaakt (ogen, band, armen, punt, buitenlijn), steeds naar het model (natief raster, klassen.py).
# Uitvoer: sprite_r4/baltoy_r4A.png/.txt/_8x.png + aantal afwijkende pixels per zone t.o.v. de kale reductie.
import sys; sys.path.insert(0,'gereedschap'); from r4lib import *
kaal=lees('gereedschap/kaal34.txt'); H,W=len(kaal),len(kaal[0])
g=[['.']*W for _ in range(H)]
def p(y,x,c): g[y][x]=c
def h(y,x0,x1,c):
    for x in range(x0,x1+1): g[y][x]=c
def v(x,y0,y1,c):
    for y in range(y0,y1+1): g[y][x]=c
ZONES=[]
def zone(n,y0,y1,x0,x1): ZONES.append((n,y0,y1,x0,x1))
# ================= KOP (rijen 0-16) =================
zone('kop: bovenvlak + hoofdband',0,8,6,27)
h(0,9,20,'D'); h(0,21,23,'K')                         # bovenrand: selout links/boven, zwart rechts
p(1,8,'D'); h(1,9,20,'l'); p(1,21,'D'); h(1,22,23,'m'); h(1,24,25,'K')
p(2,7,'D'); h(2,8,21,'d'); h(2,22,25,'m'); p(2,26,'K')  # groef boven de band
p(3,7,'D'); h(3,8,21,'l'); h(3,22,25,'m'); p(3,26,'K')
for y in (4,5,6,7): p(y,6,'D'); h(y,7,21,'l'); h(y,22,26,'m'); p(y,27,'K')
p(4,26,'K'); p(4,27,'.')                               # zijkant rij 4 nog smal (model: schuine bovenhoek)
# chakana x9-13, r3-7: getrapt kruis, omlijnd in groef-d, licht kruis binnenin
for y,s in ((3,'.ddd.'),(4,'ddldd'),(5,'dllld'),(6,'ddldd'),(7,'.ddd.')):
    for i,c in enumerate(s):
        if c!='.': p(y,9+i,c)
# trapmotief rechts: twee treden omlaag naar rechts (model: r7-15 natief, kol 32-42)
h(3,15,17,'d'); p(4,17,'d'); h(5,17,19,'d'); p(6,19,'d'); h(7,19,21,'d')
# zijkant: één trede in D (model: meander op de zijkant)
p(4,23,'D'); h(5,23,25,'D'); p(6,25,'D')
h(8,7,21,'K'); h(8,22,26,'m'); p(8,27,'K')             # onderrand band
zone('gezicht',9,16,7,26)
p(9,7,'D'); p(9,8,'l'); h(9,9,12,'R'); h(9,13,15,'l'); h(9,16,19,'R'); p(9,20,'l'); p(9,21,'D'); p(9,22,'m'); h(9,23,27,'K')
for y in range(10,15): p(y,7,'D'); h(y,8,20,'l'); p(y,21,'D'); h(y,22,24,'m'); p(y,25,'K')
p(15,8,'D'); h(15,9,20,'l'); p(15,21,'D'); h(15,22,23,'m'); p(15,24,'K')
h(16,9,23,'K')   # (9,8)/(9,20) steen: bovenhoek van de rode boog rond, zoals het model
# rood patroon: boogjes over de ogen, V tussen de ogen (punt x14), zijkanten omlaag
p(10,14,'l')   # licht driehoekje boven de V (model)
for y,x in ((10,8),(10,9),(10,13),(10,15),(10,19),(10,20),(11,8),(11,14),(11,20),(12,14)): p(y,x,'R')
for y,x in ((12,8),(12,20),(13,14)): p(y,x,'r')
# ogen: ronde ring 5x5 met horizontale streep, links x9-13, rechts x15-19, rijen 10-14
for x0 in (9,15):
    for y,s in ((10,'.DDD.'),(11,'D...D'),(12,'DDDDD'),(13,'D...D'),(14,'.DDD.')):
        for i,c in enumerate(s):
            if c!='.': p(y,x0+i,'D' if y==12 else 'd')   # ring in de groeftint (model: middengrijze ring), streep donker
# mond (model: klein plat mondje onder de V)
h(15,13,15,'d'); p(15,14,'D')
# ================= LIJF (rijen 17-28) =================
zone('lijf',17,28,10,24)
p(17,10,'K'); h(17,11,19,'m'); p(17,20,'D'); h(17,21,23,'m'); p(17,24,'K')      # schaduw onder de kop
p(18,10,'D'); h(18,11,19,'M'); p(18,20,'D'); h(18,21,22,'m')
for y in range(19,28): p(y,10,'D'); h(y,11,19,'l'); p(y,20,'D'); h(y,21,23,'m'); p(y,24,'K')
h(27,11,19,'M')                       # schaduw onderaan
h(28,11,14,'K'); h(28,21,23,'K')
# kerven: twee verticale groeven (zuil) x14/x16, links één richel, rechts twee
v(14,20,26,'d'); v(16,20,26,'d'); h(22,11,12,'d'); h(21,18,19,'d'); h(24,18,19,'d')   # richels raken de zuil niet (anders letters)
# ================= PUNT (rijen 28-33), aan het blok vast =================
zone('punt',28,34,11,23)
h(28,15,20,'m')                                        # bovenvlak punt = schaduw onder het blok (geen zwarte scheidingslijn)
p(29,14,'K'); h(29,15,20,'m'); p(29,21,'K')
p(30,14,'K'); h(30,15,20,'M'); p(30,21,'K')
p(31,15,'K'); h(31,16,18,'l'); p(31,19,'M'); p(31,20,'K')
p(32,16,'K'); p(32,17,'l'); p(32,18,'l'); p(32,19,'K')
h(33,17,18,'K')
# ================= ARMEN =================
zone('arm links',18,28,0,10)
h(18,8,9,'D'); v(10,19,20,'M')                          # schouder; aanzet in het lijf zonder lijn
h(19,6,7,'D'); h(19,8,9,'l')
for y in range(20,26):
    x=25-y; p(y,x,'D'); h(y,x+1,x+2,'l'); h(y,x+3,x+4,'M'); p(y,x+5,'K')
p(20,10,'M'); p(21,10,'D')
p(26,0,'D'); p(26,1,'l'); h(26,2,3,'M'); p(26,4,'K')
p(27,0,'K'); h(27,1,2,'M'); p(27,3,'K')
h(28,1,2,'K')
zone('arm rechts',18,30,21,33)
h(18,23,24,'D')
p(19,23,'M'); p(19,24,'M'); h(19,25,26,'D')
p(20,22,'K'); h(20,23,24,'M'); h(20,25,26,'l'); p(20,27,'D')
for y in range(21,28):
    xi={21:23,22:24,23:25,24:26,25:27,26:28,27:28}[y]; xo={21:28,22:29,23:30,24:31,25:32,26:33,27:33}[y]
    p(y,xi,'K'); 
    for x in range(xi+1,xo): g[y][x]='M' if x-xi<=2 else 'l'
    p(y,xo,'D' if y<=22 else 'K')
p(24,25,'.'); h(25,25,26,'.')
p(28,29,'K'); h(28,30,31,'M'); p(28,32,'l'); p(28,33,'K')
p(29,29,'K'); h(29,30,31,'M'); p(29,32,'K')
h(30,30,31,'K')
# ---------------------------------------------------
ys=[y for y in range(H) if any(c!='.' for c in g[y])]
rows=[''.join(r) for r in g]
open('sprite_r4/baltoy_r4A.txt','w').write('\n'.join(rows)+'\n')
for y,r in enumerate(rows): print('%2d %s'%(y,r))
for n,y0,y1,x0,x1 in ZONES:
    d=sum(1 for y in range(y0,y1+1) for x in range(x0,x1+1) if g[y][x]!=kaal[y][x])
    print('zone %-28s afwijkend van kale reductie: %d px'%(n,d))
print('totaal afwijkend:',sum(1 for y in range(H) for x in range(W) if g[y][x]!=kaal[y][x]),'van',sum(1 for r in rows for c in r if c!='.'))
pi=png(rows,'sprite_r4/baltoy_r4A.png'); op(rgba(pi),(255,255,255,255),8).save('sprite_r4/baltoy_r4A_8x.png')
