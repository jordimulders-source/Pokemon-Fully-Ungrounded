# r3: kale reductie (kaal_r3.txt, schrap2.py) + benoemde reparaties per zone naar het model.
# Elke reparatie staat hieronder als (rij, kolom, tekens); '.' = achtergrond. Telling per zone in tel3.py.
import numpy as np
CH='.#kdgGLcChWwvpor'
o=np.loadtxt('kaal_r3.txt',dtype=int)
g=[[CH[v] for v in r] for r in o]
def put(r,c,s,zone):
    for k,ch in enumerate(s):
        if ch!=' ': g[r][c+k]=ch
REP=[]
def P(zone,r,c,s): REP.append((zone,r,c,s))
# ---------- POTEN (model: kabel = omlijning | glans | vulling | omlijning, ring = witte band, 2 koperen klauwtjes)
# eerst het hele potengebied leeg onder romp/kin (rij 24+ links van de achterlijfrand, rij 32+ overal)
for r in range(24,46):
    for c in range(0,50):
        if r>=33 or c<26: g[r][c]='.'
for c in range(10,15): g[23][c]='.'
P('poten',21,21,'chc#kkk#')
P('poten',22,21,'chc#kkk#')
def K(zone,rijen):  # kabelstuk: per rij de linker kolom; doorsnede c|h|c|# (selout, glans, vulling, omlijning)
    for r,c in rijen: P(zone,r,c,'chc#')
# poot 1: boog onder de kin langs naar links-omlaag, ring, kabel bijna recht omlaag met bocht naar links onderaan
P('poten',23,13,'#####')
P('poten',24,10,'###hhhhh#')
P('poten',25, 8,'#hhcccc#')
P('poten',26, 7,'chcc###')
P('poten',27, 7,'chc#')
P('poten',28, 6,'#WWWW#'); P('poten',29, 6,'#wwww#'); P('poten',30, 6,'######')
K('poten',[(31,7),(32,7),(33,7),(34,6),(35,6),(36,5)])
P('poten',23,13,'###chc##')
# poot 2: vanuit het borststuk omlaag, voor de boog van poot 1
K('poten',[(24,16),(25,15),(26,15),(27,14)])
P('poten',28,13,'#WWWW#'); P('poten',29,13,'#wwww#'); P('poten',30,13,'######')
K('poten',[(31,14),(32,14),(33,14),(34,13)])
# poot 3
K('poten',[(23,21),(24,21),(25,22),(26,22),(27,22),(28,22),(29,23)])
P('poten',30,22,'#WWWW#'); P('poten',31,22,'#wwww#'); P('poten',32,22,'######')
K('poten',[(33,23),(34,23),(35,23),(36,23),(37,24),(38,24),(39,25),(40,25),(41,26)])
# poot 4: boog over de onderkant van het achterlijf naar rechts, ring aan de achterlijfrand, schuin naar rechts-omlaag
# boog als schuine kabel (model: 2-3 rijen dik over het grijs van de onderkant), per kolom: omlijning|glans|vulling|omlijning
def kol(c,boven,top,onder):
    for k,ch in enumerate(boven): g[22+1+k][c]=ch if ch!=' ' else g[23+k][c]
    for k,ch in enumerate('#hc#'): g[top+k][c]=ch
    for k,ch in enumerate(onder): g[top+4+k][c]=ch
LATER=[]
LATER.append(lambda: [kol(c,'',23,'') for c in (25,26,27)])
LATER.append(lambda: [kol(c,'#',24,'#') for c in (28,)])
LATER.append(lambda: [kol(c,'L',24,'G#') for c in (29,30)])
LATER.append(lambda: [kol(c,'dd',25,'G#') for c in (31,)])
LATER.append(lambda: [kol(c,'dd',25,'d#') for c in (32,)])
LATER.append(lambda: [kol(c,'GG',25,'d#') for c in (33,)])
LATER.append(lambda: [kol(c,'GGG',26,'##') for c in (34,)])
P('poten',23,35,'GGGdd'); P('poten',24,35,'GGddd'); P('poten',25,35,'GGddd')
P('poten',26,35,'####')
P('poten',26,39,'GGGdddh#')
for r in (27,28,29): P('poten',r,35,'chc#')
P('poten',27,39,'GGdkkkh#'); P('poten',28,39,'Ghkkkkh#'); P('poten',29,39,'kkkkk##')
P('poten',27,26,'.#'); P('poten',28,26,'..')
P('poten',30,34,'#WWWW#kk##'); P('poten',31,34,'#wwww###'); P('poten',32,34,'######')
K('poten',[(33,35),(34,36),(35,36),(36,37),(37,37),(38,38),(39,38)])
# klauwtjes: twee koperdraadjes vast aan het kabeleinde (model: poot 1+2 naar links, 3 omlaag, 4 naar rechts)
P('klauw',37,2,'.oor###'); P('klauw',38,0,'.oo#o#'); P('klauw',39,1,'##o#'); P('klauw',40,3,'#')
P('klauw',35,11,'oor###'); P('klauw',36,10,'o#o#'); P('klauw',37,10,'#.#')
P('klauw',42,25,'#oro#'); P('klauw',43,25,'#o##oo#'); P('klauw',44,26,'#o####'); P('klauw',45,27,'#')
P('klauw',39,42,'o#'); P('klauw',40,38,'##roo#'); P('klauw',41,39,'#o#oo#'); P('klauw',42,40,'#o##'); P('klauw',43,41,'#')
# ---------- KOP: ronder aan de linkerkant (Jordi), ^-ogen naar het model, omlijning dicht
P('kop',13,2,'#k'); P('kop',17,2,'.#'); P('kop',18,3,'#'); P('kop',20,4,'#')
# rechteroog ^ (model x31-36, y38-43): top, poten schuin uit elkaar
P('oog',14,11,'pkp')
# linkeroog ^ smaller (ver oog in 3/4), linkerpoot langs de rand van het vizier zoals het model
P('oog',13,3,'kp'); P('oog',14,3,'pkp'); P('oog',15,3,'pkp'); P('oog',16,3,'pkkp'); P('oog',17,4,'kkp')
# ---------- ACHTERLIJF: omlijning rechts dicht (reductie schrapte hem)
P('romp',19,45,'#'); P('romp',20,45,'#')
# ---------- VOELSPRIETEN: omlijning boven de knoppen dicht, kabeltinten (C/h) in de grijze sprieten -> grijs
P('spriet',2,4,'##'); P('spriet',3,3,'#g#'); P('spriet',4,2,'#'); P('spriet',4,6,'#'); P('spriet',5,1,'#')
P('spriet',6,0,'#L'); P('spriet',7,1,'G'); P('spriet',7,6,'g'); P('spriet',8,6,'g')
P('spriet',2,12,'###'); P('spriet',3,11,'#'); P('spriet',3,15,'#'); P('spriet',4,10,'#'); P('spriet',4,15,'#'); P('spriet',5,9,'#')
P('spriet',8,12,'g')
# ---------- KOPDAK: omlijning boven de koepel dicht
P('kop',7,8,'###'); P('kop',7,13,'##'); P('kop',8,8,'#'); P('kop',8,15,'#'); P('kop',9,16,'#')
# ---------- VLEUGELS / BORSTSTUK: losse kabeltinten weg, losse omlijning in het zwart weg
P('vleugel',9,25,'#'); P('vleugel',11,37,'vvv')
P('borst',14,26,'d'); P('borst',20,25,'kkk#'); P('borst',21,25,'kkk#')
for z,r,c,s in REP: put(r,c,s,z)
for f in LATER: f()
# kop: grijze rand/kin had de blauwige kabelglans (h) uit de reductie -> grijs G, kin linksboven L
for r in range(8,23):
    for c in range(0,19):
        if g[r][c]=='h': g[r][c]='G'; REP.append(('kop',r,c,'G'))
g[20][6]='L'
open('r3_stap1.chr','w').write('\n'.join(''.join(r) for r in g)+'\n')
