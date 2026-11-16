# Diff r2 t.o.v. r1 per zone (en per spikkelvariant), plus kleuren en controle.
import numpy as np; from PIL import Image
r1=np.asarray(Image.open('../r1/sprite.png')).astype(int); r1b=np.asarray(Image.open('../r1/stap_twinkel.png')).astype(int)  # r1 zonder spikkels
Y,X=np.mgrid[:64,:64]
KZ=(X<26)&(Y<31)&~((X>=22)&(Y>=24)); GZ=(X>=9)&(X<18)&(Y>=18)&(Y<27); PZ=(Y>=44)&(X<47)
ZONES={'gezicht (9-17,18-26)':GZ,'kop (rest)':KZ&~GZ,'pijl':PZ,'lijf+staart':~KZ&~PZ}
basis=np.load('r2_basis.npy')
print('r2-basis (zonder kopspikkels) t.o.v. r1 zonder kopspikkels:')
for z,m in ZONES.items():
    d=(basis!=r1b)&m; print('  %-22s %4d px'%(z,d.sum()))
print('  totaal %d'%((basis!=r1b).sum()))
for k in 'ABC':
    s=np.asarray(Image.open('sprite_%s.png'%k)).astype(int)
    print('variant',k,': kopspikkels',int(((s!=basis)).sum()),'px; kleuren incl. transparant',len(np.unique(s)))
