# controles: kleuren, tintvlakjes <3 px, open buitenlijn, losse lijnpixels midden in een vlak, zwart/selout om en om
import sys, numpy as np
from PIL import Image
for f in sys.argv[1:]:
    im=Image.open(f); a=np.array(im); H,W=a.shape
    print(f, im.mode, im.size, 'transp', im.info.get('transparency'), 'kleuren', len(np.unique(a)))
    op=a!=0
    # buitenlijn: randpixels moeten index 1 (zwart) of 2 (selout) of tand/wit zijn
    bad=[]
    for y in range(H):
        for x in range(W):
            if not op[y,x]: continue
            if any(not(0<=x+dx<W and 0<=y+dy<H) or not op[y+dy,x+dx] for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):
                if a[y,x] not in (1,2,8,12,13,14): bad.append((x,y,int(a[y,x])))
    print(' open buitenlijn:', bad)
    # clusters <3 px per index (behalve 0,1,2 lijn en oog/tand)
    seen=np.zeros_like(op); small=[]
    for y in range(H):
        for x in range(W):
            if seen[y,x] or not op[y,x]: continue
            v=a[y,x]; st=[(x,y)]; seen[y,x]=1; comp=[]
            while st:
                cx,cy=st.pop(); comp.append((cx,cy))
                for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=cx+dx,cy+dy
                    if 0<=nx<W and 0<=ny<H and not seen[ny,nx] and a[ny,nx]==v: seen[ny,nx]=1; st.append((nx,ny))
            if len(comp)<3 and v not in (1,2,8): small.append((int(v),[(p[0]-9,p[1]-26) for p in comp]))
    print(' tintvlakjes <3 px (figuurcoörd):', small)
    # losse zwarte pixel zonder zwarte/selout-buur en niet aan de rand
    lone=[]
    for y in range(1,H-1):
        for x in range(1,W-1):
            if a[y,x]==1 and all(op[y+dy,x+dx] for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):
                if not any(a[y+dy,x+dx] in (1,2,8) for dx in(-1,0,1) for dy in(-1,0,1) if dx or dy): lone.append((x-9,y-26))
    print(' losse lijnpixels:', lone)
    rand=[a[y,x] for y in range(H) for x in range(W) if op[y,x] and any(not op[y+dy,x+dx] for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
    print(' rand zwart %.0f%%, selout %.0f%%'%(100*rand.count(1)/len(rand),100*rand.count(2)/len(rand)))
