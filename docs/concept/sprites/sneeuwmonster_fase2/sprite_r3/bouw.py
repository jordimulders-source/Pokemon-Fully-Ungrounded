# Ronde 3 = r2 + drie benoemde reparaties (Claude): mond, emmer (duigen + bovenrand), gloeirand stenen.
# Gebruik vanuit sneeuwmonster_fase2: python3 sprite_r3/bouw.py
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *; from klassen import klassen; from naden import naad_kaart
PAL[7]=(132,78,42)   # donker hout = de schaduwtint van het model (gemeten mediaan rechterhelft L~88-95) i.p.v. (104,60,32): rechterhelft krijgt zo de modeltoon
o=np.asarray(Image.open('sprite_r2/sneeuwmonster2_r2.png')).astype(int).copy(); r2=o.copy()
a,c,L=klassen(); N4=((1,0),(-1,0),(0,1),(0,-1))
def sl(X,Y): return (slice(max(0,int(MY0+Y*F)),int(MY0+(Y+1)*F)),slice(int(MX0+X*F),int(MX0+(X+1)*F)))
fg=o>0
def leeg(Y,X): return not(0<=Y<64 and 0<=X<64) or not fg[Y,X]

# 1. MOND: pad per kolom uit het lijnprofiel van het model (onderkant lijn, zie NOTITIES); 1 px, lijntint 2, beide hoeken omhoog.
for Y in range(23,28):
    for X in range(19,37):
        if o[Y,X] in (1,2,3) and not (Y<=24 and 30<=X<=34) and not (Y==23 and 21<=X<=24):
            o[Y,X]=6
MOND={20:24,21:25,22:26,23:26,24:25,25:25,26:25,27:25,28:26,29:26,30:26,31:26,32:26,33:26,34:25,35:24}
for X,Y in MOND.items(): o[Y,X]=2

# 2. EMMER: vulling blijft die van r2 (meerderheid van de modeltonen; donker hout nu in de modeltint L~84).
#    Duignaden: per kolom het gemiddelde naadaandeel (naden.py: houtpixels >=22 donkerder dan het lokale houtgemiddelde
#    + zwart) boven en onder de band; pieken = naadkolommen (NOTITIES). Per rij volgt de naad het naadmaximum binnen +-1 kolom
#    (zo loopt hij licht schuin mee met het model). Naad = donker hout op licht/midden hout, zwart op donker hout.
naad,hw=naad_kaart()
BOVEN=[31,34,40,44]; ONDER=[28,32,35,39,41,44]
def regio(X):
    col=o[:20,X]; w=[Y for Y in range(20) if col[Y] in HOUT|{1} and not any(leeg(Y+dy,X+dx) for dy,dx in N4)]
    g=[Y for Y in range(20) if col[Y] in GRIJS]
    if not g: return [],[]
    return [Y for Y in w if Y<min(g)-1], [Y for Y in w if Y>max(g)+1]
vul=o.copy()
for lijst,deel in ((BOVEN,0),(ONDER,1)):
    for X0 in lijst:
        rows=regio(X0)[deel]
        if deel==0: rows=rows[2:]          # bovenste houtrij = bovenrand (zie hieronder)
        else: rows=rows[:-1] if len(rows)>3 else rows
        x=X0
        for Y in rows:
            kand=[xx for xx in (x-1,x,x+1) if vul[Y,xx] in HOUT and not any(leeg(Y+dy,xx+dx) for dy,dx in N4)]
            if not kand: continue
            x=max(kand,key=lambda xx:(naad[Y,xx],-abs(xx-X0)))
            if abs(x-X0)>1: x=X0
            if vul[Y,x] in HOUT: o[Y,x]=1 if vul[Y,x]==7 else 7
# naadstukjes van 1 px (geen naad boven/onder, ook niet schuin) terug naar de vulling: geen losse stippen
for Y,X in zip(*np.where((o!=vul)&(np.arange(64)[:,None]<20))):
    if not any(o[Y+dy,X+dx]!=vul[Y+dy,X+dx] for dy in (-1,1) for dx in (-1,0,1)): o[Y,X]=vul[Y,X]
    elif o[Y,X]==1 and any(o[Y+dy,X+dx] in SNEEUW for dy in (-1,0,1) for dx in (-1,0,1)): o[Y,X]=vul[Y,X]   # onderlijn emmer blijft hout
# bovenrand: eerste houtrij onder de buitenlijn = lichte rand van de (omgekeerde) emmerbodem, links licht, rechts midden
for X in range(26,48):
    ys=[Y for Y in range(2,12) if o[Y,X] in HOUT|{1}]
    if len(ys)>=3:
        Y=ys[0]+1
        if o[Y,X] in HOUT|{1} and not any(o[Y+dy,X+dx] in GRIJS for dy,dx in N4) and not any(leeg(Y+dy,X+dx) for dy,dx in N4):
            o[Y,X]=9 if X<=40 else 8

# 3. STENEN: gloeirand rondom waar het model aan de rand gloeit: randpixel >=8 % gloed -> rood (oranje/geel blijven),
#    en pixels net buiten de steen met >=20 % gloed (onderrand bovenste steen) -> rood.
x0,y0,x1,y1=STEENZONE
for Y in range(33,51):
    for X in range(18,30):
        s=sl(X,Y); g=np.isin(c[s],[6,7]).mean()
        if o[Y,X]==1 and g>=0.08: o[Y,X]=13
        elif o[Y,X] in SNEEUW and g>=0.20 and any(o[Y+dy,X+dx] in STEEN|{1} for dy,dx in N4): o[Y,X]=13
opslaan(o,'sprite_r3/sneeuwmonster2_r3.png')
print('r2->r3',(o!=r2).sum(),'px'); toon(o,2,28,14,50); toon(o,32,51,16,32)
