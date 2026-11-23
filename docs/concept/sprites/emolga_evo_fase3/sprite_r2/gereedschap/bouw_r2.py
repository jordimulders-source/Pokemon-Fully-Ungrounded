# bouw_r2.py: r2 = r1 + drie benoemde reparaties (Claude, 23 nov). Alles als bovenlaag per pixel; buiten de zones diff 0 (controle_r2.py).
#  1 VLEUGEL: alleen tinten D/E -> D/E/G binnen het vleugelpakket (rij 9-37). K-lijnen, geel, wit en silhouet blijven.
#  2 WANG: wangplukje rechts (x33-38, rij 43-48) naar de pieken van het model.
#  3 KAP (alleen A/A_geel): V-kap leesbaar, probeersels P1-P3 (kop_probeersels.png).
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/sprite_r2/gereedschap')
from fv import *; import palet
CH=palet.CH; I={c:i for i,c in enumerate(CH)}
R1=D+'sprite_r1/'; R2=D+'sprite_r2/'
a0=np.asarray(Image.open(R1+'A0.png')).astype(int)
A1=np.asarray(Image.open(R1+'A.png')).astype(int)
Ag1=np.asarray(Image.open(R1+'A_geel.png')).astype(int)

# ---- 1 VLEUGELPAKKET: per rij {x: tint}. Licht linksboven (G = hooglicht op de bolling), E midden, D sikkel langs de rechterrand/onderkant.
VLEUGEL={
 9:{32:'E'},
 10:{32:'E',33:'E'},
 11:{31:'E',32:'E',33:'E',34:'E'},
 12:{31:'E',32:'G',33:'G',34:'E',35:'E'},
 13:{30:'E',31:'G',32:'G',33:'G',34:'E',35:'E'},
 14:{28:'E',29:'E',30:'E',31:'G',32:'G',33:'G',34:'E',35:'E'},
 15:{28:'E',29:'E',30:'G',31:'G',32:'G',33:'E',34:'E',35:'E'},
 16:{24:'G',25:'G',28:'E',29:'E',30:'G',31:'G',32:'E',33:'E',34:'E',35:'E'},
 17:{24:'G',25:'G',26:'G',27:'G',28:'G',30:'E',31:'E',32:'E',33:'E',34:'E',35:'E',36:'E'},
 18:{24:'G',25:'G',26:'G',27:'G',31:'E',32:'E',33:'E',34:'E',35:'E',36:'E'},
 19:{23:'G',33:'E',34:'E',35:'E',36:'E',37:'E'},
 20:{23:'G',24:'G',25:'G',26:'G',27:'G',34:'E',35:'E',36:'E',37:'E'},
 21:{24:'G',25:'G',26:'G',27:'G',35:'E',36:'E',37:'E',38:'E'},
 22:{24:'G',25:'G',26:'G',36:'E',37:'E',38:'E'},
 23:{24:'G',25:'G',37:'E',38:'E'},
 24:{24:'G',37:'E'},
 26:{21:'G'},
 27:{21:'G',22:'G',23:'G'},
 28:{21:'G',22:'G'},
 33:{25:'D'},
}
# ---- 2 WANGPLUKJE (x33-38): pieken uit het model (punten rij 44 en 47, inkepingen rij 43 en 45-46/48 aan x37)
WANG={}
def wang(v):
    W2={}
    if v=='W1':   # twee punten tot x38 (model: punt 1 rij 44, punt 2 rij 46-47), scheidingslijnen N uit het model
        W2={43:{37:'K'},44:{36:'W',37:'W',38:'K'},45:{35:'N',36:'N',37:'K'},46:{36:'W',37:'K'},47:{34:'M',35:'N',36:'W',37:'W',38:'K'},48:{36:'W',37:'K'}}
    if v=='W2':   # punten op rij 44 en 47 tot x38 (model 28 %/47 %), rij 43 x37 dicht als bovenlijn van punt 1
        W2={43:{37:'K'},44:{36:'B',37:'B',38:'K'},46:{36:'W'},47:{36:'W',37:'B',38:'K'}}
    if v=='W3':   # als W2, inkeping rij 43 blijft open (model 14 %); punt 1 loopt uit in w (model: grijze punt)
        W2={44:{36:'B',37:'w',38:'K'},46:{36:'W'},47:{36:'W',37:'B',38:'K'}}
    return W2
# ---- 3 KAP-probeersels (rij 47-51, x21-31), bovenlaag op r1-A (C + oude kap)
def kap(o,v,geel):
    z={}
    if v=='P1':   # punt 25,49 (zoals r1), V op rij 50 x24-27; rechts daarvan weer het witte voorhoofd van het model (x28-30) -> het wit onder
                  # het vizier is een doorlopende band (rij 48 24-26, rij 49 23-24/26-28, rij 50 28-30 zoals A0), geen losse witte stipjes
        z={50:{24:'E',25:'D',26:'D',27:'D',28:'B',29:'B',30:'B'}}   # x28-30 = de A0-pixels (model wit 202-204)
    if v=='P2':   # hogere V: punt 25,48 (wit 24/26 ernaast), rij 49 24-26, rij 50 24-27; witte wiggen links (23,49) en rechts tot x30 (model)
        z={48:{24:'W',25:'D',26:'W'},49:{23:'W',24:'D',25:'D',26:'D',27:'W',28:'B'},50:{23:'D',24:'E',25:'D',26:'D',27:'D',28:'W',29:'B',30:'B'}}
    if v=='P3':   # als P2, maar de kap licht omlijnd linksboven (G/E langs de linkerflank van de V) zodat hij los staat van oor en vizier
        z={48:{24:'W',25:'E',26:'W'},49:{23:'W',24:'G',25:'E',26:'D',27:'W',28:'B'},50:{23:'D',24:'G',25:'E',26:'D',27:'D',28:'W',29:'B',30:'B'},51:{24:'E'}}
    o=o.copy()
    for yy,r in z.items():
        for x,c in r.items(): o[yy,x]=I[c]
    if geel:   # gele voorhoofdvlekje van het model op de kap (zelfde 4 px als r1 A_geel)
        for (x,yy),c in (((25,49),'L'),((25,50),'Y'),((26,50),'Y'),((26,51),'y')): o[yy,x]=I[c]
    return o
def zet(o,zones):
    o=o.copy()
    for yy,r in zones.items():
        for x,c in r.items(): o[yy,x]=I[c]
    return o
def bouw(kapv='P1',wangv='W3'):
    for yy,r in VLEUGEL.items():
        for x,c in r.items(): assert CH[a0[yy,x]] in 'DE',(x,yy,CH[a0[yy,x]])
    n0=zet(zet(a0,VLEUGEL),wang(wangv))
    nA=kap(zet(zet(A1,VLEUGEL),wang(wangv)),kapv,False)
    nAg=kap(zet(zet(Ag1,VLEUGEL),wang(wangv)),kapv,True)
    return n0,nA,nAg
if __name__=='__main__':
    n0,nA,nAg=bouw()
    for o,nm in ((n0,'A0'),(nA,'A'),(nAg,'A_geel')): palet.opslaan(o,R2+nm+'.png')
    print('ok')
