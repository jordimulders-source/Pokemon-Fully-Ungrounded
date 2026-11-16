# r2 punt 2: gezicht per pixel uit het model. Meting (mediaan-helderheid / % donker per 12x12-blok, zie rapport):
# donker >= 40% -> lijn (bruin 2, de donkerste modeltint), oogwit = het enige lichte blok in het oog (14,21: 242),
# pupil/iris = het tan blok ernaast (15,21: 172, 25% donker -> tan 3). Overige pixels in het gezichtsvak: cremetint naar de
# modelhelderheid (<205 -> 3, <226 -> 4, anders 5). Rood streepje (11,21) uit het model blijft.
import numpy as np; from PIL import Image
a=np.load('r2_lijn.npy'); m=np.asarray(Image.open('../../referenties/model_v14.png').convert('RGB')).astype(float)@[0.299,0.587,0.114]
LIJN=[(16,19),(15,19),(15,20),(14,20),(13,21),(12,22),(15,23),(16,23),(13,24),(14,24),(9,25),(10,25),(11,25),(11,26)]
VAST={(14,21):5,(15,21):3,(11,21):11}
n=0
for y in range(18,27):
    for x in range(9,18):
        if a[y,x]==0: continue
        if (x,y) in LIJN: v=2
        elif (x,y) in VAST: v=VAST[(x,y)]
        else:
            if a[y,x] not in (2,3,4,5): continue
            L=np.median(m[120+y*12:132+y*12,106+x*12:118+x*12]); v=3 if L<205 else (4 if L<226 else 5)
        if a[y,x]!=v: a[y,x]=v; n+=1
np.save('r2_gezicht.npy',a); print('gezicht r2: gewijzigd',n)
