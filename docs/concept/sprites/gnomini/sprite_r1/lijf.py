# lijf.py A|B : schaduw en volume van het lijf (Jordi: "schaduw en volume wel kan verbeteren") als bovenlaag op sh_X.png -> lijf_X.png
# Regels (Gen 3, licht linksboven): middentint als basis, schaduwsikkel rechts (breedte per rij) en onderrand, slagschaduw onder de mutsrand,
# kleine hooglichtlens op roze (rechts naast de neus) en op blauw (linksboven). Kleurfamilie (roze/blauw) blijft die van het model.
import sys, numpy as np; from PIL import Image
from gemeen import *
var=sys.argv[1]
o=np.asarray(Image.open('sh_%s.png'%var)).astype(int).copy()
zone=np.load('zone_%s.npy'%var); L=np.load('lijn_%s.npy'%var)
ROZE=[6,7,8,9]; BLAUW=[10,11,12,13]

WR={40:0,41:2,42:2,43:3,44:3,45:3,46:4,47:4,48:5,49:5,50:5,51:6,52:7,53:8,54:9}
lijf=(zone==3)&~L
for Y,X in zip(*np.where(lijf)):
    fam=ROZE if o[Y,X] in ROZE else BLAUW
    if o[Y,X]==fam[1] and Y<=40: continue   # slagschaduw mutsrand (schaduw.py) blijft
    # afstand tot de rechterrand van het lijf in deze rij
    r=X
    while lijf[Y,r+1]: r+=1
    d=r-X
    b=Y
    while lijf[b+1,X]: b+=1
    t=2
    if d<WR.get(Y,0): t=1
    if b-Y<1 and Y>=50: t=1
    o[Y,X]=fam[t]
# hooglichtlenzen (licht linksboven op de bolling)
for Y,X in [(41,30),(41,31),(41,32),(42,29),(42,30),(42,31),(42,32),(42,33),(43,30),(43,31),(43,32)]:
    if lijf[Y,X] and o[Y,X] in ROZE: o[Y,X]=9
for Y,X in [(47,22),(47,23),(47,24),(47,25),(48,22),(48,23),(48,24),(48,25),(48,26),(49,23),(49,24),(49,25)]:
    if lijf[Y,X] and o[Y,X] in BLAUW: o[Y,X]=13
opslaan(o,'lijf_%s.png'%var)
