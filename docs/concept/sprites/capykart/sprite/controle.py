# controle: kleuren, tintvlakjes <3 px, losse lijnpixels midden in een vlak, A/B pixel-identiek
import sys,json
from collections import Counter
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capykart/sprite/r1/'
ga=json.load(open(R+'grid_A.json'))['grid']; gb=json.load(open(R+'grid_B.json'))['grid']
print('A==B (indices):',ga==gb)
g=ga; H,W=len(g),len(g[0])
print('kleuren incl. transparant:',len(set(''.join(g))),sorted(set(''.join(g))))
seen=set(); small=[]
for y in range(H):
    for x in range(W):
        if (x,y) in seen or g[y][x] in '.0sW': continue
        v=g[y][x]; st=[(x,y)]; seen.add((x,y)); c=[]
        while st:
            cx,cy=st.pop(); c.append((cx,cy))
            for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                nx,ny=cx+dx,cy+dy
                if 0<=nx<W and 0<=ny<H and (nx,ny) not in seen and g[ny][nx]==v: seen.add((nx,ny)); st.append((nx,ny))
        if len(c)<3: small.append((v,c))
print('tintvlakjes <3 px:',len(small),small)
def op(x,y): return 0<=x<W and 0<=y<H and g[y][x]!='.'
lone=[(x,y) for y in range(H) for x in range(W) if g[y][x]=='0' and all(op(x+dx,y+dy) and g[y+dy][x+dx] not in '0s' for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
print('losse zwarte pixels zonder lijnbuur:',lone)
open_edge=[(x,y) for y in range(H) for x in range(W) if g[y][x] not in '.0sW' and any(not op(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
print('open randen (lichte kleur op buitenrand):',open_edge)
