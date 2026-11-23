# r7.py: r7 = r6 + Jordi's punten op r6 (vormen uit de meting van het model, meet6.npz) + Gen 3-tintopbouw.
import numpy as np; from PIL import Image
from scipy import ndimage as nd
from meting_sprite import is_lijn, groep
r6=Image.open('r6.png'); R6=np.asarray(r6).astype(int); O=R6.copy(); S=R6>0
d=np.load('meet6.npz'); lf,hel=d['lf'],d['hel']; Z=np.load('zone.npy')
LIJN={'steen':2,'licht':4,'roze':6,'blauw':9}
rand4=S&~nd.binary_erosion(S)          # buitenrand (4-buren): r6 houden
BRON={}
def meet_lijnen(mask,naam):
    """lijnen uit het model binnen mask (niet op de buitenrand); vlakken krijgen voorlopig de middentint (tintpass volgt)."""
    MID={'steen':4,'licht':13,'roze':8,'blauw':10}
    for y,x in zip(*np.where(mask&~rand4)):
        g=groep(y,x)
        if g is None: O[y,x]=1
        elif is_lijn(y,x): O[y,x]=1 if (lf[y,x]>=0.8 or R6[y,x]==1) else LIJN[g]
        else: O[y,x]=MID[g]
        BRON[y,x]=naam
# 1. linkerarm + vuist (zone 7): vorm uit de meting (vuist loopt tot x 11, lijn x 12, korte ovale arm x 13-16)
meet_lijnen(Z==7,'arm L')
# 1b. arm boller (Jordi: "arm is een rechte lijn"; silhouetwijziging toegestaan): de bovenrand van de modelarm ligt in het midden
# op modelrij 30,7 -> spritepixels (14,30),(15,30) zijn voor 20-25 % gedekt (drempel 0,2, zoals de stok 0,35 kreeg) -> lijn; eronder vlak.
for x in (14,15): O[30,x]=6; O[31,x]=8; BRON[30,x]='arm L (silhouet)'; BRON[31,x]='arm L'
# 2. rechterschouder: bovenlijn van het ovaal uit de modellijnen (lijnaandeel >= 0,18: rij 21 x 41-44, rij 22 x 46)
for y,x in ((21,41),(21,42),(21,43),(21,44),(22,46)): O[y,x]=6; BRON[y,x]='schouder'
# 3. mutspunt + rugrots (zone 1, x >= 40, rij 4-19): lijnen uit de meting (schuine knik van de rots, lijn tussen punt en rots)
m=np.zeros_like(S); m[4:20,40:51]=True; meet_lijnen(m&(Z==1),'muts/rots')
# 4. haar L (zone 2) + mutsrand ernaast (x 17-19, rij 12-15): uit de meting; grens haar|muts = lijn 2
m=np.zeros_like(S); m[12:16,17:20]=True; meet_lijnen((Z==2)|(m&(Z==1)),'haar L')
for y,x in list(BRON):
    if BRON[y,x]=='haar L' and O[y,x]==4 and Z[y,x]==2:
        if any(Z[y+dy,x+dx]==1 and O[y+dy,x+dx] not in (1,2) and O[y+dy,x+dx]>0 for dy,dx in ((0,1),(-1,0),(0,-1),(1,0))): O[y,x]=2
np.save('na_vorm.npy',O)
import pickle; pickle.dump(BRON,open('bron_vorm.pkl','wb'))
