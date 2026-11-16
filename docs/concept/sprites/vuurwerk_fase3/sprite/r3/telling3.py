# Bewijs bevriezing: r3 t.o.v. r2 (zonder spikkels). Buiten de kop (KZ, zonder twinkels en losse vlam) moet de diff 0 zijn.
import numpy as np; from PIL import Image
r2=np.load('r2_basis.npy'); Y,X=np.mgrid[:64,:64]
KZ=(X<26)&(Y<31)&~((X>=22)&(Y>=24)); FACE=(X>=6)&(X<=17)&(Y>=15)&(Y<=26)
for g in 'VW':
    b=np.load('r3_kop_%s.npy'%g); d=b!=r2
    print(g,'gezicht-vak:',int((d&FACE).sum()),'| kop rest:',int((d&KZ&~FACE).sum()),'| buiten de kop (lijf, lijnen, pijl):',int((d&~KZ).sum()),'| kleuren',len(np.unique(b)))
    for k in 'ABC':
        s=np.asarray(Image.open('sprite_%s_%s.png'%(g,k))).astype(int); e=(s!=b)
        print('   variant',k,'spikkelpixels',int(e.sum()),'(alle op lege pixels:',bool((b[e]==0).all()),') kleuren',len(np.unique(s)))
