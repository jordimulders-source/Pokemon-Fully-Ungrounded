# r10.py: onderarm loopt door in de hand (Jordi: "bij beide sluit de hand niet aan op de onderarm"). Alleen onderarm/pols, zone x12-21, y33-42.
# A: de lijnen tussen onderarm en hand weg (rij 38 x13-15, (15-16,39), rij 40 x16-19), grijs loopt door; schaduw d onder de pols blijft.
# B: idem, maar een korte polsplooi in d op rij 40 (x16-18) i.p.v. de zwarte lijn.
import pal,numpy as np,sys
B0=[list(r) for r in pal.load('basis_L1.txt')]
A={(13,38):'c',(14,38):'c',(15,38):'c',(15,39):'c',(16,39):'c',(16,40):'c',(17,40):'c',(18,40):'c',(19,40):'c',
   (15,41):'c',(16,41):'c',(20,36):'d',(20,37):'d',(20,38):'d',(19,39):'d',
   (12,37):'o',(13,37):'b'}   # pols 1 px breder: (12,37) erbij (alpha), contour loopt recht door naar de hand
Bv=dict(A); Bv.update({(16,40):'d',(17,40):'d',(18,40):'d'})   # B: polsplooi
ZONE=(12,33,21,42)
for n,ch in {'A':A,'B':Bv}.items():
    R=[r[:] for r in B0]
    for (x,y),c in ch.items(): R[y][x]=c
    R=[''.join(r) for r in R]; open(f'var_{n}.txt','w').write('\n'.join(R)+'\n'); pal.topng(R,f'var_{n}.png')
    a=np.array([list(r) for r in R]); b=np.array(B0); ys,xs=np.where(a!=b)
    buiten=[(x,y) for x,y in zip(xs,ys) if not (ZONE[0]<=x<=ZONE[2] and ZONE[1]<=y<=ZONE[3])]
    print(n,len(xs),'px gewijzigd, buiten de zone:',buiten)
