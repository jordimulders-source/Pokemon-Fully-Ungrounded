# vlam3.py: handvlam opnieuw uit het model. Silhouet: spritepixel is vuur als >=2 van de 4 natieve modelpixels figuur zijn
# en er minstens 1 vuur is (dezelfde regel als de rest van de sprite; r1/r2 telden vuur al vanaf 1 en zwollen op).
# Losse enkele pixels vallen weg. Banden: vuurhitte 4x4-venster (zoals r2). Hoofdvlam: rand rood, donkerrood waar de
# achtergrond rechts ligt; vonkjes (losse stukjes) krijgen alleen hun band, geen rand. Alleen vuur- en achtergrondpixels
# in de zone x5-13, y16-28 veranderen.
import numpy as np, sys
from collections import Counter
FIRE=set('YAOrR')
src,dst=sys.argv[1],sys.argv[2]
X0,Y0,X1,Y1=[int(v) for v in sys.argv[3:7]] if len(sys.argv)>6 else (5,16,13,28)
R=[list(r.rstrip('\n')) for r in open(src)]
R0=[r[:] for r in R]
K=np.load('natief_klas.npy')
HEAT={13:4,8:4,12:3,11:2,14:2,10:1,9:0}
BAND={4:'Y',3:'A',2:'O',1:'r',0:'R'}
def cel(sx,sy):
    nx=62+(sx-4)*2; ny=6+(sy-5)*2; return K[ny:ny+2,nx:nx+2].ravel()
def heat(sx,sy):
    nx=62+(sx-4)*2; ny=6+(sy-5)*2
    h=[HEAT[k] for k in K[ny-1:ny+3,nx-1:nx+3].ravel() if k in HEAT]
    return np.mean(h) if h else 2
Z=[(x,y) for y in range(Y0,Y1+1) for x in range(X0,X1+1) if R[y][x] in FIRE or R[y][x]=='.']
fig=set()
for x,y in Z:
    f=cel(x,y)
    if (f>0).sum()>=2 and any(k in HEAT for k in f): fig.add((x,y))
# componenten (4-buren, binnen de vuurpixels)
def comps(s):
    s=set(s); out=[]
    while s:
        p=s.pop(); c=[p]; st=[p]
        while st:
            a,b=st.pop()
            for q in ((a+1,b),(a-1,b),(a,b+1),(a,b-1)):
                if q in s: s.remove(q); st.append(q); c.append(q)
        out.append(c)
    return out
cs=sorted(comps(fig),key=len,reverse=True)
weg=[c for c in cs if len(c)==1]; cs=[c for c in cs if len(c)>1]
hoofd=set(cs[0]); vonk=[c for c in cs[1:]]
for x,y in Z: R[y][x]='.'
new={}
for x,y in fig-set(p for c in weg for p in c):
    new[(x,y)]=BAND[int(np.clip(np.floor(heat(x,y)+0.5),0,4))]
# vlekjes <3 px in de hoofdvlam opgaan
for it in range(3):
    for c in comps([p for p in hoofd]):
        pass
    seen=set()
    for p in hoofd:
        if p in seen: continue
        c=[p]; st=[p]; seen.add(p)
        while st:
            a,b=st.pop()
            for q in ((a+1,b),(a-1,b),(a,b+1),(a,b-1)):
                if q in hoofd and q not in seen and new[q]==new[p]: seen.add(q); st.append(q); c.append(q)
        if len(c)>=3: continue
        nb=Counter(new[q] for a,b in c for q in ((a+1,b),(a-1,b),(a,b+1),(a,b-1)) if q in hoofd and new[q]!=new[p])
        if nb:
            for q in c: new[q]=nb.most_common(1)[0][0]
for (x,y),v in new.items(): R[y][x]=v
for x,y in hoofd:
    if any(R[y+dy][x+dx]=='.' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))):
        R[y][x]='R' if R[y][x+1]=='.' else 'r'
# vonk: één band per vonk (meest voorkomende), zodat er geen 1-px-tintjes in zitten
BEHOUD={(9,17),(9,18),(10,18)}  # vonkjes boven de handvlam: kleuren van r2 blijven
for c in vonk:
    if set(c)<=BEHOUD:
        for x,y in c: R[y][x]=R0[y][x]
        continue
    b=Counter(new[p] for p in c).most_common(1)[0][0]
    for x,y in c: R[y][x]=b
open(dst,'w').write('\n'.join(''.join(r) for r in R)+'\n')
print('hoofdvlam',len(hoofd),'vonken',[sorted(c) for c in vonk],'weg (1 px)',weg)
for y in range(Y0,Y1+1): print(y,''.join(R[y][X0-2:X1+2]))
