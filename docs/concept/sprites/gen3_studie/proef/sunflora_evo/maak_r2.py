# Ronde 2: stralen. Gerichte pixellijsten op na.png (r1). Schijf, gezicht, silhouet, blad/steel/voeten bevroren.
from PIL import Image
import math
R1='na.png'
im=Image.open(R1); px=im.load()
Z={}  # zone -> lijst (x,y,kleur)
Z['A navy-facet: schaduwrand 8 doorgetrokken']=[(34,10,8),(35,10,8),(35,11,8),(36,11,8),(36,15,8),(35,16,8),(35,17,8),(34,18,8)]
Z['B oranje vlam linksboven: licht links (4/3), schaduw rechts (5)']=[(22,6,4),(21,7,4),(21,8,4),(20,9,4),(21,9,3),(20,10,4),(21,10,3),
   (22,7,3),(22,8,3),(23,8,5),(23,9,5),(23,10,5),(23,11,5),(23,12,5)]
Z['C/C2 gele stralen linksboven: schaduwstrook rechts']=[(14,10,5),(15,11,5),(15,12,5),(18,14,5),(18,15,5)]
Z['D navy linksboven: licht 7 aan de rand, grond 8, onderrand 9']=[(19,12,7),(20,12,8),(18,13,7),(19,13,8),(20,13,8),(19,14,7),
   (20,15,8),(21,15,8),(19,16,8),(20,16,8),(21,16,8),(20,18,8),(21,18,8),(22,18,9),(23,18,9),(24,18,9)]
Z['F0 straal links boven E: vlek weg, puntjes lichtrand 4']=[(17,20,3),(10,18,4),(13,18,4)]
Z['E grote straal links: punt 4, schaduwstrook 5 onderlangs het geel']=[(4,27,4),(3,28,4),(5,28,5),(6,28,5),(7,28,5),(8,28,5),(9,28,5),
   (10,27,5),(14,28,5),(15,29,5)]
Z['F1 oranje straal linksonder: licht boven (4/3), schaduw onder (5)']=[(9,34,4),(8,35,4),(9,35,5),(11,33,3),(12,33,3),(13,33,3),(10,34,3),(11,34,3),(12,34,3)]
Z['F2 oranje straal linksonder: lichtkant links 4/3']=[(13,38,3),(13,39,3),(12,40,3),(12,41,3),(11,42,3),(10,43,4),(11,43,3),(10,44,4),(11,44,3)]
Z['G vlammetje in navy linksonder: zalm weg, licht links']=[(18,35,3),(18,36,3),(17,37,3),(17,38,3),(20,37,5),(18,38,5),(16,39,8),(17,39,5)]
Z['H straal onder: licht links bovenaan, vlam ernaast lichtrand']=[(24,40,3),(21,42,3),(21,43,3)]
Z['N oranje straal boven: licht links (4/3), schaduw rechts (5)']=[(42,7,4),(43,7,4),(41,8,4),(42,8,3),(43,8,5),(40,9,4),(41,9,3),(42,9,3),(43,9,5),
   (40,10,3),(41,10,3),(39,11,3),(40,11,3),(38,12,3),(39,12,3),(38,13,3),(39,13,3)]
Z['M gele straal rechtsboven: gemengde lichtrand -> 4, vlekken weg']=[(46,11,4),(50,9,4),(39,15,3),(44,17,8),(44,18,8),(38,21,5)]
Z['L oranje straal rechts: licht boven (4/3), schaduw onder (5)']=[(52,19,4),(50,20,4),(51,20,4),(52,20,3),(47,21,3),(48,21,3),(49,21,3),(50,21,3),(51,21,3),(52,21,5)]
Z['K navy straal rechts: bovenfacet 7, onderfacet 8']=[(48,25,7),(49,25,7),(48,26,7),(49,26,7),(50,26,7),(51,26,7),(52,26,7),
   (48,27,7),(54,27,7),(55,27,7),(55,28,7),(56,28,7),(51,29,8),(40,30,5)]
Z['J oranje straal rechtsonder: licht boven (3)']=[(45,35,3),(46,35,3),(47,35,3),(48,35,3)]
Z['vlammen onder: lichtrand links-boven']=[(34,44,3),(35,44,3),(34,45,3),(44,44,3),(44,45,3)]
FROZEN_COL=(0,1,11,12,13,14)
def disk(x,y): return math.hypot(x-28.3,y-28.8)<=11.6
out=im.copy(); op=out.load(); log={}
for z,L in Z.items():
    n=0
    for x,y,c in L:
        assert px[x,y] not in FROZEN_COL, (z,x,y,px[x,y])
        assert not disk(x,y), (z,x,y,'schijf')
        if px[x,y]!=c: op[x,y]=c; n+=1
        else: print('al gelijk',z,x,y)
    log[z]=n
out.save('na_r2.png')
a=Image.open(R1).load(); b=Image.open('na_r2.png').load()
o=Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/sunflora_evo/af/sunflora_evo.png').load()
print('silhouet diff t.o.v. origineel', sum((o[x,y]==0)!=(b[x,y]==0) for x in range(64) for y in range(64)))
print('schijf+gezicht diff t.o.v. r1', sum(a[x,y]!=b[x,y] for x in range(64) for y in range(64) if disk(x,y)))
print('blad/steel/voeten/zwart diff', sum(a[x,y]!=b[x,y] for x in range(64) for y in range(64) if a[x,y] in FROZEN_COL or b[x,y] in FROZEN_COL))
for z,n in log.items(): print(n,z)
print('totaal',sum(log.values()), 'kleuren', len({b[x,y] for x in range(64) for y in range(64)}-{0}))
