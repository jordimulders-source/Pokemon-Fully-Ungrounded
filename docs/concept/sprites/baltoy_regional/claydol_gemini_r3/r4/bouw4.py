# Ronde 4 op r3. Niets middelen/gladmaken: alleen per pixel uit het model (natieve modelpixel) en hoeken scherp uit het model.
import sys, numpy as np; sys.path.insert(0,'.'); sys.path.insert(0,'r4')
from natcoord import S3
from knop import knoppen, scherp, ZR, ZL
S=S3.copy(); log=[]
# 1. Neusruggen: r3 heeft ze al (lichte rug met donkere randlijnen tot de kaakrand, g3-onderkop terug); r2 had ze vanaf rij 31
#    weggemiddeld. Geen wijziging.
# 2+3. Stafknoppen
log+=knoppen(S); log+=scherp(S)
# 4. Treden bovenop het lijf (model natief rij 62-65): links liep de trede schuin (44,24)->(45,24)->(46,25) en las als ^;
#    rechts was de verticale lijn (natief x47, rijen 63-65) weggeschrapt (kolom 47).
ZT=np.zeros((64,64),bool); ZT[43:48,20:37]=True
for y,x,why in ((46,24,'trede links: hoek (verticaal 44-46 op x24, dan voet)'),
                (45,31,'trede rechts: verticale lijn natief x47 rij 63 (kolom 47 was geschrapt) op x31'),
                (47,31,'trede rechts: verticale lijn natief x47 rij 65 op x31')):
    log.append(('treden lijf',y,x,int(S[y,x]),8)); S[y,x]=8
ZONES=ZR|ZL|ZT
np.save('r4/sprite_r4.npy',S)
if __name__=='__main__':
    from collections import Counter
    from cc import label
    d=S!=S3
    print('gewijzigd',int(d.sum()),'| buiten zones',int((d&~ZONES).sum()),'| per zone',Counter(z for z,*_ in log))
    for l in log: print(l)
    c,n=label(S>0,diag=True); print('componenten',n)
