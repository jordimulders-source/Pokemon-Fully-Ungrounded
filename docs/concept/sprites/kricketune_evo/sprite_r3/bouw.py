# Kricketune-evolutie r3 = r2 + keurderpunten (ruis), alles naar het model; oog niet aangeraakt.
# Bouwen: cd kricketune_evo && python3 sprite_r3/bouw.py
import sys, numpy as np; sys.path.insert(0,'gereedschap'); from gemeen import *
r2=laden('sprite_r2/kricketune_evo_r2.png'); o=r2.copy(); tel={}
N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def buur(Y,X,uit=()):
    nb=[o[Y+dy,X+dx] for dy,dx in N8 if o[Y+dy,X+dx] in (9,10,11) and o[Y+dy,X+dx] not in uit]
    if not nb: nb=[o[Y+dy,X+dx] for dy,dx in N8 if o[Y+dy,X+dx]>0 and o[Y+dy,X+dx] not in uit]   # geen rood ernaast: meest voorkomende buur
    return max(set(nb),key=nb.count)
def zet(n,lst):
    v=o.copy()
    for X,Y,k in lst: o[Y,X]=k
    tel[n]=int((v!=o).sum())
# 1. vest-onderrand: model = één zwarte V-boog (links natief (33,48)->(39,53), rechts (46,49)->(40,53)). In de sprite als
#    aaneengesloten lijn (29,36)(30,37)(31,38)(31,39)(32-34,40) en (37,36)(37,37)(36,38)(35,39); overige donkerrood in y36-37, x25-38
#    -> rode buurtint (het vest).
V=[(29,36),(30,37),(31,38),(31,39),(32,40),(33,40),(34,40),(37,36),(37,37),(36,38),(35,39)]
v=o.copy()
for X,Y in V: o[Y,X]=1
for Y in (36,37):
    for X in range(25,39):
        if (X,Y) not in V and o[Y,X]==7: o[Y,X]=buur(Y,X)
tel['1 vest-onderrand (V-boog)']=int((v!=o).sum())
# 2. pakdonker midden in de buik: (33,46)(34,46) liggen op de modellijn (natief rij 61 K K d d) -> zwart; (36,47) los -> rood
zet('2 pakdonker in de buik',[(33,46,1),(34,46,1),(36,47,buur(47,36))])
# 3. losse tintpixels -> buurtint
zet('3 losse tintpixels',[(X,Y,buur(Y,X,(o[Y,X],))) for X,Y in [(35,40),(39,22),(31,4),(29,42),(32,47),(34,48)]])
# 4. strik: twee witte vleugels met elk één roze plooi (29,24) en (32,24) + roze knoop (30-31,25-26); (31,24) roze -> wit,
#    (31,25) zwart -> roze (model: knoop natief x35-37 rij 34-35 roze)
zet('4 strik',[(31,24,6),(31,25,5)])
# 5. kleding: lichttint 4 als 1-px verticale streep op x35 y26-30 (banding) -> weg (pak midden 3)
zet('5 kleding: streep x35 weg',[(35,y,3) for y in range(26,31) if o[y,35]==4])
# 6. antenne rechts: donkerrode strook (49-52,17) die r1 er als selout bovenop zette -> zwart zoals het model (natief rij 23 K)
zet('6 antenne: strook (49-52,17) zwart als het model',[(x,17,1) for x in range(49,53)])
opslaan(o,'sprite_r3/kricketune_evo_r3.png')
for k,n in tel.items(): print('  %-40s %d'%(k,n))
print('totaal anders dan r2:',int((o!=r2).sum()),'| silhouet-diff:',int(((o>0)!=(r2>0)).sum()))
from PIL import Image
rgb(o,(255,255,255)).resize((512,512),Image.NEAREST).save('sprite_r3/kricketune_evo_r3_8x.png')
