# Cuyby ronde 5, variant_asym: A5 silhouet licht asymmetrisch. Basis: ronde 5 (= ronde 4 + C6).
# De rechter (schaduw)flank hangt lager uit: rijen y33-39 lopen 1 px verder naar rechts
# (oude rand-9 wordt schaduw 8, nieuwe 9 ernaast). Rijen y28-32 en y40+ blijven.
from fu import *
base,pal=load('cuyby/ronde5'); old4,_=load('cuyby/ronde4'); a=base.copy()
OUT={1,9,5,11}
for f,dy in ((0,0),(1,-1)):
    for y in range(33,40):
        Y=64*f+y+dy; row=a[Y]; last=max(x for x in range(64) if row[x]!=0)
        assert row[last]==9 and row[last-1] in (8,), (f,y,last,row[last-1])
        a[Y,last]=8; a[Y,last+1]=9
zones=[(0,25,43,28,46),(1,25,42,28,45),(0,44,33,47,39),(1,44,32,47,38)]
r,outside=report(old4,a,zones,OUT); print('\n'.join(r)); assert outside==0
save(a,pal,'cuyby/ronde4','cuyby/ronde5/variant_asym')
