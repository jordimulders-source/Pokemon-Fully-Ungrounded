# Rechterklauw: exacte 2x van het natieve modelvak x 77-92, y 111-122 (zonder geschrapte kolommen/rijen, dus alle tenen en
# teenlijnen blijven), als voorste vorm op sprite X 32-39, Y 48-53, met gesloten omlijning tegen de staart.
# Regels per 2x2-blok: klauw (ivoor/wit) wint bij >=1 px (vorm voor kleur); lijn bij >=2 px of als 1 px en de lijn verticaal
# doorloopt (teenscheiding); anders goud, toon licht (4) als het lichte goud de meerderheid heeft, anders schaduw (3).
import numpy as np, sys
sys.path.insert(0,'../sprite_r3/gereedschap'); import os
N=np.load('../sprite_r3/natief.npy'); P=np.load('../sprite_r3/natief_pal.npy'); lum=P@np.array([.299,.587,.114])
from half import GR
NX,NY,SX,SY,BW,BH=77,111,32,48,8,6
def voet(variant='A'):
    f=np.zeros((BH,BW),int)
    for j in range(BH):
        for i in range(BW):
            y,x=NY+2*j,NX+2*i; b=[N[y+a,x+c] for a in (0,1) for c in (0,1)]
            g=[GR[k] if k>=0 else '.' for k in b]
            nW=sum(1 for k in b if k>=0 and GR[k]=='W'); nL=g.count('L')
            vert=nL==1 and any(N[yy,xx]>=0 and GR[N[yy,xx]]=='L' for yy in (y-1,y+2) for xx in (x,x+1))
            if nW>=1 and j>=2: f[j,i]=7 if nW>=2 or j==BH-1 else 14
            elif nL>=2 or vert: f[j,i]=1
            elif g.count('.')>=3: f[j,i]=0
            else:
                gl=[lum[k] for k in b if k>=0 and GR[k] in 'GD']
                f[j,i]=4 if gl and np.mean([l>170 for l in gl])>=0.5 else 3
    if variant=='B':   # klauwpunten 1-op-1 zoals Gen 3: lichte pixel met schaduwpixel eronder, alleen onderaan elke teen
        for i in range(BW):
            col=f[:,i]
            if 7 in col or 14 in col:
                rows=[j for j in range(BH) if col[j] in (7,14)]
                for j in rows: f[j,i]=3 if j<BH-2 else f[j,i]
                f[BH-2,i]=7; f[BH-1,i]=14
    return f
def plak(o,f):
    o=o.copy(); m=np.zeros((64,64),bool)
    for j in range(BH):
        for i in range(BW):
            if f[j,i]>0: o[SY+j,SX+i]=f[j,i]; m[SY+j,SX+i]=True
    # gesloten omlijning: buitenrand van de voet tegen staart/lijf (links, rechts, onder) zwart, buiten het voetmasker
    for Y,X in zip(*np.where(m)):
        for dy,dx in ((1,0),(0,-1),(0,1)):
            YY,XX=Y+dy,X+dx
            if dy==1 and o[Y,X] in (7,14): continue      # onder de klauwpunt geen lijn: anders een rechte balk van 8 px
            if 0<=YY<64 and 0<=XX<64 and not m[YY,XX] and o[YY,XX]>0: o[YY,XX]=1
    return o,m

def voet2(variant='A'):
    """Teenstructuur uit de modellijnen: per spritekolom (natief kolompaar) is het een teenscheiding als het paar in de
    teenrijen (natief 115-122) in >=4 rijen een lijnpixel heeft; anders een teen. Teentoon = modelhelderheid van het paar
    (licht goud -> 4, anders 3). Klauwpunt onderaan een teen als het paar in natief 117-122 ivoor/wit heeft.
    A: teenscheiding donker goud (binnenlijn), klauw 1 px licht (7). B: teenscheiding zwart, klauw 2 px (7 boven, 14 eronder) en teen boven licht/onder schaduw."""
    f=np.zeros((BH,BW),int)
    isL=lambda k:k>=0 and GR[k]=='L'; isW=lambda k:k>=0 and GR[k]=='W'
    for i in range(BW):
        x=NX+2*i; cols=(x,x+1)
        sep=sum(any(isL(N[y,c]) for c in cols) for y in range(115,123))>=4 and 1<=i<=BW-2
        rand=i==BW-1
        claw=any(isW(N[y,c]) for y in range(117,123) for c in cols)
        for j in range(BH):
            y=NY+2*j; b=[N[y+a,c] for a in (0,1) for c in cols]
            if j==0:
                f[j,i]=1 if sum(isL(k) for k in b)>=2 else 3; continue
            if rand and j>=1: f[j,i]=1; continue
            if sep and j>=2: f[j,i]=2 if variant=='A' else 1; continue   # A: binnenlijn in donkerste goudtint, B: zwart
            gl=[lum[k] for k in b if k>=0 and GR[k] in 'GD']
            t=4 if gl and np.mean([l>170 for l in gl])>=0.5 else 3
            if variant=='B': t=4 if j<=2 else 3
            f[j,i]=t
        if claw and not sep:
            f[BH-2,i]=7; f[BH-1,i]=14     # klauwpunt 2 px zoals Gen 3 (licht boven, ivoorschaduw onder)
    return f
