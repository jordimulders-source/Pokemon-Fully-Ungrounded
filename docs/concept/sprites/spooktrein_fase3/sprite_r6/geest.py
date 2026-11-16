# Stap 3: schone geest ±1,1x opschalen door rijen/kolommen te dupliceren in egale stukken (nooit tekenen),
# en op r4 zetten. Uitvoer: sprite_r6/stap_geest.png (r4 + nieuwe geest).
from PIL import Image; import numpy as np
rows=[l.rstrip('\n') for l in open('sprite_r6/geest_schoon.txt')]
R0=6
DUPR=[14]          # natieve rij midden in de mond: mond +1 hoog
DROPR=[19,21]      # r19 lijkt op r18/r20 (schrappen, lijf 1 rij korter); r21 = steel, valt in de schoorsteenopening
DUPC=[5,12,23]     # kolommen (i=x-29): linkerkwab, mond+rechteroog, arm
g=[]
for r,line in enumerate(rows):
    line=line[:21-0] if False else line
    row=[]
    for i,ch in enumerate(line):
        row.append(ch)
        if i in DUPC: row.append(ch)
    g.append(row)
    if r+R0 in DROPR: g.pop(); continue
    if r+R0 in DUPR: g.append(row[:])
open('sprite_r6/geest_groot.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
s=Image.open('sprite_r4/sprite.png'); pal=s.getpalette(); a=np.array(s)
pal[13*3:13*3+3]=[232,248,232]
GROEN={2,3,4,5,6}; IDX={'6':6,'5':5,'2':2,'W':13}
for y in range(0,15):
    for x in range(0,44):
        if a[y,x] in GROEN: a[y,x]=0
DX=14
for y,row in enumerate(g):
    for i,ch in enumerate(row):
        if ch not in IDX: continue
        x=i+DX
        if y>=16 and a[y,x] in GROEN: continue   # bevroren wolk wint
        a[y,x]=IDX[ch]
o=Image.fromarray(a.astype('uint8'),'P'); o.putpalette(pal); o.save('sprite_r6/stap_geest.png',transparency=0)
print(len(g),'rijen x',len(g[0]),'kolommen')
