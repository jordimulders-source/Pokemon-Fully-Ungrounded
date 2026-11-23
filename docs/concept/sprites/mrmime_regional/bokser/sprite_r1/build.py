# Bokser-Mr. Mime r1: kale reductie (basis.npy uit reductie.py) + benoemde reparaties per zone + Jordi's toegestane bovenlagen.
# Elke wijziging staat hieronder per zone; diff.py telt per zone de pixels die afwijken van de kale reductie.
import numpy as np, json, os
from PIL import Image
from palet import PAL
b=np.load('basis.npy').copy(); H,W=b.shape
zones={}            # zone -> set van (y,x) die deze build aanraakt
def put(zone,y,x,v):
    zones.setdefault(zone,set()).add((y,x)); b[y,x]=v
def rows(zone,y0,x0,lines):
    """lines: strings; '.' = laten staan, 0-8 = index, ' ' wordt genegeerd"""
    for dy,s in enumerate(lines):
        s=s.replace(' ','')
        for dx,c in enumerate(s):
            if c!='.': put(zone,y0+dy,x0+dx,int(c))

# ---------- 1. HAAR: regel (geen tekenwerk): rand naar transparant/gezicht = 1, binnen zwart/donker = 2, strepen 4/5 blijven
hair=np.zeros_like(b,bool)
for y in range(0,17):
    for x in range(20,W):
        if b[y,x] in (1,3,4,5) and not (y>=12 and x<=32): hair[y,x]=1
for y in range(0,9):            # bovenkant kop tot rij 8: alles wat niet huid is
    for x in range(20,W):
        if b[y,x] in (1,3,4,5): hair[y,x]=1
hb=b.copy()
for y,x in zip(*np.where(hair)):
    nb=[hb[yy,xx] if 0<=yy<H and 0<=xx<W else 0 for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))]
    edge=any(v in (0,7,8) for v in nb)
    if edge: put('haar',y,x,1)
    elif hb[y,x] in (1,3): put('haar',y,x,2)
    elif hb[y,x]==5: put('haar',y,x,4)

# ---------- 2. GEZICHT: ogen + mond 1-op-1 uit Gen 3 Mr. Mime (omgekleurd: a/f->8, 1/b->7, 3->3, e->1, c->3), op de modelplek
# linkerrand kop (model: donkere rand kol 20 r10-11, 21 r9)
put('gezicht',9,21,1); put('gezicht',10,20,1); put('gezicht',11,20,1); put('gezicht',12,20,1)
rows('gezicht',9,21,[
 "8 8 7 8 8 8 7 7 8",    # r9  : kol21..29  (ogen r9-12: nabij kol22-24, ver kol26-28)
 "8 3 8 7 8 3 8 7 8",    # r10
 "8 1 8 7 8 1 8 7 8",    # r11
 "8 8 7 7 8 8 7 7 8",    # r12
 "8 8 8 8 8 8 8 8",      # r13 : snor uit rij 13 weg (snor = 1 rij, rij 14)
])
rows('gezicht',14,21,["8 1 1 1 1 8 8"])           # snor: modelrij 14, kol 22-25 (heel klein, 1 rij)
rows('gezicht',15,22,["8 3 8 8 8 3"])             # mond Mr. Mime: (25,26)->(23,15), (29,26)->(27,15)
rows('gezicht',16,23,["7 7 3 3 7"])               # (26,27)b->(24,16)=7, (27,27),(28,27)->(25,16),(26,16)
rows('gezicht',17,25,["1 1 1 1"])                 # kinlijn doorgetrokken (model rij 17 donker over kol 22-31)
# wang: model grijze cirkel kol 28-31 r13-15 -> lichter grijs 6
for y,x in [(13,30),(13,31),(14,30),(14,31),(15,28),(15,29),(15,30),(15,31),(14,28)]:
    put('gezicht',y,x,6)

# ---------- 3. NABIJE VUIST (getapete vingers als banden; vorm = silhouet model)
rows('vuist_nabij',9,0,[
 ". . 1 1 1 1 1",
 ". 1 8 8 7 4 8 1",          # vingers links gestapeld, knokkellijn kol 5 (model: zwarte lijn), handrug rechts
 "1 4 4 4 6 4 7 1",
 "1 8 8 7 7 4 7 6 1",
 "1 4 4 4 6 4 6 6 1",
 "1 1 7 7 4 4 4 6 6 1",      # duim (tape) dwars onderlangs
 ". . 1 4 7 8 7 6 6 1",
 ". . . . 1 1 1 1 1 8",
])

# ---------- 4. VERRE VUIST voor de borst (getapete vingers, zelfde opbouw)
rows('vuist_ver',19,28,[
 ". . . 1 1 1",
 "1 8 8 7 4 8 1",
 "1 4 4 6 4 7 1",
])
rows('vuist_ver',22,27,[
 "1 8 8 7 7 4 7 1",
 "1 4 4 4 6 4 6 1",
 ". 1 7 7 4 4 4 6 1",
 ". . 1 4 7 8 7 6 1",
 ". . . 1 1 1 1 1 1",
])

# ---------- 5. V-PATROON (donkergrijs) bovenin de romp, binnen het silhouet; spierlijntjes weg
rows('v_patroon',18,21,[
 "8 8 8 8 8 7 7 7",     # r18 huid onder de kinlijn
 "8 3 3 3 3 3 3 3",     # r19 kol21-28 (loopt achter de vuist door)
 "8 8 3 3 3 3 3",       # r20
 "8 8 8 3 3 3 3",       # r21
 "8 8 8 8 3 3",         # r22
 "8 8 8 8 3 8",         # r23 punt
 "7 8 8 8 8 8 8",       # r24 borst: spierschaduw weg
 "7 7 8 8 8 8 7 8",     # r25
])
put('v_patroon',19,29,3); put('v_patroon',19,30,3)

# ---------- 6. RONDE SCHOUDERS: vorm 1-op-1 uit Gen 3 Mr. Mime (rechterschouderbal, linkerschouder-sikkel), grijs
MAP={'5':7,'a':8,'6':5,'7':4,'8':2,'e':1,'2':1,'4':1}
bal=["...88887..",
     ".78666667.",
     "886a566667",
     "8665566668",
     "8666666668",
     "8766667768",
     "8777778878",
     ".87778....",
     "..88......"]
BY,BX=map(int,os.environ.get('VPOS','14,30').split(','))
voor=set()   # kop en verre vuist liggen ervoor
for y in range(H):
    for x in range(W):
        if (y<=16 and x<=33) or (y==17 and x<=31) or ('vuist_ver' in zones and (y,x) in zones['vuist_ver'] and b[y,x]!=0): voor.add((y,x))
for dy,s in enumerate(bal):
    for dx,c in enumerate(s):
        y,x=BY+dy,BX+dx
        if c=='.' or (y,x) in voor: continue
        put('schouders',y,x,MAP[c])
# nabije schouder: sikkel (MM kol 17-21, r29-34) waar de gestrekte arm de romp in gaat
sik=["..8...",
     "..8664",
     "..8664",
     ".8664.",
     ".8664.",
     "..ee4."]
import os
NAB=os.environ.get('NABIJ','bal')
if NAB=='sikkel':
    for dy,s in enumerate(sik):
        for dx,c in enumerate(s):
            if c!='.': put('schouders',16+dy,17+dx,MAP[c])
else:
    NY,NX=map(int,os.environ.get('NPOS','11,14').split(','))
    for dy,s in enumerate(bal):
        for dx,c in enumerate(s):
            y,x=NY+dy,NX+dx
            if c=='.' or (y<=14 and x>=20) or (y==15 and x>=21) or (y==16 and x>=22) or (y==17 and x>=23) or (x<=9 and y<=16): continue
            put('schouders',y,x,MAP[c])

# ---------- 7. KNIEEN: grijze blobjes weg -> huid van het been
rows('knieen',46,23,[". 8 7 1"])
rows('knieen',47,23,["5 8 7 1"])
rows('knieen',48,23,["5 8 7 1"])
rows('knieen',47,30,["1 8 7 1"])
rows('knieen',48,30,["1 8 7 1"])
rows('knieen',49,30,["5 8 7 1"])

put('gezicht',9,21,1)
put('gezicht',6,24,1)   # haarlijn: witte stip tussen twee zwarte (model rij 6 kol 23-25 donker/grijs)
# ---------- 8. OPSCHONEN na de reductie (alleen kapotte pixels, steeds naar het model)
# nabije arm: losse grijze pixels uit de reductie weg, rompomtrek links zwart zoals het model
put('arm_nabij',19,12,8); put('arm_nabij',20,19,7)
for y in (21,22,23): put('romp',y,20,1)
# verre arm: bovenarm onder de schouderbal, plooi naar de onderarm, elleboog dicht
rows('arm_ver',21,35,["2 8 8 7 1"])
rows('arm_ver',22,34,["1 7 8 8 8 7 1"])
rows('arm_ver',23,34,["1 1 6 8 8 7 1"])
rows('arm_ver',24,35,["1 1 6 7 7 7 1"])
rows('arm_ver',25,35,["1 7 8 8 6 7 1"])
rows('arm_ver',26,35,["1 7 8 8 8 8 7 1"])
# broek: middennaad 1 px zwart, kleine plooien in donkere broektint, schaduw rechts/onder
rows('broek',35,32,["2"])
rows('broek',36,32,["2 2"])
rows('broek',37,33,["2"])
rows('broek',38,24,["2 2 1"])
rows('broek',38,33,["2"])
rows('broek',39,26,["3"]); rows('broek',39,33,["3 2"])
rows('broek',40,27,["3"]); rows('broek',40,33,["3 2"])
rows('broek',41,22,["2 2 2 2 2"]); rows('broek',41,29,["2 2 2 2"])
# benen: selout links aan de dij (model grijs), knie dicht, scheen links zwart (model)
put('benen',44,22,4); put('benen',46,23,4); put('benen',47,23,4); put('benen',48,23,4)
rows('benen',49,24,["1 4 8 7 1"])
rows('benen',50,25,["1 8 7 1 . 1"])
rows('benen',51,26,["8 8 7"])
for y in (43,44,45): put('benen',y,29,1)
put('benen',46,30,1); put('benen',49,30,1); put('benen',52,30,7)
rows('benen',55,27,["1 7 1 1 7 8 1"])
# schoenen: neus dicht (model donker), schaduw onder/rechts
put('schoenen',59,22,1); put('schoenen',59,23,3); put('schoenen',60,21,1); put('schoenen',60,22,5)
rows('schoenen',60,26,["2 2"]); rows('schoenen',61,34,["2 2"]); rows('schoenen',59,33,["2"])

# randcontrole: lichte pixels op de buitenrand -> omlijning
put('arm_ver',27,37,1)
put('schoenen',58,24,1); put('schoenen',58,25,1); put('schoenen',59,23,1)
np.save('r1.npy',b)
json.dump({k:sorted([int(a),int(c)] for a,c in v) for k,v in zones.items()},open('zones.json','w'))
# naar 64x64: x-offset 10, y 0
full=np.zeros((64,64),'uint8'); full[0:H,10:10+W]=b
p=Image.fromarray(full,'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal)))
p.save('bokser.png',transparency=0)
print('kleuren',len(set(full.ravel())),'incl. transparant')
