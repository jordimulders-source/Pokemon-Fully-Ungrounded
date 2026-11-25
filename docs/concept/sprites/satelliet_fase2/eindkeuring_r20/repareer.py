# Eindkeuring r20 -> r21: ALLEEN tinten (paletwaarden + omtinten van bestaande pixels), silhouet-diff 0.
# Draaien vanuit deze map: python3 repareer.py
from PIL import Image
import numpy as np
SRC='../sprite/r20/sprite.png'
im=Image.open(SRC); pal=im.getpalette()[:48]; a=np.array(im)
b=a.copy(); P=list(pal)
Y=lambda c:0.299*c[0]+0.587*c[1]+0.114*c[2]

# Z1 lijf-ladder: F(255) en 2(236) lagen 19 uit elkaar (bijna gelijk), 2->3 31.
#    Gen 3 Glalie wit: 239/208/179/124 (stappen 31/29/55). Nieuw: 255/227/196/166/127 (28/31/30/39), koel (H 245/256).
P[2*3:2*3+3]=[226,225,238]
P[3*3:3*3+3]=[198,191,217]

ch={}
def zet(x,y,oud,nieuw,zone):
    assert b[y,x]==oud,(x,y,b[y,x],oud); b[y,x]=nieuw; ch.setdefault(zone,[]).append((x,y,oud,nieuw))
# Z2 antennebolletjes: licht linksboven (Gen 3); de linkerbovenpixel was 5 (lijflavendel, donkerder dan 6 ernaast).
zet(35,8,5,6,'Z2 antennebol links'); zet(48,10,5,6,'Z2 antennebol rechts')
# Z3 selout lijf/klein paneel: gat in de lijn (paneel A raakte lijf 2 direct op x=20).
zet(20,21,2,5,'Z3 selout linksboven')
# Z4 sikkel rechterrand onderwang: lichtste lijftint lag tegen de zwarte schaduwrand (Glalie: daar altijd 179/124).
for x,y in [(36,28),(36,29),(37,30),(37,31),(36,32)]: zet(x,y,2,3,'Z4 sikkel rechts')
# Z5 klein paneel rechtsonder: lichte framelijnkleur A op de buitenrand tussen zwart -> paneelbasis 9.
zet(12,35,10,9,'Z5 hoek klein paneel')

assert ((a==0)==(b==0)).all(), 'silhouet gewijzigd'
o=Image.fromarray(b,'P'); o.putpalette(P+[0]*(768-48)); o.save('r21/sprite.png',transparency=0)
for z,v in ch.items(): print(z,len(v),v)
print('pixels omgetint:',int((a!=b).sum()),'| paletslots gewijzigd: 2',pal[6:9],'->',P[6:9],' 3',pal[9:12],'->',P[9:12])
print('lijfladder Y:',[round(Y(P[i*3:i*3+3])) for i in (15,2,3,4,5)])
