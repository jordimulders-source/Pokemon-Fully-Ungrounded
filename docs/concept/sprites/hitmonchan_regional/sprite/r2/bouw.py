# r2: ontkorrelen van r1 (geen nieuwe tinten, geen vormwijziging): een vultintpixel (2-8) die in zijn kleur een 4-cluster van 1 px is
# en niet in een diagonale keten (8-buren, >=3 px) van dezelfde kleur ligt -> meest voorkomende kleur van zijn 4-buren (gelijkspel: 8-buren),
# Oogzone (natieve rijen 24-31, kolommen 28-37 = sprite rijen 18-25, kolommen 21-30) blijft 1-op-1.
# alleen als die buurkleur ook een vultint is (2-8). Lijnpixels (1), wit (9, glans) en randpixels (achtergrondbuur) blijven staan.
import numpy as np, sys
from collections import Counter
D='docs/concept/sprites/hitmonchan_regional/sprite/'
sys.path.insert(0,D); from toon import save_idx, save_p64
S=np.load(D+'r1/idx.npy'); H,W=S.shape; pal=eval(open(D+'pal.txt').read())
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
        if not (2<=c<=8) or (18<=y<=25 and 21<=x<=30): continue
        n4=[S[u,v] for u,v in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)) if 0<=u<H and 0<=v<W]
        if 0 in n4 or len(n4)<4 or c in n4: continue
        if keten(S,y,x): continue
        cnt=Counter(n4).most_common()
        if len(cnt)>1 and cnt[0][1]==cnt[1][1]:
            n8=Counter(S[u,v] for u in range(y-1,y+2) for v in range(x-1,x+2) if (u,v)!=(y,x) and S[u,v]!=c)
            best=n8.most_common(1)[0][0]
        else: best=cnt[0][0]
        if 2<=best<=8: T[y,x]=best; log.append((x,y,int(c),int(best)))
np.save(D+'r2/idx.npy',T); open(D+'r2/log.txt','w').write('\n'.join(f'({x},{y}) {a}->{b}' for x,y,a,b in log)+'\n')
print('gewijzigd',len(log))
save_p64(T,pal,D+'r2/sprite.png'); save_idx(T,pal,D+'r2/r2_8x.png',8)
