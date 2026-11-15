# Bewaakt c2 t.o.v. p8: silhouet-diff 0, buitenlijn ongewijzigd, lijn/oog/mond/tong/tand-pixels van p8 ongewijzigd,
# gezicht-rechthoek (oog, snuit, mond, tanden, tong) index-diff 0 EN kleur van de gezichtsindexen (6,9,10,11,12,13,15)
# gelijk aan p8, palet <=16. Telt hooglicht (14) buiten de tenen.
import numpy as np
from PIL import Image
from basis import bevroren_kop
P=Image.open('../p8/welp_p8.png'); p8=np.array(P); pp=P.getpalette()[:48]
def rand(a):
    m=a>0; r=np.zeros_like(m)
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)): r|=m&~np.roll(np.roll(m,dy,0),dx,1)
    return r
ok=True
for f in ('welp_c2.png','welp_c2_grijs.png'):
    I=Image.open(f); a=np.array(I); pa=I.getpalette()[:48]
    sil=int(((a>0)!=(p8>0)).sum()); buit=int((rand(p8)&(a!=p8)).sum())
    lijn=int((np.isin(p8,[1,2,10,12,13,15])&(a!=p8)).sum()); kop=int((bevroren_kop()&(a!=p8)).sum())
    kleur=all(pa[3*k:3*k+3]==pp[3*k:3*k+3] for k in (6,9,10,11,12,13,15)); n=len(np.unique(a))
    teen=(p8==14); hl=int(((a==14)&~teen).sum())
    print(f,'| silhouet-diff',sil,'| buitenlijn',buit,'| lijnen/oog/mond',lijn,'| gezicht-zone',kop,'| gezichtskleuren = p8',kleur,'| kleuren',n,'| hooglicht px (excl. tenen)',hl,'+ tenen',int(teen.sum()),'| anders dan p8',int((a!=p8).sum()))
    ok&=sil==0 and buit==0 and lijn==0 and kop==0 and kleur and n<=16
print('ALLES OK' if ok else 'FOUT')
