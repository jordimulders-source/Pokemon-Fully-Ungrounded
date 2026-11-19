# Palpaca r1 stap 4 (bovenlaag): per pixel repareren wat de reductie kapotmaakt, steeds naar het model.
# Elke reparatie: (x,y,nieuwe index, zone, reden). assert dat het vak binnen het silhouet ligt.
import numpy as np; from PIL import Image
B=np.load('stapB.npy'); R=B.copy()
rep=[
 # oog (model: zwart ovaal, witte glans boven, onderin grijsbruin) en verre oog op de wangrand
 (8,12,2,'oog','glans boven (model natief 47,31-32)'),(9,12,1,'oog',''),(8,13,1,'oog',''),(9,13,1,'oog',''),
 (8,14,15,'oog','lichtere onderkant van het oog (model 98-128)'),(9,14,1,'oog',''),
 (9,15,3,'oog','losse ooglaagpixel: model is hier wol'),
 (2,12,1,'oog','verre oog op de wangrand (model natief 32-34,30-33)'),
 # neus en mond (model: neusgat natief 32-34,38-39; mondlijn 33-38,42-44)
 (2,15,5,'mond','neusgat'),(3,17,5,'mond','mondlijn'),
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
