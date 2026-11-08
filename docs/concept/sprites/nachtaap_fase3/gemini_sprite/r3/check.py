import sys; from tools import *
from collections import Counter
a=load(sys.argv[1]); print('kleuren:',sorted(Counter(a.ravel()).items()))
H,W=a.shape
iso=[]; lone1=[]
for y in range(H):
    for x in range(W):
        v=a[y,x]
        if v==0: continue
        nb=[a[y+dy,x+dx] if 0<=y+dy<H and 0<=x+dx<W else 0 for dy,dx in((0,1),(1,0),(0,-1),(-1,0))]
        if v not in nb and v not in (1,9): iso.append((x,y,CH[v],''.join(CH[n] for n in nb)))
        if v==1:
            nb8=[a[y+dy,x+dx] if 0<=y+dy<H and 0<=x+dx<W else 0 for dy in(-1,0,1) for dx in(-1,0,1) if dy or dx]
            if 0 not in nb8 and sum(n==1 for n in nb)==0: lone1.append((x,y))
        if v!=1:
            if 0 in nb and v not in (15,): pass
print('losse pixels (geen 4-buur zelfde kleur):',len(iso)); print(iso)
print('losse zwarte pixels binnenin:',lone1)
# lichte kleur op buitenrand (grenst aan transparant)
edge=[(x,y,CH[a[y,x]]) for y in range(H) for x in range(W) if a[y,x] not in (0,1,15,5) and any((not(0<=y+dy<H and 0<=x+dx<W)) or a[y+dy,x+dx]==0 for dy,dx in((0,1),(1,0),(0,-1),(-1,0)))]
print('niet-lijn op buitenrand:',edge)
