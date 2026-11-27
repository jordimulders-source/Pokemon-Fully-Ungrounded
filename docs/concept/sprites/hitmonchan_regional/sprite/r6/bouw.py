# r6: technisch opschonen van r5 (7-kleurenpalet: 1 lijn, 2-6 ijs donker->licht, 7 wit/glans). Geen nieuwe tinten, geen vormwijziging.
# A ontkorrelen: vultintpixel (2-6) die in zijn kleur een 4-cluster van 1 px is en niet in een diagonale keten (8-buren, >=3) ligt
#   -> meest voorkomende kleur van zijn 4-buren (gelijkspel: 8-buren), alleen als dat ook een vultint is. Rand- en oogzonepixels blijven.
# B buitenlijn-tint: randpixel met lichte tint (>=5): lichtkant (achtergrond boven/links) -> M_donker als die 2-4 is, anders 4
#   (de selout-tint van het model); schaduwkant -> 1 als M_donker <=2, anders M_donker.
import numpy as np, sys
from collections import Counter
D='docs/concept/sprites/hitmonchan_regional/sprite/'
sys.path.insert(0,D); from toon import save_idx, save_p64
S=np.load(D+'r5/idx.npy'); Dk=np.load(D+'M_donker.npy'); pal=eval(open(D+'pal.txt').read()); H,W=S.shape
OOG=lambda y,x: 18<=y<=25 and 21<=x<=30
def keten(S,y,x):
    c=S[y,x]; seen={(y,x)}; st=[(y,x)]
    while st and len(seen)<3:
        a,b=st.pop()
        for da in (-1,0,1):
            for db in (-1,0,1):
                u,v=a+da,b+db
                if 0<=u<H and 0<=v<W and (u,v) not in seen and S[u,v]==c: seen.add((u,v)); st.append((u,v))
    return len(seen)>=3
T=S.copy(); log=[]
for y in range(H):
    for x in range(W):
        c=S[y,x]
        if not (2<=c<=6) or OOG(y,x): continue
        n4=[S[u,v] for u,v in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)) if 0<=u<H and 0<=v<W]
        if 0 in n4 or len(n4)<4 or c in n4 or keten(S,y,x): continue
        cnt=Counter(n4).most_common()
        if len(cnt)>1 and cnt[0][1]==cnt[1][1]:
            best=Counter(S[u,v] for u in range(y-1,y+2) for v in range(x-1,x+2) if (u,v)!=(y,x) and S[u,v]!=c).most_common(1)[0][0]
        else: best=cnt[0][0]
        if 2<=best<=6: T[y,x]=best; log.append(f'A ({x},{y}) {c}->{best}')
S=T.copy(); P=np.pad(S,1)
for y in range(H):
    for x in range(W):
        if S[y,x]<5 or OOG(y,x): continue
        N,Sd,Wd,E=P[y,x+1]==0,P[y+2,x+1]==0,P[y+1,x]==0,P[y+1,x+2]==0
        if not (N or Sd or Wd or E): continue
        v=(Dk[y,x] if 2<=Dk[y,x]<=4 else 4) if (N or Wd) else (1 if Dk[y,x]<=2 else Dk[y,x])
        T[y,x]=v; log.append(f'B ({x},{y}) {S[y,x]}->{v}')
np.save(D+'r6/idx.npy',T); open(D+'r6/log.txt','w').write('\n'.join(log)+'\n')
print('A',sum(l[0]=='A' for l in log),'B',sum(l[0]=='B' for l in log))
save_p64(T,pal,D+'r6/sprite.png'); save_idx(T,pal,D+'r6/r6_8x.png',8)
