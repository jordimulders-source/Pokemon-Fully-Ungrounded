# lijnen van het model 1-op-1: kop/masker, bontkraag, vleugels, poten (lijnenkaart van samengesteld.png)
import numpy as np
from collections import Counter
M=np.load('modellijnen.npy')
Z=set(tuple(map(int,l.split(','))) for l in open('spriet_zone.txt'))
OOG={(x,y) for y in range(31,42) for x in range(13,35) if r[y][x] in '12B'}
def binnen(x,y): return all(r[y+dy][x+dx]!='.' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
KLAUW_Y=55
for y in range(26,48):          # poten (y>=48) niet: de lijnenkaart is daar te rommelig
    for x in range(4,63):
        if r[y][x]=='.' or (x,y) in Z or (x,y) in OOG or not binnen(x,y): continue
        if y>=KLAUW_Y and r[y][x] in '23': continue
        if M[y,x]>0.30:
            r[y][x]='3'
        elif M[y,x]<0.12 and r[y][x] in '234' and y>=30 and x<40 and not (y in (41,42) and 18<=x<=28):
            c=Counter(r[y+dy][x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if r[y+dy][x+dx] in '67A')
            if c: r[y][x]=c.most_common(1)[0][0]
