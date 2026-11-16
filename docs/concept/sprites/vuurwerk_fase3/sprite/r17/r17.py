# Opschoning na eindkeuring r12/r16 (keurder bevindingen 1, 2, 4); basis r16 sprite_B (Jordi's keuze).
from PIL import Image
import numpy as np
from collections import Counter
src=Image.open('../r16/sprite_B.png'); a=np.array(src); pal=src.getpalette(); a0=a.copy()
for (x,y) in [(36,7),(39,9),(27,21),(58,19)]: assert a[y,x]==6; a[y,x]=1      # 1: één lijnkleur per rand
assert a[33,20]==8; a[33,20]=6                                                  # 2: rand dicht
for (x,y) in [(28,8),(28,11),(40,15),(21,34),(38,34)]:                         # 4: glitterrest weg (Jordi: "die glitterspikkels kan je wegdoen")
    nb=[a0[y+dy,x+dx] for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)] if a0[y+dy,x+dx]!=a0[y,x]]
    a[y,x]=Counter(nb).most_common(1)[0][0]
print('gewijzigd',len(np.argwhere(a!=a0)))
im=Image.fromarray(a,'P'); im.putpalette(pal); im.save('sprite.png',transparency=0)
