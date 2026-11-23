# meet per (dx,dy) de lijfafstand (Chebyshev, dus ook diagonaal) van de mond tot linker- en rechteroog
import numpy as np, r5
import contextlib,io
import sys
OOGL={'c3':(r5.C3,int(sys.argv[2])),'c3_6':(np.insert(r5.C3,1,r5.C3[1],0),int(sys.argv[2]))}[sys.argv[1]]
for dx in (0,1,2,3):
    for dy in (1,2,3):
        with contextlib.redirect_stdout(io.StringIO()):
            B,niet,over,gap,mond=r5.bouw(OOGL[0],OOGL[1],dx,dy)
        A=B.copy()
        oogR=np.zeros((64,64),bool); oogR[40:45,28:33]=np.isin(B[40:45,28:33],[8,9,10,11])
        my,mx=np.where(mond); ry,rx=np.where(oogR)
        gr=min(max(abs(a-c),abs(b-d)) for a,b in zip(my,mx) for c,d in zip(ry,rx))-1
        print('dx',dx,'dy',dy,'| lijf links',gap,'rechts',gr,'| mond y',my.min(),my.max(),'x',mx.min(),mx.max())
