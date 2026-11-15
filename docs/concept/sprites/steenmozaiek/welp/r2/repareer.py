# Stap 3b + 4: benoemde reparaties per pixel op onderlaag_50 -> welp_r2_zonder_extra. Alles naar het model.
import numpy as np
from PIL import Image
from reduceer import X0,X1,Y0,Y1
a=np.load('onderlaag_50.npy'); FIN=np.load('FIN.npy').tolist()
# irisgrijs uit het model: mediaan van de grijze modelpixels in het oog (spritecellen x11-14, y9-10)
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); s=(X1-X0)/50
eye=n[int(Y0+9*s):int(Y0+11*s),int(X0+11*s):int(X0+15*s)].reshape(-1,3)
sat=eye.max(1)-eye.min(1); lum=eye@[0.299,0.587,0.114]
g=eye[(sat<25)&(lum>100)&(lum<165)]; G=tuple(int(v) for v in g[np.argmin(((g-np.median(g,0))**2).sum(1))])
print('irisgrijs uit model',G,len(g),'px')
FIN.append(list(G)); GI=len(FIN)-1
K,d,S,M,L,P,Q,R,g_,W,C,T=range(1,13)
REP={
 # stap 3: buitenlijn 1 px (opgeheven poot had onderrand 2 px zwart)
 'lijn': [((2,28),S),((3,28),S),((4,28),S),((5,28),S)],
 # stap 4: oog naar het model (lid, glans links, pupil 2 hoog, grijze iris, licht rechtsonder, creme onderrand)
 'oog': [((14,8),K),((11,9),W),((12,9),K),((13,9),GI),((14,9),GI),((11,10),GI),((12,10),K),((13,10),GI),((14,10),g_),((10,11),g_),((11,11),C)],
 # stap 4: neus is in het model een dicht donkerbruin vlak; de reductie liet er een middenbruine pixel in
 'neus': [((4,14),d)],
 # stap 4: teenlijnen die het model heeft en de vlakgemiddelde wegpoetste
 'tenen': [((20,41),S),((19,42),S),((19,43),S),((32,41),S),((32,42),S),((35,41),S),((35,42),S)],
 # stap 4: binnenspiraal van de schouder; modelcellen met >=40% donkere lijn (frac.py), hoeken rond gezet zodat het een krul blijft
 'spiraal': [((23,23),S),((24,23),S),((25,24),S),((22,24),S),((22,25),S),((23,26),S),((24,26),S),((24,25),S)],  # variant C van 4 (spv), leest het meest als spiraal
}
base=a.copy(); log={}
for zone,lst in REP.items():
    ch=0
    for (x,y),v in lst:
        if a[y,x]!=v: a[y,x]=v; ch+=1
    log[zone]=ch
print(log,'totaal',(a!=base).sum())
np.save('welp_r2_zonder_extra.npy',a); np.save('FIN2.npy',np.array(FIN))
