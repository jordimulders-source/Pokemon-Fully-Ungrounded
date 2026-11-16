# Bewijs r6: diff t.o.v. r5 115% (geel) alleen in het oogvak x10-16, y19-24; daarbuiten 0.
import numpy as np; from PIL import Image
r5=np.asarray(Image.open('../r5/sprite_115_geel.png')).astype(int); Y,X=np.mgrid[:64,:64]; OV=(X>=10)&(X<=16)&(Y>=19)&(Y<=24)
for n in ('geel_glans','geel','goud_glans','goud'):
    s=np.asarray(Image.open('sprite_%s.png'%n)).astype(int); d=s!=r5
    print(n,'| oogvak:',int((d&OV).sum()),'px | buiten het oogvak:',int((d&~OV).sum()),'| kleuren',len(np.unique(s)))
