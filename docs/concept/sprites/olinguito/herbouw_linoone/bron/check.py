"""Controles: open randen, formaat, box, rechte runs in de omtrek."""
import sys
sys.path.insert(0,'/home/user/projectgrounded/docs/concept/sprites/olinguito/herbouw_linoone/bron')
from render import load
rows=load(sys.argv[1])
g=lambda x,y: rows[y][x] if 0<=y<64 and 0<=x<64 else '.'
OUT=set('129')
open_=[]
px=0; xs=[];ys=[]
for y in range(64):
    for x in range(64):
        c=g(x,y)
        if c=='.': continue
        px+=1; xs.append(x); ys.append(y)
        if any(g(x+dx,y+dy)=='.' for dx,dy in((1,0),(-1,0),(0,1),(0,-1))) and c not in OUT:
            open_.append((x,y,c))
print('px',px,'box',max(xs)-min(xs)+1,'x',max(ys)-min(ys)+1, 'x',min(xs),max(xs),'y',min(ys),max(ys))
print('open randen',len(open_),open_[:40])
# rechte runs in de silhouetomtrek (verticaal/horizontaal) >= 4
edge=lambda x,y: g(x,y)!='.' and any(g(x+dx,y+dy)=='.' for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
runs=[]
for y in range(64):
    # linkerrand/rechterrand-pixels per kolom: verticale runs
    pass
for x in range(64):
    for side in (-1,1):
        run=0
        for y in range(65):
            e = y<64 and g(x,y)!='.' and g(x+side,y)=='.'
            if e: run+=1
            else:
                if run>=4: runs.append(('vert',x,y-run,y-1,'L' if side<0 else 'R'))
                run=0
for y in range(64):
    for side in (-1,1):
        run=0
        for x in range(65):
            e = x<64 and g(x,y)!='.' and g(x,y+side)=='.'
            if e: run+=1
            else:
                if run>=4: runs.append(('hor',y,x-run,x-1,'boven' if side<0 else 'onder'))
                run=0
print('rechte runs >=4 in silhouet:')
for r in runs: print('  ',r)
