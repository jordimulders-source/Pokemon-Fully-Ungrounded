# r4: alleen B. Franjezoom zoals r2 (vulling vanaf rij 44 rood, D1 -> donkerrood), plus een paar strengen die 1-3 px omhoog
# uitschieten in het zwarte jurkvlak (Jordi over r3: "de franje mogen een paar pixels naar boven uitschieten zodat het er wat realistischer uit ziet").
# Alleen herkleuren binnen het r2-silhouet.
import numpy as np; from lib import I
R,R2=12,13
UIT={12:2,15:1,21:3,29:1,31:3,33:1}   # kolom: aantal pixels omhoog boven rij 44 (werkcoördinaten)
def varianten():
    o=np.load('tango_kls.npy'); b=o.copy(); poot=np.load('poot_mask.npy')
    VUL=[I['D2'],I['D3'],I['D4'],I['D5']]
    def kleur(y,x):
        if poot[y,x]: return 0
        if o[y,x]==I['D1']: b[y,x]=R2; return 1
        if o[y,x] in VUL: b[y,x]=R; return 1
        return 0
    for y in range(44,o.shape[0]):
        for x in range(o.shape[1]): kleur(y,x)
    n=0
    for x,k in UIT.items():
        for y in range(44-k,44): n+=kleur(y,x)
    print('uitschieters herkleurd:',n)
    return {'B':b}
