# Ruisfilter (alleen vulkleuren, binnen dezelfde kleurgroep): een eilandje (4-samenhangend) van één tint
# kleiner dan MIN px neemt de meest voorkomende buurtint (8 buren) uit dezelfde groep aan.
# Omlijning, oogrood en tanden worden niet aangeraakt; manen en de beschermde zones ook niet (handwerk). Herhaalt tot stabiel. gebruik: ontruis.py in out
import sys
from collections import Counter
LIJF=set('abmlvw')  # r (selout/lijnen) niet: dunne lijnen
MAAN=set('gGhH')
MIN={'lijf':2,'maan':1}
# beschermde zones (y0,y1,x0,x1): wervel en gezicht worden met de hand gedaan
BESCHERM=[(27,40,33,48),(28,47,12,33)]
def beschermd(y,x):
    # randpixels (grenzen aan transparant) blijven: dat is silhouet/selout
    if any(not(0<=y+dy<64 and 0<=x+dx<64) or R[y+dy][x+dx]=='.' for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): return True
    return any(a<=y<=b and c<=x<=d for a,b,c,d in BESCHERM)
R=[list(l.rstrip('\n')) for l in open(sys.argv[1])][:64]
def groep(c): return 'lijf' if c in LIJF else 'maan' if c in MAAN else None
def eilanden():
    seen=set(); out=[]
    for y in range(64):
        for x in range(64):
            if (y,x) in seen or groep(R[y][x]) is None or beschermd(y,x): continue
            c=R[y][x]; st=[(y,x)]; comp=[]; seen.add((y,x))
            while st:
                p=st.pop(); comp.append(p)
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    q=(p[0]+dy,p[1]+dx)
                    if 0<=q[0]<64 and 0<=q[1]<64 and q not in seen and R[q[0]][q[1]]==c: seen.add(q); st.append(q)
            out.append((c,comp))
    return out
n=0
for it in range(10):
    ch=0
    for c,comp in eilanden():
        g=groep(c)
        if len(comp)>=MIN[g]: continue
        cnt=Counter()
        S=set(comp)
        for (y,x) in comp:
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    q=(y+dy,x+dx)
                    if q in S or not(0<=q[0]<64 and 0<=q[1]<64): continue
                    v=R[q[0]][q[1]]
                    if groep(v)==g and v!=c: cnt[v]+=1
        if not cnt: continue
        nv=cnt.most_common(1)[0][0]
        for (y,x) in comp: R[y][x]=nv; ch+=1
    n+=ch
    if not ch: break
open(sys.argv[2],'w').write('\n'.join(''.join(r) for r in R)+'\n')
print('gewijzigd',n)
