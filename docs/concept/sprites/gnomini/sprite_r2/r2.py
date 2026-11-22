# r2.py: alleen de 5 keurderreparaties op r1 (gnomini_A) -> gnomini.png; bewijst diff 0 buiten de opdrachtzones.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite_r1'); import os; os.chdir('../sprite_r1'); from gemeen import opslaan; os.chdir('../sprite_r2')
o=np.asarray(Image.open('r1.png')).astype(int); n=o.copy()
P,Q,R,S,C,BD=6,7,8,9,4,10   # p (172,72,102), q (213,102,136), r (244,153,181), s (251,184,202), c muts (184,163,211), blauw donker (56,109,142)
zones={}
def zet(naam,pts,k):
    for x,y in pts: n[y,x]=k
    zones.setdefault(naam,set()).update(pts)
# 1 roze schaduwsikkel
zet('1 sikkel',[(39,41),(40,41),(38,42),(39,42),(40,42),(37,43),(38,43),(39,43),(37,44),(38,44),(36,45),(37,45)],Q)
# 2 hooglicht 2 px naar links; rij 41 x28 grenst aan de neuslijn (x26-27) -> geen r-rand -> een rij lager (y42-44)
oud=[(30,41),(31,41),(32,41),(29,42),(30,42),(31,42),(32,42),(33,42),(30,43),(31,43),(32,43)]
nieuw=[(28,42),(29,42),(30,42),(27,43),(28,43),(29,43),(30,43),(31,43),(28,44),(29,44),(30,44)]
zet('2 hooglicht',[p for p in oud if p not in nieuw],R); zet('2 hooglicht',nieuw,S)
zet('3 armlijn',[(20,41)],P)
zet('4 muts',[(26,33)],C)
zet('5 blauw',[(41,52)],BD)
opslaan(n,'gnomini.png')
mask=np.zeros((64,64),bool)
for pts in zones.values():
    for x,y in pts: mask[y,x]=True
d=n!=o
print('diff buiten opdrachtzones:',(d&~mask).sum())
for k,pts in zones.items(): print(k,'gewijzigd',sum(d[y,x] for x,y in pts),'/',len(pts))
