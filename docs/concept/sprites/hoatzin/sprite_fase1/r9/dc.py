# Kuiken r9: Dragonfly Cave-eindkeuring op r8 (Jordi op r8: "nee naar de eindkeuring ermee").
# Alleen DC-fouten die over waren, zo min mogelijk pixels; silhouet gelijk (alpha-diff 0 met r8).
# Vast (niet aangeraakt): haren B, nabije vleugel als één gevouwen vorm, binnenlijnen op hun plek in 13 (lijf) / 12 (poot),
# geen rechte hulplijnen, oog en snavel.
import numpy as np, os
from PIL import Image
HIER=os.path.dirname(os.path.abspath(__file__)); R8=HIER+'/../r8/kuiken_r8.png'
FIX=[  # (x, y, oud, nieuw, soort)
 # 1 dubbele lijn: r7-slagschaduw (13) direct onder/naast de in r8 teruggezette lijn (13) -> r6-tint van het lijf (2)
 (36,36,13,2,'dubbele lijn'),(39,37,13,2,'dubbele lijn'),(31,38,13,2,'dubbele lijn'),(33,38,13,2,'dubbele lijn'),(34,38,13,2,'dubbele lijn'),
 # 2 vleugelrand tegen het lijf zigzagde x42/41/42/41/42 met losse lijfpixels ertussen: lijn x41 doorlopend, lijfstrookje x42 doorlopend
 (41,43,8,13,'zigzaglijn/ruis'),(42,43,13,3,'zigzaglijn/ruis'),
 # 3 buitenlijn schaduwkant: haarwortels werden in r8 als binnenlijn gezien (13); terug naar zwart zoals de rest van die rand
 (42,38,13,1,'buitenlijn haarwortel'),(42,41,13,1,'buitenlijn haarwortel'),
 # 4 bovenrand vleugelpunt: selout 12 en zwart om en om (s s K K s s K) -> selout doorlopend tot de punt
 (46,45,1,12,'om-en-om rand'),(47,46,1,12,'om-en-om rand'),
 # 5 losse ruispixels: los donker stipje (37,46) aan het eind van de veerlijn -> veerlijn taps laten doorlopen (model: vouw);
 #   lichte stip in de donkere band
 (38,45,8,5,'losse pixel'),(44,47,9,5,'losse pixel'),
]
im=Image.open(R8); a=np.array(im); o=a.copy(); tel={}
for x,y,oud,nieuw,k in FIX:
    assert a[y,x]==oud,(x,y,a[y,x]); o[y,x]=nieuw; tel[k]=tel.get(k,0)+1
assert ((o>0)!=(a>0)).sum()==0
uit=Image.fromarray(o,'P'); uit.putpalette(im.getpalette()); uit.save(HIER+'/kuiken_r9.png',transparency=0)
n=(o>0).sum()
print(tel,'totaal',int((o!=a).sum()),'alpha-diff',int(((o>0)!=(a>0)).sum()))
print('zwart % r8',round((a==1).sum()/n*100,1),'r9',round((o==1).sum()/n*100,1),'kleuren',len(set(o.flat)-{0}))
