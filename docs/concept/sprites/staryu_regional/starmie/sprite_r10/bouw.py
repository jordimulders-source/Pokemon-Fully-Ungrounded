# bouw.py r10: python3 sprite_r10/bouw.py   (vanuit starmie/)
# Jordi omcirkelde twee plekken op r9 ("omcirkeld is nog niet netjes afgewerkt", referenties/jordi_starmie_omcirkeld.png):
#   zone 1 = achterpunt rechtsboven, zone 2 = tip rechter voorarm.
# Alleen tinten binnen het bestaande silhouet; niets getekend buiten deze twee zones, palet ongewijzigd.
# Elke wijziging (x, y, oude index, nieuwe index), oude index ge-assert; silhouet ge-assert (alpha-diff 0);
# alles buiten de zonemaskers ge-assert op diff 0.
# Variant B (sprite_r10/starmie_r10_B.png): de binnenlijn waar de voorste ster over de achterpunt valt in 2 i.p.v. 1.
import numpy as np; from PIL import Image
IN='sprite_r9/starmie_r9.png'; OUT='sprite_r10/starmie_r10.png'; OUTB='sprite_r10/starmie_r10_B.png'
im=Image.open(IN); o0=np.array(im); pal=im.getpalette()

# ---------- ZONE 1: achterpunt rechtsboven ----------
# Doelraster per rij (x: index). 1 = buitenlijn/voorste-sterlijn, 2 = selout, 3 = donker vlak,
# 4/5 = licht vlak (5 = randlicht langs de lijn linksboven), 15 = chip, 7 = glazuurlijn voorste ster, 4 = voorrand.
Z1={
 11:{42:5,43:5,44:4,45:3},
 12:{40:5,41:5,42:5,43:4,44:4,45:3},
 13:{39:5,40:5,41:5,42:4,43:4,44:3,45:3},
 14:{37:1,38:5,39:5,40:4,41:15,42:15,43:4,44:3,45:3},
 15:{37:1,38:4,39:4,40:4,41:4,42:4,43:4,44:3,45:3},
 16:{37:4,38:1,39:4,40:4,41:4,42:4,43:3,44:3,45:3},
 17:{36:4,37:4,38:1,39:4,40:4,41:15,42:4,43:3,44:3},
 18:{36:7,37:4,38:4,39:1,40:4,41:15,42:4,43:3,44:3},
 19:{36:7,37:4,38:4,39:1,40:2,41:2,42:2,43:2,44:2},
 20:{37:7},
}
# ---------- ZONE 2: tip rechter voorarm ----------
Z2={
 22:{47:5,48:5,49:5,50:5,51:5,52:5,53:5,54:5,55:4},
 23:{51:5,52:5,53:4,54:4,55:3},
 24:{52:5,53:4,54:4,55:3},
}
# zonemaskers (rechthoeken; alles erbuiten moet identiek blijven)
M=np.zeros((64,64),bool)
M[10:21,36:47]=True     # zone 1: x36-46, y10-20 (x36 rij 17-19 en (37,20) = voorrand/glazuurlijn in de binnenhoek)
M[20:27,44:58]=True     # zone 2: x44-57, y20-26

def bouw(lijn=1):
    o=o0.copy()
    for Z in (Z1,Z2):
        for y,row in Z.items():
            for x,v in row.items():
                if v==1 and lijn!=1 and Z is Z1 and (x,y) in [(37,14),(37,15),(38,16),(38,17),(39,18)]: v=lijn
                assert M[y,x],(x,y)
                assert o0[y,x]!=0,(x,y,'transparant')
                o[y,x]=v
    assert ((o>0)==(o0>0)).all(),'silhouet veranderd'
    assert (o[~M]==o0[~M]).all(),'diff buiten zones'
    return o
def save(o,p):
    q=Image.fromarray(o.astype('uint8'),'P'); q.putpalette(pal); q.save(p,transparency=0)
A=bouw(1); B=bouw(2)
save(A,OUT); save(B,OUTB)
for n,o in (('A',A),('B',B)):
    d=o!=o0
    print(n,'gewijzigd totaal',d.sum(),'| buiten zones',(d&~M).sum())
    for y,x in zip(*np.where(d)): print('  (%d,%d) %d->%d'%(x,y,o0[y,x],o[y,x]))
