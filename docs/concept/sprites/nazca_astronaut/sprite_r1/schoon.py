# Technisch opschonen van de kale reductie: buitenlijn 1 px, ogen per pixel uit het model (5x5), rest ongemoeid.
# Uitvoer: schoon.txt (klassen) + telling per zone t.o.v. kaal.
import numpy as np
from reduceer import reduceer
g=reduceer('n_edit.png',0,0.5); kaal=g.copy(); H,W=g.shape
bg=(g=='.')
def nb(j,i):
    return [(j+dy,i+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
def isbg(j,i): return not(0<=j<H and 0<=i<W) or bg[j,i]
# 1. buitenlijn: elke figuurpixel naast achtergrond wordt lijn (klasse K); de kleur (zwart/selout) volgt bij het kleuren
for j in range(H):
    for i in range(W):
        if not bg[j,i] and any(isbg(y,x) for y,x in nb(j,i)): g[j,i]='K'
# 2. ogen: modeloog (wit cirkel, blauwe cirkel, wit midden) 7x7 natief -> 5x5
oog=[".WWW.","WbbbW","WBWbW","WBbbW",".WWW."]
for (j0,i0) in ((8,9),(8,19)):
    for dy,r in enumerate(oog):
        for dx,ch in enumerate(r):
            g[j0+dy,i0+dx]= 'K' if ch=='.' else ch
# 2b. losse witte/blauwe resten van de reductie rond de ogen (buiten de 5x5-ogen) -> kopvlak
for j in range(0,20):
    for i in range(7,W):
        inoog=any(j0<=j<j0+5 and i0<=i<i0+5 for j0,i0 in ((8,9),(8,19)))
        if not inoog and g[j,i] in 'WBb': g[j,i]='K'
# 3. kop: K binnen de kop (niet aan de rand) = kopvlak 'k'
for j in range(0,20):
    for i in range(W):
        if g[j,i]=='K' and not any(isbg(y,x) for y,x in nb(j,i)) and i>=7: g[j,i]='k'
open('schoon.txt','w').write('\n'.join(''.join(r) for r in g))
np.save('kaal.npy',kaal); np.save('schoon.npy',g)
d=(g!=kaal); print('afwijkend van kaal:',d.sum())
for naam,(a,b) in {'kop+ogen (rij 0-19)':(0,20),'romp/armen (20-47)':(20,48),'benen/voeten (48-)':(48,H)}.items():
    print(naam,d[a:b].sum())
for j,r in enumerate(g): print('%2d '%j+''.join(r))
