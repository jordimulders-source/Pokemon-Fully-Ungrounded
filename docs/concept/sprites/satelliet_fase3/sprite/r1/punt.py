# puntbemonstering: modelklasse in het midden van elk spritepixel (+ 4 subpunten op 1/4,3/4) -> meest voorkomend
from bouw import *
from collections import Counter
rows=[]
for y in range(OH):
    r=''
    for x in range(OUTW):
        c=Counter()
        for fy in (0.25,0.5,0.75):
            for fx in (0.25,0.5,0.75):
                mx=int(X0+(x+fx)*s); my=int(Y0+(y+fy)*s)
                c[lab[min(my,H-1),min(mx,W-1)]]+= 2 if (fx==0.5 and fy==0.5) else 1
        v=c.most_common(1)[0][0]
        r+='.' if v==0 else '0123456789abcdef'[v]
    rows.append(r)
open('punt.txt','w').write('\n'.join(rows)+'\n')
