# Gaucho-Ludicolo r1, variant 0: kale reductie (kaal_vlak.py) + gezichtsreparatie naar het model + technische opschoning.
# Schrijft basis0.npy en ludicolo_gaucho_0.png; telt per stap de gewijzigde pixels t.o.v. de kale reductie.
import numpy as np
from gemeen import opslaan, ROOD, OLIJF, GEEL
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
o=np.load('kaal_vlak.npy').copy(); kaal=o.copy(); tel={}
def stap(n,v): tel[n]=tel.get(n,0)+int((v!=o).sum())
def g(y,x): return o[y,x] if 0<=y<64 and 0<=x<64 else 0
K,l,d,L,m,M=1,2,4,7,5,6
# 1. Gezicht (per pixel naar het model, natief gemeten; zie NOTITIE):
v=o.copy()
o[25,22]=d; o[26,22]=L            # linkeroog: model rij 36-38 rond pupil x35 = d / L K L (iris aan beide kanten)
o[24,28]=3                        # rechteroog: pupil los van de hoedrandlijn (model x46 rij 36 = D)
o[27,28]=M                        # rechteroog: pupil 2 hoog zoals links (model x46 rij 40 = M)
o[26,27]=m                        # rechteroog: iris links van de pupil (model x45 rij 38-39 = m/M)
o[31,20]=13; o[32,19]=13          # mond: 1 px lijn zonder dubbele stukken (model: trap 2-4-6-5 natief, rij 45-48)
stap('gezicht (ogen, mond) naar het model',v)
FACE=lambda y,x: 24<=y<=34 and 15<=x<=35
def mat(y,x):
    k=o[y,x]
    if k in ROOD: return 'r'
    if k in OLIJF: return 'o'
    if k in GEEL: return 'g'
    ms=[('r' if o[y+dy,x+dx] in ROOD else 'o' if o[y+dy,x+dx] in OLIJF else 'g') for dy,dx in N8
        if 0<=y+dy<64 and 0<=x+dx<64 and o[y+dy,x+dx] in ROOD|OLIJF|GEEL]
    return max(set(ms),key=ms.count) if ms else None
# 2. Buitenlijn (zoals gaucho-Lotad/Lombre): rand rechts/onder aan de achtergrond = zwart; rand alleen links/boven = selout
#    in de lijntint van het materiaal (rood 2, olijf 8, geel 12). Silhouet blijft gelijk (alleen indexwissels).
v=o.copy(); nieuw=[]; SEL={'r':2,'o':8,'g':12}
for y,x in zip(*np.where(o>0)):
    bgR=g(y,x+1)==0; bgD=g(y+1,x)==0; bgL=g(y,x-1)==0; bgU=g(y-1,x)==0
    if not(bgR or bgD or bgL or bgU): continue
    if bgR or bgD:
        if o[y,x]!=K: nieuw.append((y,x,K))
    else:
        mm=mat(y,x)
        if mm and o[y,x]!=SEL[mm]: nieuw.append((y,x,SEL[mm]))
for y,x,k in nieuw: o[y,x]=k
stap('buitenlijn (selout links/boven, zwart rechts/onder)',v)
# 3. Losse tintpixels (geen gelijke 8-buur; geen lijnen, niet in het gezicht) -> meest voorkomende buurtint uit dezelfde groep.
v=o.copy()
for y,x in zip(*np.where(np.isin(o,[3,4,5,6,7,9,10,11,12,13]))):
    if FACE(y,x): continue
    k=o[y,x]; nb=[g(y+dy,x+dx) for dy,dx in N8]
    if k in nb: continue
    grp=ROOD if k in ROOD else OLIJF if k in OLIJF else GEEL
    kand=[b for b in nb if b in grp and b not in (1,2,8)]
    if kand: o[y,x]=max(set(kand),key=kand.count)
stap('losse tintpixels',v)
assert ((o>0)==(kaal>0)).all(), 'silhouet gewijzigd'
for k,n in tel.items(): print('%-55s %3d px'%(k,n))
print('totaal t.o.v. kale reductie', int((o!=kaal).sum()),'px; silhouet-diff',int(((o>0)!=(kaal>0)).sum()))
np.save('basis0.npy',o); opslaan(o,'ludicolo_gaucho_0.png')
