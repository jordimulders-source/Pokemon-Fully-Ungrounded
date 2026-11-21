# Vlieg r1: kale reductie (reduce2.py -> kaal.txt) + reparaties per zone, steeds naar het model.
# Elke wijziging staat hieronder per zone; tel.py telt per zone de afwijking van kaal.txt.
# Palet (reduce_pal.py): 1 omlijning, 2 vizier/borst, 3-6 grijs (donker->licht), 7-9 kabel (donker, midden, glans),
# A/B vleugel/ring licht en schaduw, C vleugellijn, D paars, E/F koper licht/donker.
import numpy as np
K=np.loadtxt('kaal.txt',dtype=int); o=K.copy(); H,W=o.shape
zone=np.full((H,W),'',object)
def put(x,y,v,z):
    if 0<=x<W and 0<=y<H: o[y,x]=v; zone[y,x]=z
def row(y,x0,s,z):
    for k,c in enumerate(s):
        if c!=' ': put(x0+k,y,int(c,16) if c!='.' else 0,z)

# ---------- VLEUGELS (model: bovenrand in vleugellijn C, achterrand zwart, binnenlijn = voorrand vleugel 2)
row(0,28,'CCCCCC1','vleugel')            # bovenrand vleugel 1 + punt
row(1,23,'CCCCC','vleugel')              # bovenrand loopt door naar links (model rij 1)
put(20,3,0,'vleugel')
for x,y in [(22,2),(21,3),(20,4),(19,4)]: put(x,y,12,'vleugel')
put(18,5,12,'vleugel'); put(17,6,12,'vleugel'); put(16,7,12,'vleugel')  # voorrand (lichtkant)
row(4,28,'CCCCCC','vleugel')             # bovenrand vleugel 2 loopt over vleugel 1 (model rij 4)
row(2,39,'CC.','vleugel')                # punt vleugel 2
put(37,7,1,'vleugel'); put(36,8,1,'vleugel'); put(32,9,11,'vleugel'); put(31,9,11,'vleugel')   # achterrand dicht, schaduw onderin
put(31,10,1,'vleugel'); put(32,10,1,'vleugel'); put(20,9,10,'vleugel')
put(21,8,12,'vleugel')                   # einde binnenlijn
for y in range(0,11):                    # restjes kabelklasse in de vleugel = vleugellijn
    for x in range(15,W):
        if o[y,x] in (8,9) : put(x,y,12,'vleugel')

# ---------- SPRIETEN (model: knik bovenaan, stuk schuin naar linksonder, steel naar de kop; grijs met zwart)
for y in range(2,8):
    for x in range(0,14):
        if y<7 or x<5 or x>12: put(x,y,0,'spriet') if K[y,x] else None
row(3,3,'45','spriet'); row(4,1,'45441','spriet'); row(5,0,'411141','spriet'); row(6,0,'1   141','spriet'); row(7,5,'41','spriet')
row(3,10,'454','spriet'); row(4,9,'4541','spriet'); row(5,8,'41141','spriet'); row(6,8,'1141','spriet'); row(7,9,'141','spriet')

# ---------- KOP: vizier-omlijning links, ^-ogen, rand rechts, kin (model)
for y in range(10,16):
    for x in range(1,14):
        if o[y,x]==13: put(x,y,2,'oog')
for x,y in [(3,11),(2,12),(4,12),(2,13),(4,13),(4,14)]: put(x,y,13,'oog')                  # verre ^
for x,y in [(10,11),(9,12),(11,12),(9,13),(11,13),(9,14),(12,14)]: put(x,y,13,'oog')       # nabije ^
put(10,12,2,'oog')
put(1,12,1,'kop'); put(1,13,1,'kop'); put(2,14,1,'kop'); put(3,14,2,'kop'); put(3,15,1,'kop'); put(2,11,1,'kop')
for y in range(10,15): put(15,y,5,'kop')                                                    # grijze rand naast het vizier
put(15,15,4,'kop')
row(17,4,'1555 44','kop'); row(18,5,'15544111','kop'); row(19,6,'1441','kop'); row(20,7,'11','kop')   # kin
put(11,17,4,'kop'); put(12,17,4,'kop'); put(13,17,1,'kop'); put(13,16,1,'kop')

# ---------- ACHTERLIJF: buitenlijn rechts dicht (model)
put(38,17,1,'lijf')
for y in range(20,25): put(39,y,1,'lijf')

# ---------- POTEN: eerst alles onder de romp en kabel/koperklassen weg, romp dichten, dan poten langs de modelpaden
bodem={}   # laatste romprij per kolom (model)
for x in range(0,W): bodem[x]=-1
for x in range(5,10): bodem[x]=20
for x in range(10,13): bodem[x]=19
for x in range(13,23): bodem[x]=20
for x in range(23,30): bodem[x]=25
for x in range(30,33): bodem[x]=24
for x in range(33,39): bodem[x]=25
bodem[39]=24
for y in range(17,H):
    for x in range(W):
        if zone[y,x]=='kop': continue
        if y>bodem[x]: put(x,y,0,'poot')
        elif o[y,x] in (7,8,9,10,11,14,15): put(x,y,-1,'poot')
# gaten in de romp vullen met de meest voorkomende romptint uit de buren (2-6)
for it in range(4):
    for y in range(H):
        for x in range(W):
            if o[y,x]==-1:
                nb=[o[y+dy,x+dx] for dy,dx in ((0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)) if 0<=y+dy<H and 0<=x+dx<W and 2<=o[y+dy,x+dx]<=6]
                if nb: o[y,x]=max(set(nb),key=nb.count)
o[o==-1]=2
# onderrand romp = omlijning
for x in range(13,W):
    y=bodem[x]
    if y>0 and o[y,x]!=0 and zone[y,x]!='kop': put(x,y,1,'poot')

def kabel(pad,ver=False,z='poot'):
    # pad: lijst (x,y,stijl); stijl 'h' = profiel links-rechts [7][9][1], 'v' = boven-onder [7][9][1]
    glans=8 if ver else 9
    for x,y,s in pad:
        if s=='h': trio=[(x-1,y),(x,y),(x+1,y)]
        else: trio=[(x,y-1),(x,y),(x,y+1)]
        for (a,b),v in zip(trio,(1 if ver else 8,glans,1)):
            if ver and o[b,a]!=0: continue   # verre poot alleen in lege ruimte
            put(a,b,v,z)
def ring(c,y,ver=False,z='poot'):   # ring (model: witte band, breder dan de kabel): [1][A][A][A][1], eronder [1][B][B][B][1]
    for dy,t in ((0,10),(1,11)):
        for dx in range(-2,3):
            a,b=c+dx,y+dy; v=1 if abs(dx)==2 else (11 if ver else t)
            if ver and o[b,a]!=0: continue
            put(a,b,v,z)
def koper(pts,ver=False,z='poot'):
    for x,y,v in pts:
        if ver and o[y,x]!=0: continue
        put(x,y,15 if ver else v,z)

# poot 1 (nabij voor): bovenstuk schuin naar linksonder, ring, onderbeen, koperklauw (model)
P1=[(11,20,'h'),(10,21,'h'),(9,22,'h'),(8,23,'h')]
P1o=[(7,26,'h'),(7,27,'h'),(7,28,'h'),(7,29,'h'),(7,30,'h'),(6,31,'h'),(5,32,'h')]
K1=[(4,33,14),(3,33,14),(2,34,15),(4,34,14),(4,35,15)]
# poot 2 (ver voor, al in het model): recht omlaag, ring, voet naar links
P2=[(13,y,'h') for y in range(20,24)]+[(13,y,'h') for y in range(25,31)]
K2=[(12,31,14),(11,31,14),(10,31,15),(12,32,15)]
# poot 3 (nabij midden)
P3=[(20,y,'h') for y in range(20,26)]
P3o=[(21,y,'h') for y in range(28,34)]+[(22,34,'h'),(23,35,'h')]
K3=[(23,36,14),(24,36,14),(25,37,15),(23,37,14),(22,38,15)]
# poot 4 (nabij achter): vlak onder het achterlijf langs, buigt omlaag, ring, schuin naar rechtsonder
P4=[(23,20,'v'),(24,20,'v'),(25,21,'v'),(26,21,'v'),(27,21,'v'),(28,22,'v'),(29,22,'h'),(29,23,'h'),(30,24,'h')]
P4o=[(31,y,'h') for y in range(27,31)]+[(32,31,'h'),(33,32,'h'),(34,33,'h')]
K4=[(35,34,14),(36,34,14),(37,35,15),(35,35,14),(35,36,15)]

kabel(P2,ver=True); put(12,24,11,'poot'); put(13,24,11,'poot'); put(14,24,1,'poot'); koper(K2)
kabel(P1); ring(7,24); kabel(P1o); koper(K1)
kabel(P3); ring(20,26); kabel(P3o); koper(K3)
kabel(P4); ring(31,25); kabel(P4o); koper(K4)

# ---------- TOEGESTANE AFWIJKING (Jordi, optie A): 2 extra verre poten = kopie van poot 3 en poot 4, (+2,-2) verschoven,
# schaduwtint, alleen in lege ruimte (half verstopt achter de nabije). Bovenlaag, als laatste.
DX,DY=2,-2
sh=lambda P:[(x+DX,y+DY,s) for x,y,s in P]
kabel(sh(P3),ver=True,z='extra'); ring(20+DX,26+DY,ver=True,z='extra'); kabel(sh(P3o),ver=True,z='extra'); koper([(x+DX,y+DY,v) for x,y,v in K3],ver=True,z='extra')
kabel(sh(P4o),ver=True,z='extra'); ring(31+DX,25+DY,ver=True,z='extra'); koper([(x+DX,y+DY,v) for x,y,v in K4],ver=True,z='extra')

# ---------- RUIS (losse pixels na de reductie)
for x,y,v in [(12,7,4),(22,7,12),(23,12,1),(21,18,1),(22,19,1),(29,21,3),(34,23,2)]: put(x,y,v,'ruis')
np.savetxt('vlieg_r1.txt',o,fmt='%2d')
np.save('zone.npy',zone.astype(str))
print('px',(o>0).sum(),'breed',W)
