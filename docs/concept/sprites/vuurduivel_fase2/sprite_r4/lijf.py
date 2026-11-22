# lijf.py: tintverdeling romp + bovenarm (x18-46, y29-43) naar de modelhelderheid. Alleen pixels die in r3 lijfgrijs zijn
# (d/g) veranderen; omlijning, plooien (#), manen en benen blijven. Helderheid per spritepixel = gemiddelde luminantie van
# de natieve modelpixels in een 4x4-venster rond de 2x2-cel, alleen lijfklassen, zonder lijnpixels (lum <= 8).
import numpy as np, sys; from PIL import Image
from collections import Counter
n=np.asarray(Image.open('natief.png')).astype(float); L=n@[0.3,0.59,0.11]
K=np.load('natief_klas.npy')
R=[list(r.rstrip('\n')) for r in open(sys.argv[1])]
X0,Y0,X1,Y1=18,29,46,43
def lum(x,y,w=1):
    nx=62+(x-4)*2; ny=6+(y-5)*2
    blk=L[ny-w:ny+2+w,nx-w:nx+2+w].ravel(); k=K[ny-w:ny+2+w,nx-w:nx+2+w].ravel()
    v=blk[np.isin(k,[1,2,3])&(blk>8)]
    return v.mean() if len(v) else None
cel=[(x,y) for y in range(Y0,Y1+1) for x in range(X0,X1+1) if R[y][x] in 'dg']
lv={p:lum(*p) for p in cel}
if '--toon' in sys.argv:
    for y in range(Y0,Y1+1): print(y,' '.join(('%2d'%lv[(x,y)] if lv.get((x,y)) is not None else ' '+R[y][x]) for x in range(X0,X1+1)))
    sys.exit()
T1=float(sys.argv[3]) if len(sys.argv)>3 else 26   # >= T1 -> middentint g, anders donker d
T2=float(sys.argv[4]) if len(sys.argv)>4 else 99   # >= T2 binnen de schouderzone -> licht L
SCH=lambda x,y: 18<=x<=24 and 32<=y<=37
new={}
for p in cel:
    l=lv[p]
    if l is None: new[p]=R[p[1]][p[0]]; continue
    new[p]='L' if (l>=T2 and SCH(*p)) else ('g' if l>=T1 else 'd')
# vlekjes < 3 px opgaan in de meest voorkomende buurtint (binnen de lijfpixels)
for it in range(4):
    seen=set()
    for p in cel:
        if p in seen: continue
        c=[p]; st=[p]; seen.add(p)
        while st:
            a,b=st.pop()
            for q in ((a+1,b),(a-1,b),(a,b+1),(a,b-1)):
                if q in new and q not in seen and new[q]==new[p]: seen.add(q); st.append(q); c.append(q)
        if len(c)>=3: continue
        nb=Counter(new[q] for a,b in c for q in ((a+1,b),(a-1,b),(a,b+1),(a,b-1)) if q in new and new[q]!=new[p])
        if nb:
            for q in c: new[q]=nb.most_common(1)[0][0]
for (x,y),v in new.items(): R[y][x]=v
open(sys.argv[2],'w').write('\n'.join(''.join(r) for r in R)+'\n')
for y in range(Y0-1,Y1+2): print('%2d %s'%(y,''.join(R[y][X0-2:X1+2])))
