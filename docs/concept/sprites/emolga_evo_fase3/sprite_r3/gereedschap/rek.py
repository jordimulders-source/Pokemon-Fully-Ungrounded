# rek.py: meet per modelrij hoe het lijf in model.png uit r6 is opgerekt (x' = c + (x-c)/s), zodat elke modelpixel naar zijn
# r6-bron (en dus natieve cel) terug kan. De rek loopt boven en onder af (s 1,04 -> 1,25 -> 1,04) en het centrum schuift per rij.
# Uitvoer: rek.npy (1024x2: s, c per rij; rij zonder rek: s=1).
import numpy as np; from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/'
m=np.asarray(Image.open(D+'model/model.png').convert('L')).astype(float)
r=np.asarray(Image.open(D+'gemini/r6.png').convert('L')).astype(float)
xs=np.arange(280,780); X=np.arange(1024)
out=np.zeros((1024,2)); out[:,0]=1; out[:,1]=530
for y in range(70,700):
    if np.abs(m[y]-r[y]).max()<30: continue
    best=(1e18,1,530)
    for s in np.arange(1.0,1.30,0.01):
        for c in np.arange(440,620,2.0):
            e=np.abs(np.interp(c+(xs-c)/s,X,r[y])-m[y,xs]).mean()
            if e<best[0]: best=(e,s,c)
    # verfijnen
    e0,s0,c0=best
    for s in np.arange(s0-0.01,s0+0.0101,0.0025):
        for c in np.arange(c0-2,c0+2.01,0.5):
            e=np.abs(np.interp(c+(xs-c)/s,X,r[y])-m[y,xs]).mean()
            if e<best[0]: best=(e,s,c)
    out[y]=best[1:]
np.save(D+'sprite_r1/gereedschap/rek.npy',out)
for y in range(70,700,25): print(y,out[y].round(3))
