# Technisch opschonen: tintclusters < 3 px (4-buren, zelfde index) binnen hout/vacht -> meest voorkomende buurtint uit dezelfde groep.
from collections import Counter
ZONE=hout.copy()   # vacht = r15b-tinten, niet opschonen
for (x,y) in FACE: ZONE[y,x]=False
for y in range(64):
    for x in range(64):
        if ZONE[y,x] and kop[y,x] and 0 in nb4(src,x,y): ZONE[y,x]=False   # buitenrand kop niet
OPS=[]
for it in range(4):
    seen=np.zeros((64,64),bool); n=0
    for y in range(64):
        for x in range(64):
            if not ZONE[y,x] or seen[y,x]: continue
            v=G[y,x]; comp=[(x,y)]; seen[y,x]=True; i=0
            while i<len(comp):
                cx,cy=comp[i]; i+=1
                for a,b in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=cx+a,cy+b
                    if ZONE[ny,nx] and not seen[ny,nx] and G[ny,nx]==v: seen[ny,nx]=True; comp.append((nx,ny))
            if len(comp)<3:
                c=Counter(G[cy+b,cx+a] for cx,cy in comp for a,b in ((1,0),(-1,0),(0,1),(0,-1)) if ZONE[cy+b,cx+a] and G[cy+b,cx+a]!=v)
                if c:
                    nv=c.most_common(1)[0][0]
                    for cx,cy in comp: OPS.append((cx,cy,int(v),int(nv))); G[cy,cx]=nv
                    n+=1
    if n==0: break
# Dubbele lijn langs de hoepels: houtpixel 4 naast een hoepellijn (1 die aan band 8 grenst) krijgt de meest voorkomende
# niet-4 houttint uit zijn 8-buren (de hoepel heeft zelf al een lijn van 1 px; het model zet zijn eigen hoepellijn iets anders).
hooplijn=np.zeros((64,64),bool)
for y in range(1,63):
    for x in range(1,63):
        if G[y,x]==1 and any(G[y+b,x+a]==8 for a in (-1,0,1) for b in (-1,0,1)): hooplijn[y,x]=True
HOOPOPS=[]
for y,x in zip(*np.nonzero(hout)):
    if G[y,x]==4 and any(hooplijn[y+b,x+a] for a,b in ((1,0),(-1,0),(0,1),(0,-1))):
        c=Counter(G[y+b,x+a] for a in (-1,0,1) for b in (-1,0,1) if hout[y+b,x+a] and G[y+b,x+a] in (5,6,13))
        if c: nv=c.most_common(1)[0][0]; HOOPOPS.append((x,y,4,int(nv))); G[y,x]=nv
