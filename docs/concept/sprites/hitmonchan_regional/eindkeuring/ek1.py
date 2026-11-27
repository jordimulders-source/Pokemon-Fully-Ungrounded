import numpy as np
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmonchan_regional/'
src=Image.open(D+'sprite/kandidaat.png'); K=np.array(src); pal=src.getpalette()[:24]
T=K.copy(); log=[]
W=[ # (x,y,oud,nieuw,reden)
 (16,14,1,2,'arm links: selout op lichte kant (model 127), haalt om-en-om 1/2/1 weg'),
 (16,15,1,2,'arm links: selout (model 140)'),
 (17,13,1,2,'naad kubus-onderarm: binnenlijn in eigen donkerste tint (model 84)'),
 (18,13,1,2,'idem (model 83)'),
 (19,13,1,2,'idem (model 69)'),
 (20,13,1,2,'idem (model 54)'),
 (21,13,1,2,'idem (model 61)'),
 (22,24,1,2,'losse navy-streep arm/schouder -> binnenlijn eigen tint (model 108)'),
 (22,25,1,2,'idem (model G=2)'),
 (29,11,3,4,'kuif linkerrand: 4/3/4 om-en-om -> 4'),
 (50,30,4,1,'kubus rechts: lichte pixel in de schaduwbuitenlijn, gat in de lijn'),
 (24,45,1,2,'zoom tuniek over dij: binnenlijn eigen tint (model 131)'),
 (25,46,1,2,'idem (model 103)'),
 (43,44,4,2,'verre dij rechtsboven: open lichte rand -> lijn (model heeft hier geen lijn; Gen 3-eis)'),
 (44,45,4,2,'idem'),
 (45,46,4,1,'idem, schaduwkant'),
 (45,47,4,1,'idem, schaduwkant'),
 (19,48,4,3,'nabij been links: selout 3/4/3 om-en-om -> 3'),
 (17,51,4,3,'idem'),
 (15,55,3,2,'scheen links: selout 2/3/2 -> 2'),
 (22,51,3,1,'scheen rechts: lichte pixel in navy schaduwlijn (model 76)'),
 (38,49,3,2,'verre knie binnenkant: 2/3/1 -> 2/2/1'),
 (44,55,4,3,'verre voet bovenrand: 4/2/4 om-en-om -> 3 (model 117)'),
 (45,55,2,3,'idem (model 121)'),
 (46,56,4,3,'idem (model 140)'),
]
for x,y,o,n,r in W:
    assert T[y,x]==o,(x,y,T[y,x],o)
    T[y,x]=n; log.append(f'({x},{y}) {o}->{n}  {r}')
assert ((T>0)==(K>0)).all()
im=Image.fromarray(T.astype('uint8'),'P'); im.putpalette(pal+[0]*(768-24))
O=D+'eindkeuring/'; import os; os.makedirs(O,exist_ok=True)
im.save(O+'ek1.png',transparency=0); im.save('ek1.png',transparency=0)
np.save('T.npy',T)
open('log.txt','w').write('\n'.join(log)+'\n'); print(len(log),'pixels; silhouet gelijk')
