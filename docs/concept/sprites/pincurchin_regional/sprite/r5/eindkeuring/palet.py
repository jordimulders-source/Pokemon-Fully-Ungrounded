# Palet + luminantie + gebruik + aandeel op de buitenrand, per sprite (bovenste 64x64)
import sys
from PIL import Image
from collections import Counter
for p in sys.argv[1:]:
    im=Image.open(p); pal=im.getpalette()
    g=[[im.getpixel((x,y)) for x in range(64)] for y in range(64)]
    use=Counter(v for r in g for v in r); edge=Counter()
    for y in range(64):
        for x in range(64):
            if g[y][x] and any((0<=x+a<64 and 0<=y+b<64 and g[y+b][x+a]==0) for a,b in((1,0),(-1,0),(0,1),(0,-1))): edge[g[y][x]]+=1
    print(p.split('/')[-2] if 'graphics' in p else p.split('/')[-1])
    for i in sorted(use):
        if i==0: continue
        r,gg,b=pal[3*i:3*i+3]; print('  %2d (%3d,%3d,%3d) L%3d n%4d rand%3d'%(i,r,gg,b,round(.299*r+.587*gg+.114*b),use[i],edge[i]))
