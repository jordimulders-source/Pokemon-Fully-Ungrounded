# r2 (Jordi 19 nov: "frame 2 moet alleen nog klein beetje scheiding tussen de rechtervleugel en de staart,
# qua belijning/schaduw/kleur. Verder uitstekend"). r1-frame2 + alleen deze zone; buiten de zone diff 0 (assert).
import numpy as np; from PIL import Image
from palet import PAL
a0=np.array(Image.open('../r1/frame2.png')).astype(int); a=a0.copy()
Y,X=np.mgrid[0:64,0:64]
ZONE=(Y>=10)&(Y<=22)&(X>=45)&(X<=52)          # waar de nabije (rechter) vleugel tegen de opkrullende staart ligt
VLEUGEL=[4,11,12,13,14]; STAART=[5,6]   # lichte middenstreng (7) blijft
for y,x in zip(*np.where(ZONE&np.isin(a0,STAART))):
    nb=[a0[y+dy,x+dx] for dy,dx in ((0,-1),(-1,0),(1,0),(-1,-1),(1,-1))]
    if any(v in VLEUGEL for v in nb): a[y,x]=2   # staartrand tegen de vleugel een tint donkerder (schaduw/binnenlijn)
d=a!=a0; assert not (d&~ZONE).any()
print('gewijzigd',int(d.sum()),[(int(x),int(y),int(a0[y,x]),int(a[y,x])) for y,x in zip(*np.where(d))])
im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(sum(PAL,())); im.save('frame2.png',transparency=0)
