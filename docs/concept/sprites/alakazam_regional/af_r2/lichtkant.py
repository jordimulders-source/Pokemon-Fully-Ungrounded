# lichtkant.py raster: aandeel zwarte omlijning (o) aan de lichtkant.
# Lichtkant-rand = randpixel met een transparante buur links of boven (licht linksboven), zonder transparante buur rechts of onder.
import sys,pal
R=pal.load(sys.argv[1]); T=lambda x,y: not(0<=x<64 and 0<=y<64) or R[y][x]=='.'
lk=[(x,y) for y in range(64) for x in range(64) if R[y][x]!='.' and (T(x-1,y) or T(x,y-1)) and not (T(x+1,y) or T(x,y+1))]
o=[p for p in lk if R[p[1]][p[0]]=='o']
print(f'lichtkant {len(lk)} px, waarvan o {len(o)} = {100*len(o)/len(lk):.0f}%')
if len(sys.argv)>2: print('o aan de lichtkant:',o)
