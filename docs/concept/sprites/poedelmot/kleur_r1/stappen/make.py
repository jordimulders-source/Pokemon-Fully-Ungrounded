import sys, os
P=int(os.environ.get('P','6'))
sys.path.insert(0,'.')
from rows import build
from edits import E
g=build()
for x,y,c in E:
    if g[y][x]=='.': raise SystemExit(f'edit op transparant {x},{y}')
    if c.startswith('?'):
        if g[y][x]=='8': g[y][x]=c[1]
        continue
    g[y][x]=c
# --- sprietbaarden: 3 px lange schuine streken, zelfde ontwerp voor beide sprieten ---
def zone(x,y):
    if y<17 or y>29: return False
    if x<=20: return g[y][x] in '13456' and not (g[y][x]=='6' and y>=26)
    if 28<=x<=52: return g[y][x] in '13456' and not (x>=38 and y>=29)
    return False
Z={(x,y) for y in range(64) for x in range(64) if zone(x,y)}
RIB={(x,y) for (x,y) in Z if g[y][x] in '56' and ((x<=20 and y<=25) or (x>=29 and y<=28))}
def outline(x,y):
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        if (x+dx,y+dy) not in Z: return True
    return False
for (x,y) in sorted(Z):
    if (x,y) in RIB: continue
    if outline(x,y): g[y][x]='1'; continue
    light = (2*x - y) % P in (0,1,2)
    low = any((x,y+k) in Z and outline(x,y+k) and (x,y+k) not in RIB and y+k>=y for k in (1,)) and not any((x,y-k) in RIB for k in (1,2))
    g[y][x] = '4' if light else '1'
# baardstukjes die door rand/nerf korter dan 3 px werden: donker
seen=set()
for (x,y) in sorted(Z):
    if g[y][x]!='4' or (x,y) in seen: continue
    st=[(x,y)]; comp=[]; seen.add((x,y))
    while st:
        a,b=st.pop(); comp.append((a,b))
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            p=(a+dx,b+dy)
            if p in Z and p not in seen and g[p[1]][p[0]]=='4': seen.add(p); st.append(p)
    if len(comp)<3:
        for a,b in comp: g[b][a]='1'
open(sys.argv[1],'w').write('\n'.join(''.join(r) for r in g)+'\n')
