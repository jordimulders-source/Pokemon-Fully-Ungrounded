# kaal (0,75x-reductie, fase 0.67,0) -> technisch opgeschoonde sprite. Elke stap logt hoeveel pixels hij wijzigt.
import numpy as np, json
NAMEN=['_','O','B1','B2','B3','N','M','L1','L2','P','K1','K2','R','G','Y','W']
I={n:i for i,n in enumerate(NAMEN)}
o=np.load('kaal_0_67_0.npy').copy(); H,W=o.shape
log={}
def nb4(y,x):
    for dy,dx in((-1,0),(1,0),(0,-1),(0,1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<H and 0<=xx<W: yield yy,xx,dy,dx
        else: yield None,None,dy,dx
def comps(mask):
    lab=-np.ones(mask.shape,int); n=0; out=[]
    for y in range(H):
        for x in range(W):
            if mask[y,x] and lab[y,x]<0:
                st=[(y,x)]; lab[y,x]=n; pts=[]
                while st:
                    a,b=st.pop(); pts.append((a,b))
                    for yy,xx,_,_ in nb4(a,b):
                        if yy is not None and mask[yy,xx] and lab[yy,xx]<0: lab[yy,xx]=n; st.append((yy,xx))
                out.append(pts); n+=1
    return out
GROEP={I['B1']:'b',I['B2']:'b',I['B3']:'b',I['N']:'s',I['M']:'s',I['L1']:'s',I['L2']:'s',I['P']:'p',I['K1']:'k',I['K2']:'k',I['R']:'r',I['G']:'g',I['Y']:'y'}
# 1. losse vulklusters < 3 px (geen omlijning, geen accenten R/G/Y/P) nemen de meest voorkomende buurklasse aan
n1=0
for it in range(3):
    for k in [I[c] for c in ('B1','B2','B3','N','M','L1','L2','K1','K2')]:
        for pts in comps(o==k):
            if len(pts)>=3: continue
            from collections import Counter
            c=Counter(o[yy,xx] for (a,b) in pts for yy,xx,_,_ in nb4(a,b) if yy is not None and o[yy,xx] not in (0,k,I['O']))
            if c: 
                v=c.most_common(1)[0][0]
                for a,b in pts: o[a,b]=v; n1+=1
log['1_kleine_vulklusters']=n1
# 2. buitenrand: elke dekkende pixel met transparante 4-buur wordt omlijning
n2=0; rand=np.zeros_like(o,bool)
for y in range(H):
    for x in range(W):
        if o[y,x] and any(yy is None or o[yy,xx]==0 for yy,xx,_,_ in nb4(y,x)):
            rand[y,x]=True
            if o[y,x]!=I['O']: o[y,x]=I['O']; n2+=1
log['2_buitenrand_dicht']=n2
# 3. dubbele buitenlijn: binnen-O die aan de rand-O grenst en geen binnenlijn voortzet -> buurvulkleur
n3=0
from collections import Counter
for it in range(2):
    for y in range(H):
        for x in range(W):
            if o[y,x]==I['O'] and not rand[y,x]:
                nbs=[(yy,xx) for yy,xx,_,_ in nb4(y,x) if yy is not None]
                if not any(rand[a,b] for a,b in nbs): continue
                # zet hij een binnenlijn voort (O-buur die zelf niet aan de rand ligt)?
                inner=[(a,b) for a,b in nbs if o[a,b]==I['O'] and not rand[a,b]]
                if inner: continue
                c=Counter(o[a,b] for a,b in nbs if o[a,b] not in (0,I['O']))
                if c: o[y,x]=c.most_common(1)[0][0]; n3+=1
log['3_dubbele_rand_weg']=n3
np.save('stap3.npy',o); np.save('rand.npy',rand)
print(json.dumps(log))
