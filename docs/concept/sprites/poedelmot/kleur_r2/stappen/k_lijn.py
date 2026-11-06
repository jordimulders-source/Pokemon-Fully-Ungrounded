# buitenlijn: lichtkant (normaal naar links/boven) selout 4, schaduwkant 2; sprieten (al 1) en ogen blijven
import math
op=lambda x,y: 0<=x<64 and 0<=y<64 and r[y][x]!='.'
for y in range(64):
    for x in range(64):
        if not op(x,y) or r[y][x] not in '56789AC': continue
        if all(op(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): continue
        nx=ny=0
        for dy in range(-2,3):
            for dx in range(-2,3):
                if (dx or dy) and not op(x+dx,y+dy): nx+=dx; ny+=dy
        # licht van linksboven: (-1,-1)
        d=(-nx-ny)/max(1e-6,math.hypot(nx,ny))
        r[y][x]='4' if d>0.35 else '2'
