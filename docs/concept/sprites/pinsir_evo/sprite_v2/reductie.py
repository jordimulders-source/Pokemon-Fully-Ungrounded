# Gedeeld: natief raster -> klassen, en de exacte puntreductie naar 64 px. Geen tekenen; alleen modelcellen.
import numpy as np; from PIL import Image
from collections import Counter
D='sprite_v2/'
a=np.asarray(Image.open(D+'natief_ruw.png')).astype(int)
r,g,b=a[...,0],a[...,1],a[...,2]; L=(0.299*r+0.587*g+0.114*b)
H,W=L.shape
BG=(a.min(2)>222)&((r-b)<40)
BLK=(L<26)&~BG
RED=(r-g>38)&~BLK&~BG
CREAM=(L>=165)&~BG&~RED
BROWN=~BG&~BLK&~RED&~CREAM
EYE=np.zeros_like(BG); EYE[27:31,24:38]=True; EYE&=CREAM      # gele ogen (alleen op deze plek)
FACE=np.zeros_like(BG); FACE[26:46,22:40]=True                  # kop/mond: alle lijnen houden
# klasse-codes:  0 bg, 1 zwart, 2 bruin-lijntint, 3..6 bruin schaduw..hooglicht, 7 roomdonker, 8 roomlicht, 9 rood donker, 10 rood licht, 11 oog
K=np.zeros((H,W),int)
K[BLK]=1
bl=[60,92,118,140]
for i,(lo,hi) in enumerate(zip([-1]+bl,bl+[999])): K[BROWN&(L>lo)&(L<=hi)]=2+i
K[CREAM&(L<=195)]=7; K[CREAM&(L>195)]=8
K[RED&(L<=75)]=9; K[RED&(L>75)]=10
K[EYE]=11
X0,Y0=5,11; S=64/91
def kaart(phx=0.3,phy=0.3,s=S):
    cx=np.floor((np.arange(W)-X0)*s+phx).astype(int); cy=np.floor((np.arange(H)-Y0)*s+phy).astype(int)
    return cx,cy
