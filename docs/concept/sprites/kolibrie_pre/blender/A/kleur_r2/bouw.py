"""rijen.txt (y x0 tekens) -> raster.txt; controle tegen het bevroren silhouet."""
import sys
H="/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/"
g=[['.']*64 for _ in range(64)]
for l in open('rijen.txt'):
    if not l.strip(): continue
    y,x,s=l.split(); y=int(y); x=int(x)
    for i,c in enumerate(s):
        assert g[y][x+i]=='.', (y,x+i)
        g[y][x+i]=c
open('raster.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
