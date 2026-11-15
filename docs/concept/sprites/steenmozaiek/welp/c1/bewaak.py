# Bewaakt c1 t.o.v. p8: silhouet-diff 0, buitenlijn (randpixels) ongewijzigd, alle lijn/oog/mond/tong/tand-pixels van p8
# (index 1,2,10,12,13,15) ongewijzigd, bevroren kop-rechthoek (oog, snuit, mond, tanden, tong) ongewijzigd, palet <=16.
import numpy as np
from PIL import Image
from basis import bevroren_kop
p8=np.array(Image.open('../p8/welp_p8.png'))
def rand(a):
    m=a>0; r=np.zeros_like(m)
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        s=np.roll(np.roll(m,dy,0),dx,1); r|=m&~s
    return r
ok=True
for v in 'ABC':
    a=np.array(Image.open('welp_c1_%s.png'%v))
    sil=int(((a>0)!=(p8>0)).sum()); R=rand(p8); buit=int((R&(a!=p8)).sum())
    vast=np.isin(p8,[1,2,10,12,13,15]); lijn=int((vast&(a!=p8)).sum())
    kop=int((bevroren_kop()&(a!=p8)).sum()); n=len(np.unique(a))
    print(v,'silhouet-diff',sil,'| buitenlijn gewijzigd',buit,'| lijn/oog/mond/tong gewijzigd',lijn,'| kop-zone gewijzigd',kop,'| kleuren incl. transparant',n,'| pixels anders dan p8',int((a!=p8).sum()))
    ok&=sil==0 and buit==0 and lijn==0 and kop==0 and n<=16
print('ALLES OK' if ok else 'FOUT')
