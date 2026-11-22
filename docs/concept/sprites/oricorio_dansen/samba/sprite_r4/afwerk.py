# Afwerking (alleen herkleuren, dekking blijft gelijk): selout aan de lichtkant. Buitenlijnpixel (zwart of donkere lijntint) waarvan de
# transparante buren alleen boven/links liggen -> donkere tint van het vlak eronder/rechts (groen G3, geel Y3, blauw B2, roze K3);
# met transparant rechts/onder -> zwart.  gebruik: afwerk.py in.txt uit.txt
import numpy as np, sys
from dump import LET, INV
from collections import Counter
o=np.array([[INV[c] for c in r] for r in open(sys.argv[1]).read().split('\n')[:64]]); oud=o.copy()
O,G1,G2,G3,G4,Y1,Y2,Y3,B1,B2,K1,K2,K3,W=range(1,15)
FAM={G1:G3,G2:G3,G3:G4,Y1:Y3,Y2:Y3,B1:B2,B2:B2,K1:K3,K2:K3}
LIJN=(O,G4,Y3,B2,K3)
H=W_=64
def t(y,x): return not(0<=y<H and 0<=x<W_) or oud[y,x]==0
n=Counter()
for y in range(H):
    for x in range(W_):
        if oud[y,x] not in LIJN: continue
        if 26<=y<=33 and 23<=x<=36: continue   # Pom-Pom-oog en -snavel pixel voor pixel: niet herkleuren
        boven=t(y-1,x); links=t(y,x-1); onder=t(y+1,x); rechts=t(y,x+1)
        if not(boven or links or onder or rechts): continue
        if (onder or rechts):
            if oud[y,x]!=O: o[y,x]=O; n['zwart_schaduwkant']+=1
            continue
        # lichtkant: tint van de vulling rechts/onder
        c=Counter(oud[a,b] for a,b in ((y+1,x),(y,x+1),(y+1,x+1)) if 0<=a<H and 0<=b<W_ and oud[a,b] in FAM)
        if c:
            v=FAM[c.most_common(1)[0][0]]
            if y<=21 and v==Y3 and x<46 and not (14<=y): v=G3   # geel puntje van een groene tooiveer: donkergroene rand zoals het model
            if v!=o[y,x]: o[y,x]=v; n['selout_lichtkant']+=1
open(sys.argv[2],'w').write('\n'.join(''.join(LET[v] for v in r) for r in o)+'\n')
assert ((o>0)==(oud>0)).all(); print(dict(n))
# 2. ontkorrelen: losse vulpixels (G1/G2/Y1/Y2, 8-samenhang 1 px) binnen het silhouet -> meest voorkomende vulbuur; rokhangers (rij 45-47) en kop bevroren
from scipy import ndimage as nd
o2=o.copy(); m=0
for k in (G1,G2,Y1,Y2):
    lab,nn=nd.label(o==k,structure=np.ones((3,3)))
    for i in range(1,nn+1):
        p=np.argwhere(lab==i)
        if len(p)!=1: continue
        y,x=p[0]
        if 45<=y<=47 and 25<=x<=39: continue
        if 26<=y<=33 and 23<=x<=36: continue
        c=Counter(o[a,b] for a,b in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)) if o[a,b] in (G1,G2,G3,Y1,Y2) and o[a,b]!=k)
        if c and not any(o[a,b]==0 for a,b in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))):
            o2[y,x]=c.most_common(1)[0][0]; m+=1
o=o2; open(sys.argv[2],'w').write('\n'.join(''.join(LET[v] for v in r) for r in o)+'\n'); print('ontkorreld',m)
