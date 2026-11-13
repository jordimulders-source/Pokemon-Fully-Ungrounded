# r2/rand.py : loopt de buitencontour na. Per randpixel: bloot naar boven/links (lichtkant) -> verwacht 2, bloot naar onder/rechts -> verwacht 1.
# kaart: 'o' = klopt, 'Z' = zwart op zuivere lichtkant, 'R' = donkerrood op schaduwkant, 'L' = lichte kleur op de rand; daarna losse tintpixels en 6-pixels
import sys; sys.path.insert(0,'.')
import cfg,numpy as np
a=cfg.read('r3/raster.txt'); P=np.pad(a,1); M=[['.' if a[y,x]==0 else ' ' for x in range(64)] for y in range(64)]
n={'Z':0,'R':0,'L':0,'o':0}
for y in range(64):
    for x in range(64):
        v=a[y,x]
        if not v: continue
        up=P[y,x+1]==0; dn=P[y+2,x+1]==0; lf=P[y+1,x]==0; rt=P[y+1,x+2]==0
        if not(up or dn or lf or rt): continue
        if v not in (1,2,12): k='L'
        elif v==1 and (up or lf) and not (dn or rt): k='Z'
        elif v==2 and (dn or rt): k='R'
        else: k='o'
        n[k]+=1; M[y][x]=k
print('    '+''.join(str(x%10) for x in range(64)))
for y in range(64):
    if any(c not in '. ' for c in M[y]): print('%3d '%y+''.join(M[y]))
print(n)
iso=[(x,y,cfg.CH[a[y,x]]) for y in range(64) for x in range(64) if a[y,x] in (3,4,5,6,7,8) and a[y,x] not in (P[y,x+1],P[y+2,x+1],P[y+1,x],P[y+1,x+2])]
print('losse tintpixels',len(iso),iso)
print('6:',[(x,y) for y in range(64) for x in range(64) if a[y,x]==6])
