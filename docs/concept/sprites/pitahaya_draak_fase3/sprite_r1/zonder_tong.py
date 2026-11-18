# Variant zonder tong: de hoofdversie, met alleen de bek-/tongzone (x 0-12, y 26-38) uit dezelfde pijplijn op model_zonder_tong
# (zelfde geometrie: --ref natief.png --plaats). Buiten de zone diff 0 met de hoofdversie (assert), zodat Jordi alleen de tong vergelijkt.
# Gebruik: python3 zonder_tong.py MET.png ZONDER_PIJPLIJN.png UIT.png
import sys,numpy as np; from PIL import Image
M=Image.open(sys.argv[1]); m=np.asarray(M).astype(int); z=np.asarray(Image.open(sys.argv[2])).astype(int)
ZX0,ZX1,ZY0,ZY1=0,12,26,38
o=m.copy(); o[ZY0:ZY1+1,ZX0:ZX1+1]=z[ZY0:ZY1+1,ZX0:ZX1+1]
assert not ((o>=12)&(o<=14)).any(), 'tongresten'
buiten=np.ones((64,64),bool); buiten[ZY0:ZY1+1,ZX0:ZX1+1]=False
assert (o[buiten]==m[buiten]).all()
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette(M.getpalette()); im.save(sys.argv[3],transparency=0)
d=np.where(o!=m); print(sys.argv[3],'gewijzigd t.o.v. hoofdversie',len(d[0]),'px, alle binnen x %d-%d, y %d-%d; buiten de zone 0'%(ZX0,ZX1,ZY0,ZY1))
