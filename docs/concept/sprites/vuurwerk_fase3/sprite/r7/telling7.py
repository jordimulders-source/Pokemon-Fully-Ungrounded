# Bewijs r7: diff t.o.v. r5 115% (zelfde oogkleur) alleen binnen de oogzone (afstand < 3,2 px tot het oogmidden (13,22)).
import numpy as np; from PIL import Image
Y,X=np.mgrid[:64,:64]; OZ=np.hypot(X+0.5-13,Y+0.5-22)<3.2
for n,o in (('geel',13),('goud',14)):
    r5=np.asarray(Image.open('../r5/sprite_115_%s.png'%n)).astype(int); s=np.asarray(Image.open('sprite_%s.png'%n)).astype(int); d=s!=r5
    print(n,'| oogzone:',int((d&OZ).sum()),'px gewijzigd (binnenkant',int(((s==o)&OZ).sum()),'px, was',int(((r5==o)&OZ).sum()),'; pupil',int(((s==1)&OZ).sum()),
          '; ooglijn erbij',int(((s==2)&(r5!=2)&OZ).sum()),'; kop-pixels die de binnenkant/pupil nu bedekt',int((((s==o)|(s==1))&~((r5==o))&(r5!=2)&OZ).sum()),
          ') | buiten de oogzone:',int((d&~OZ).sum()),'| kleuren',len(np.unique(s)))
