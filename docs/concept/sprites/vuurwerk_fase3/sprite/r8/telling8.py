# Bewijs r8: diff t.o.v. r5 115% geel alleen in het oogvak (x7-14, y21-23) en de vlamtong (x14-16, y2-3); rest 0.
import numpy as np; from PIL import Image
r5=np.asarray(Image.open('../r5/sprite_115_geel.png')).astype(int); Y,X=np.mgrid[:64,:64]
OOG=(X>=7)&(X<=14)&(Y>=21)&(Y<=23); V=(X>=14)&(X<=16)&(Y>=2)&(Y<=3)
for k in 'abcde':
    s=np.asarray(Image.open('sprite_%s.png'%k)).astype(int); d=s!=r5
    print(k,'| ogen:',int((d&OOG).sum()),'| vlamtong:',int((d&V).sum()),'| rest:',int((d&~OOG&~V).sum()),'| kleuren',len(np.unique(s)))
