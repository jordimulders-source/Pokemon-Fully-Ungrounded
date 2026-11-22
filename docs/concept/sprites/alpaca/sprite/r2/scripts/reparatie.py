# Palpaca r1 stap 4 (bovenlaag): per pixel repareren wat de reductie kapotmaakt, steeds naar het model.
# Elke reparatie: (x,y,nieuwe index, zone, reden). assert dat het vak binnen het silhouet ligt.
import numpy as np; from PIL import Image
B=np.load('stapB.npy'); R=B.copy()
rep=[
 # r2 oog: model natief x 46-50, y 30-37 = 2,1 x 3,4 spritepx -> 2x4 (rij 12-15), glans linksboven (natief 47,30-33),
 # lichtere onderkant (natief 47-49,36) in 6, onderrand dicht; verre oog op de wangrand (natief 32-34,30-33)
 (8,12,2,'oog','glans'),(9,12,1,'oog',''),(8,13,1,'oog',''),(9,13,1,'oog',''),
 (8,14,6,'oog','lichtere onderkant'),(9,14,6,'oog',''),(8,15,1,'oog','onderrand'),(9,15,1,'oog',''),
 (2,12,1,'oog','verre oog'),
 # r2 kuif/pony: krullijn van het model (natief 32-36,28 -> 38-42,30 -> 43-46,29-26 -> 47-49,28 -> 50-51,25-28) als twee boogjes;
 # boogje boven het oog in 4 zodat het oog vrij blijft
(3,11,5,'kuif','boog 1'),(4,11,5,'kuif',''),(5,12,5,'kuif',''),(6,12,5,'kuif',''),
 (7,12,3,'kuif',''),
 # r2 kopschaduw (Jordi: hoekige kop oplossen met kleur en schaduw): schaduw onder de kuif volgt de boogjes (1 px boven de krullijn)
 # i.p.v. een rechte band, en een sikkel langs de rechterrand die van 1 px (boven) naar 2 px (onder) groeit
 (5,10,3,'kopschaduw','band -> boogje'),(6,10,3,'kopschaduw',''),(5,11,4,'kopschaduw',''),(6,11,4,'kopschaduw',''),
 (12,16,4,'kopschaduw','sikkel wordt onderaan breder (model 190-193) en neemt de wanglijn op'),(12,17,4,'kopschaduw',''),(11,18,4,'kopschaduw',''),
 (14,10,4,'kopschaduw','sikkel rechts'),(14,11,4,'kopschaduw',''),(15,12,4,'kopschaduw',''),(15,13,4,'kopschaduw',''),
 (7,11,5,'kuif','boog 1 loopt op'),(8,10,5,'kuif',''),(8,11,4,'kuif','boog 2 (licht, boven het oog)'),(9,11,4,'kuif',''),(9,10,3,'kuif',''),
 (10,10,5,'kuif','boog 2 rechts'),(10,11,5,'kuif',''),
 # r2 wanglijn rechts van het oog (natief 52-55, 29-44, doorlopend): zachte lijn in 4 die het gezicht rond maakt
 (11,11,4,'wang',''),(11,12,4,'wang',''),(11,13,4,'wang',''),(11,14,4,'wang',''),(11,15,4,'wang',''),(11,16,4,'wang',''),(10,17,4,'wang',''),(10,18,4,'wang',''),
 (10,12,3,'wang','wol tussen oog en wanglijn'),(10,13,3,'wang',''),(10,14,3,'wang',''),
 # neus en mond (model: neusgat natief 32-35,38-40; mond 33-35,42-43 -> kin 37-38,44 -> opkrul 39,43)
 (2,15,5,'mond','neusgat'),(2,17,5,'mond','mondlijn'),(3,17,5,'mond',''),(5,17,5,'mond','opkrul'),(4,17,3,'mond',''),
 # roze oorbinnenkant linkeroor (model: roze binnenoor natief 32-34, 6-14; reductie gaf wol-schaduw)
 (3,2,14,'oor',''),(3,3,14,'oor',''),
 # kraag (model l->r: teal, roze, teal, geel, teal, roze)
 (7,23,13,'kraag',''),(8,23,14,'kraag',''),(9,23,13,'kraag',''),(10,23,12,'kraag',''),(11,23,13,'kraag',''),
 (11,22,14,'kraag','roze eind loopt omhoog'),(12,22,14,'kraag',''),(10,22,3,'kraag','wol boven de kraag'),
 # manchet geheven handschoen (model: roze band, onderste rij teal/geel om en om)
 (2,37,14,'manchet',''),(3,37,14,'manchet',''),(4,37,14,'manchet',''),(5,37,13,'manchet','teal blok rechtsboven'),
 (2,38,13,'manchet',''),(3,38,12,'manchet',''),(4,38,13,'manchet',''),(5,38,12,'manchet',''),
 # manchet staande handschoen (model: roze band, onderste rij geel/teal/geel)
 (12,42,12,'manchet',''),(13,42,13,'manchet',''),(14,42,12,'manchet',''),

 # licht (Gen 3): glansband op de rug liep als rechthoek evenwijdig aan de rugrand (banding); uiteinden afgeschuind
 (17,25,3,'licht',''),(17,26,3,'licht',''),(18,26,3,'licht',''),(22,26,3,'licht',''),
]
for x,y,v,z,why in rep:
    assert B[y,x]>0, (x,y); R[y,x]=v
np.save('stapR.npy',R)
pal=[tuple(map(int,l.split())) for l in open('../normal.pal').read().split('\n')[3:19]]
oy,ox=np.load('plaats.npy'); H,W=R.shape
S=np.zeros((64,64),int); S[oy:oy+H,ox:ox+W]=R
im=Image.fromarray(S.astype('uint8'),'P'); im.putpalette(sum(pal,())); im.save('../palpaca.png',transparency=0)
from collections import Counter
print('reparaties per zone:',dict(Counter(z for x,y,v,z,_ in rep if B[y,x]!=v)))
