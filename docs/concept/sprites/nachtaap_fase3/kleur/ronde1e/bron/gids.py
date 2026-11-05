"""Gids (alleen als hulp): 4 vachttinten uit de helderheid van de onderlaag per 64-pixel, voor de zones benen/armen/onderlijf.
Uitvoer: gids.txt (raster met de gids in de zones, rest = huidige sprite)."""
import os
import numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); B=os.path.join(H,'../../..')
o=np.array(Image.open(os.path.join(B,'silhouet/onderlaag_256.png')).convert('RGBA')).astype(float)
lum=(0.3*o[:,:,0]+0.59*o[:,:,1]+0.11*o[:,:,2]).reshape(64,4,64,4).mean(axis=(1,3))
g=[list(l.rstrip('\n')) for l in open(os.path.join(H,'../raster.txt'))]
def zone(x,y):
    if x>=37 and y<=38: return None      # staart (bevroren)
    if x>=44 and y<=41: return None
    if y<=21 and x<=12: return None       # vuist (1c)
    if x<=20 and y>=26: return None       # kop, hand, gloed
    if x<=22 and y>=45: return None
    if 21<=x<=24 and y>=46: return 'healerarm'
    if x<=21 and y<=31: return 'vuistarm'
    if y<=36 and 23<=x<=36: return 'been boven'
    if x>=32 and y>=38: return 'been onder'
    return 'romp'
P=lambda x,y: g[y][x] if 0<=x<64 and 0<=y<64 else '.'
pts=[(x,y) for y in range(64) for x in range(64) if g[y][x] in 'LVSD' and zone(x,y)
     and not (g[y][x]=='D' and any(P(x+dx,y+dy)=='.' for dx,dy in((1,0),(-1,0),(0,1),(0,-1))))]
v=np.array([lum[y,x] for x,y in pts]); q=np.quantile(v,[0.18,0.55,0.88])
for (x,y),l in zip(pts,v): g[y][x]='D' if l<q[0] else 'S' if l<q[1] else 'V' if l<q[2] else 'L'
open(os.path.join(H,'gids.txt'),'w').write('\n'.join(''.join(r) for r in g)+'\n')
print(len(pts),q)
