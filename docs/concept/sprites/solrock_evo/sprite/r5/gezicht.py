# r5 gezicht: plaat + ogen opnieuw uit het natieve raster met "donkerste wint" voor dunne lijnen.
# Per spritepixel alle natieve pixels waarvan het midden erin valt (±5,4). Regels:
#  rood >=2 -> rood (licht als lichtrood de meerderheid heeft); zwart >=2 -> K; bruin(L)+zwart >=2 -> plaatlijn (10);
#  anders: kern (g/w) in de meerderheid -> kern (r4-pixel blijft, of G2 als r4 daar plaat had); anders plaattint naar helderheidsklasse
#  (a->P1, b->P2, c->P3, meerderheid). Buiten de gezichtszone blijft r4.
import numpy as np, sys; from klas import *
sys.path.insert(0,'..'); from npy2png import save
r4=np.load('../r4/sprite.npy'); o=r4.copy()
ZX,ZY=(14,37),(21,47)
cnt={}
for j in range(N.shape[0]):
    for i in range(N.shape[1]):
        x,y=int(sx(i)),int(sy(j))
        if ZX[0]<=x<ZX[1] and ZY[0]<=y<ZY[1]: cnt.setdefault((y,x),[]).append(klas(N[j,i]))
P={'a':7,'b':8,'c':9,'A':13}
RED_MIN=int(sys.argv[1]) if len(sys.argv)>1 else 2
LIJN_MIN=int(sys.argv[2]) if len(sys.argv)>2 else 2
for (y,x),ks in cnt.items():
    if (x+0.5-31.1)**2+(y+0.5-34)**2>=16.0**2: continue   # alleen binnen de kern (ring/creme niet als plaat lezen)
    nr=sum(k in 'rR' for k in ks); nk=ks.count('K'); nl=ks.count('L'); ng=sum(k in 'gw' for k in ks)
    npl=sum(k in 'aAbc' for k in ks)
    if nr>=RED_MIN: v=11 if ks.count('r')>ks.count('R') else 12
    elif ng>npl and ng>=nk+nl: v=r4[y,x] if r4[y,x] in (1,2,3,4) else 3
    elif nk>=LIJN_MIN and nk>=nl: v=1
    elif nk+nl>=LIJN_MIN: v=10
    else:
        pl=[('a' if k=='A' and ks.count('A')<2 else k) for k in ks if k in 'aAbc']
        v=P[max(set(pl),key=pl.count)] if pl else r4[y,x]
    o[y,x]=v
# ogen + ooglid: 2x2 uit het natieve raster (kleinste reductie die lens, lid en contour houdt), gecentreerd op de eigen modelplek
from oog2x import red
M={'K':1,'R':12,'r':11,'a':7,'b':8,'c':9,'L':10,'A':13}
OOG={'L':(61,84,8,9,1,0),'R':(84,86,9,10,0,0)}
for k,(x0,y0,w,h,fx,fy) in OOG.items():
    b=red(x0+fx,y0+fy,w,h)
    cx=sx(x0+fx+w); cy=sy(y0+fy+h)          # natief blokmidden -> sprite
    X=int(round(cx-w/2)); Y=int(round(cy-h/2)); print(k,'blok op',X,Y,w,h)
    for j,row in enumerate(b):
        for i,c in enumerate(row):
            if c in M: o[Y+j,X+i]=M[c]
np.save('gezicht.npy',o)
ch='.KdmlCGabcLrRA'
for j in range(ZY[0],ZY[1]): print('%2d '%j+''.join(ch[o[j,i]] for i in range(ZX[0],ZX[1])))
