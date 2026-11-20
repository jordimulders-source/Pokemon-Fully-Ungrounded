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

for x,y,v in [(12,7,4),(22,7,12),(23,12,1),(21,18,1),(22,19,1),(29,21,3),(34,23,2)]: put(x,y,v,'ruis')
np.savetxt('romp.txt',o,fmt='%2d')

# =====================  RONDE 2: POTEN ALS GEBOGEN KABELS LANGS HET GEMETEN MODELPAD  =====================
# Middenpaden gemeten op de natieve kaart (idx = natieve x-15, rij = natieve y); omrekenen naar spritecoordinaten.
sx=lambda i:(i-1.5)/1.6; sy=lambda r:(r+0.5-20)/1.6
POTEN={  # naam: (pad, ring (idx,rij_boven,rij_onder), voet-prongs [(idx,rij),...] als twee lijnen, ver?)
 'p1':([(21,52),(18,54.5),(15.5,56),(14.5,58),(14,60),(13,62),(13,69),(12,70.5),(11.5,72)],(14,59,61),
       [[(10.5,72.5),(8.5,72.5),(6.5,73.5)],[(10.5,73),(10,74.5),(9,75.5)]],False),
 'p2':([(22.5,51),(25,53),(24,55),(22.5,57),(22.5,60),(22.5,62),(23,64),(23,67),(22.5,68.5)],(22.5,58,61),
       [[(21,69),(19,69.5),(18,70)],[(21.5,70),(21,71.5)]],True),
 'p3':([(30.5,49),(31.5,51),(33,54),(34,56),(34.5,58),(35,60),(35,62),(36,64),(35.5,66),(35.5,73),(36,74),(37,76)],(35,61,63),
       [[(38,77),(40.5,77.5),(42,78.5)],[(38,78),(38.5,79.5),(39,80.5)]],False),
 'p4':([(35.5,48.5),(37,50.5),(40,52),(43,52.5),(46,53.5),(48,54.5),(49.5,56),(50.5,58),(51.5,60.5),(51.5,63),(51.5,65),(52.5,67),(53.5,69),(55,71),(56,73),(57,74)],(51.5,59,62),
       [[(58.5,74.5),(61,75),(63,75.5)],[(58.5,75.5),(59.5,77),(60,78.5)]],False),
}
def punten(pad,stap=0.05):
    P=[]
    for (a,b),(c,d) in zip(pad,pad[1:]):
        n=max(2,int(np.hypot(c-a,d-b)/stap))
        for t in np.linspace(0,1,n,endpoint=False): P.append((sx(a+(c-a)*t),sy(b+(d-b)*t),c-a,d-b))
    a,b=pad[-1]; P.append((sx(a),sy(b),0,1)); return P
def band(pad):
    # 2 px brede kabel langs het modelpad: steil (per spriterij gemiddelde x) -> [glans][kabel] links-rechts;
    # vlak (|dx|>2,5|dy|, alleen poot 4 onder het achterlijf) -> per kolom gemiddelde y -> [glans] boven [kabel]
    rij={}; kol={}
    for x,y,dx,dy in punten(pad):
        if abs(dx)>2.5*abs(dy): kol.setdefault(int(np.floor(x)),[]).append(y)
        else: rij.setdefault(int(np.floor(y)),[]).append(x)
    cel={}
    for i,ys in kol.items():
        j=int(np.floor(np.mean(ys)-0.5)); cel[(i,j)]='g'; cel[(i,j+1)]='k'
    for j,xs in rij.items():
        i=int(np.floor(np.mean(xs)-0.5))
        if (i,j) not in cel: cel[(i,j)]='g'
        if (i+1,j) not in cel: cel[(i+1,j)]='k'
    return cel
leg_px={}
E,F=14,15
VOET={'p1':[(5,33,E),(4,33,E),(3,33,F),(5,34,E),(4,35,F)],        # model: prong naar links + prong omlaag
      'p2':[(12,30,E),(11,31,F),(10,31,F),(12,31,F),(12,32,F)],
      'p3':[(22,36,E),(23,36,E),(24,37,F),(22,37,E),(22,38,F)],   # model: prong naar rechtsonder + prong omlaag
      'p4':[(35,35,E),(36,35,E),(37,36,F),(35,36,E),(36,37,F)]}
def teken(naam,dx=0,dy=0,extra=False):
    pad,rg,voet,ver=POTEN[naam]; ver=ver or extra; z='extra' if extra else 'poot'
    G,Kc=(7,1) if ver else (8,7)
    def zet(i,j,v):
        i+=dx; j+=dy
        if not(0<=i<W and 0<=j<H): return
        if extra and o[j,i]!=0: return            # verre extra poot: alleen in lege ruimte (achter romp en nabije poten)
        if zone[j,i] not in ('poot','extra') and o[j,i]!=0 and naam=='p2': return   # model-verre poot achter de romp
        put(i,j,v,z)
    cel=band(pad)
    r0,r1=int(np.floor(sy(rg[1]))),int(np.floor(sy(rg[2])))   # ringrijen
    for (i,j),t in cel.items():
        if r0<=j<=r0+1: continue
        zet(i,j,G if t=='g' else Kc)
    # ring: dikke witte band, 1 breder dan de kabel aan de lichtkant, zwart aan de schaduwkant; twee rijen (wit, schaduw)
    for k,j in enumerate((r0,r0+1)):
        xs=sorted(i for (i,jj) in cel if jj==j)
        if not xs: xs=sorted(i for (i,jj) in cel if jj in (j-1,j+1))[:2]
        L,R=xs[0],xs[-1]
        for i in range(L-1,R+1): zet(i,j,11 if (ver or k==1) else 10)
        zet(R+1,j,1)
    # koperklauwtjes: wortel onder het kabeleinde + twee prongs van 2 px in de richting van de modelprongs, punt donker
    for i,j,v in VOET[naam]: zet(i,j,15 if extra else v)
for n in ('p2','p1','p3','p4'): teken(n)
# toegestane afwijking (optie A): kopie van p3 en p4 langs hun nieuwe pad, (+2,-2), schaduwtint, alleen in lege ruimte
teken('p3',3,-2,True); teken('p4',2,-2,True)
# ---------- KOP ronder (Jordi 20 nov: "linkerkant hoofd en oog mag wat ronder"; ronding uit het model: linkerrand rij 12-14 op kol. 1, rij 15 op kol. 2)
put(1,14,1,'kop2'); put(2,14,2,'kop2'); put(2,15,1,'kop2'); put(3,15,2,'kop2')
# grijze rand achter de kop (model: boog van rij 9 tot de kin) + zwarte lijn die kop en borststuk scheidt
put(15,9,1,'kop2')
for y in range(10,16): put(16,y,1,'kop2')
put(15,16,1,'kop2'); put(13,16,4,'kop2')
put(14,15,4,'kop2'); put(15,15,1,'kop2')   # model: rand loopt via (14,15),(13,16) naar de kin
# kop rond bovenaan (model: rechterkoepel ook op rij 9 grijs, vizierlijn op rij 10; koepelrand donkergrijs) en kinkerf zwart (model rij 17)
for x in range(10,14): put(x,9,5,'kop2'); put(x,10,1,'kop2')
put(8,7,4,'kop2'); put(13,7,4,'kop2'); put(9,17,1,'kop2'); put(10,17,1,'kop2')
# ---------- BORSTSTUK: een subtiel hooglicht linksboven (Gen 3-volume), op de donkergrijze modelplek
put(17,9,4,'borst'); put(18,9,4,'borst')
np.savetxt('vlieg_r2.txt',o,fmt='%2d'); np.save('zone.npy',zone.astype(str)); print('px',(o>0).sum())
