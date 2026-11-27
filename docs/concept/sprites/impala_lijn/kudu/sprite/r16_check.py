# Controle r16: (1) alleen tintwissels binnen vachtvlakken, (2) rechte tintgrenzen die r16 nieuw maakt, (3) losse pixels.
import numpy as np
from PIL import Image
g0=np.load('r15/grid.npy').astype(str); i0=np.array(Image.open('r15/kudu_r15.png'))
out=[]
VACHT=set('MLDH')
for v in 'AB':
    g=np.load(f'r16/grid{v}.npy').astype(str); i1=np.array(Image.open(f'r16/kudu_r16{v}.png'))
    d=np.argwhere(g!=g0)
    out.append(f'== {v}: {len(d)} pixels veranderd')
    bad=[(x,y,g0[y,x],g[y,x]) for y,x in d if not (g0[y,x]=='M' and g[y,x] in 'HLD')]
    out.append(f'  wissels die niet M->H/L/D zijn: {len(bad)} {bad[:5]}')
    out.append(f'  silhouet (transparant) anders: {int(((i0==0)!=(i1==0)).sum())} px')
    niet=[(x,y) for y,x in d if g0[y,x] not in VACHT]
    out.append(f'  pixels buiten vacht (lijn/strepen/oog/manen/hoorn/oor) aangeraakt: {len(niet)}')
    oog=sum(1 for y,x in d if 15<=x<=19 and 21<=y<=24); neus=sum(1 for y,x in d if 8<=x<=12 and 23<=y<=29)
    out.append(f'  oog K4 (x15-19 y21-24): {oog} px, neus/mond (x8-12 y23-29): {neus} px')
    # letters -> index consistent met r15 voor ongewijzigde pixels
    same=(g==g0); out.append(f'  index ongewijzigde pixels gelijk: {bool((i0[same]==i1[same]).all())}')
    # rechte grenzen: horizontale/verticale grens tussen twee verschillende vachttinten, waarvan minstens een kant nieuw
    nieuw=(g!=g0); runs=[]
    for y in range(63):   # grens tussen rij y en y+1
        x=0
        while x<64:
            def grens(x): return g[y,x] in VACHT and g[y+1,x] in VACHT and g[y,x]!=g[y+1,x] and (nieuw[y,x] or nieuw[y+1,x])
            if grens(x):
                s=x
                while x<64 and grens(x) and g[y,x]==g[y,s] and g[y+1,x]==g[y+1,s]: x+=1
                if x-s>=4: runs.append(('hor',y,s,x-1,str(g[y,s]),str(g[y+1,s])))
            else: x+=1
    for x in range(63):
        y=0
        while y<64:
            def grens(y): return g[y,x] in VACHT and g[y,x+1] in VACHT and g[y,x]!=g[y,x+1] and (nieuw[y,x] or nieuw[y,x+1])
            if grens(y):
                s=y
                while y<64 and grens(y) and g[s,x]==g[y,x] and g[s,x+1]==g[y,x+1]: y+=1
                if y-s>=4: runs.append(('ver',x,s,y-1,str(g[s,x]),str(g[s,x+1])))
            else: y+=1
    out.append(f'  nieuwe rechte tintgrenzen >= 4 px: {len(runs)} {runs}')
    los=[(int(x),int(y),str(g[y,x])) for y,x in d if not any(g[y+dy,x+dx]==g[y,x] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)))]
    out.append(f'  losse nieuwe pixels (geen gelijke buur, ook diagonaal): {los}')
    from collections import Counter
    out.append('  per tint nieuw: '+str(dict(Counter(str(g[y,x]) for y,x in d))))
    out.append('  vachttellingen r15 -> r16: '+str({t:(int((g0==t).sum()),int((g==t).sum())) for t in 'LHMD'}))
open('r16/telling.txt','w').write('\n'.join(out)+'\n'); print('\n'.join(out))
