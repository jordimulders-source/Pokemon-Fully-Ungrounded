# Regionale Jynx r4 = r3 + alleen de rokvouw rechts (r3 rij 47, x33-46) op het modelpad (Jordi: "op die horizontale
# streep in de jurk na"). Pad gemeten in het natieve model (gereedschap/natief.png, veerlijn L<95), zie NOTITIES.md.
# Bouwen: cd docs/concept/sprites/jynx_regional && python3 sprite_r4/bouw.py      (variant B zonder lijn: ... bouw.py B)
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from gemeen import *
import gemeen
r3=np.asarray(Image.open('sprite_r3/jynx_regional_r3.png')).astype(int); o=r3.copy()
PAL2=list(PAL); PAL2[15]=(200,154,104); gemeen.PAL[:]=PAL2      # palet r3, ongewijzigd
L_,M_=2,4
def zet(lst,k,moet):
    for X,Y in lst: assert CH[o[Y,X]]==moet,(X,Y,CH[o[Y,X]]); o[Y,X]=k
B=len(sys.argv)>1 and sys.argv[1]=='B'
if not B:
    # Modelpad (natief -> sprite): (57,66)->(61,68) = sprite (37,47)->(38,48)(39,48)->(40,48); (61-63,66) = (40-41,46);
    # (64-67,67) = (42-44,47); (68,66)->(70,68)->(72,69) = (45-46,47)(47,48)(48,49) (al zo in r3).
    # x34-36 op rij 47 heeft geen modellijn (natief u54-56 v65-67 = vlak 145): weg, vlak = rok midden zoals erboven/eronder.
    zet([(34,47),(35,47),(36,47),(38,47),(39,47),(41,47)],M_,'l')
    zet([(38,48),(39,48),(41,46)],L_,'m')
    NAAM='sprite_r4/jynx_regional_r4.png'
else:
    # Variant B: de dwarslijn valt weg tussen de verticale vouwen x33, x40 en x44 (die blijven); vlak = rok midden.
    zet([(34,47),(35,47),(36,47),(37,47),(38,47),(39,47),(41,47),(42,47),(43,47),(45,47),(46,47)],M_,'l')
    NAAM='sprite_r4/jynx_regional_r4_B_zonder_lijn.png'
d=(o!=r3); ys,xs=np.where(d)
assert ((o>0)==(r3>0)).all(), 'silhouet gewijzigd'
assert xs.min()>=33 and xs.max()<=48 and ys.min()>=45 and ys.max()<=49, 'wijziging buiten de rokzone'
opslaan(o,NAAM)
print(NAAM,'| anders dan r3: %d px, allemaal in rokzone x33-48 y45-49 | silhouet-diff %d | buiten zone %d | kleuren %d'%(
      d.sum(),((o>0)!=(r3>0)).sum(),int(d.sum()-d[45:50,33:49].sum()),len(set(o.ravel()))))
toon(o,43,52,30,52)
