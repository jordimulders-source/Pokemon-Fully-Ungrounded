# rand.py raster : buitenrandpixels (grenzen aan transparant, 4-buren) die geen lijn- of seloutkleur (1,2,3,5,6,8,D,F) zijn
import sys
from tl import *
R=raster(sys.argv[1]); bad=[]
for y in range(64):
  for x in range(64):
    c=R[y][x]
    if c=='.': continue
    edge=any(not(0<=x+dx<64 and 0<=y+dy<64) or R[y+dy][x+dx]=='.' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
    if edge and c not in '12356 8DF'.replace(' ',''): bad.append((x,y,c))
print(len(bad),bad)
