import sys, numpy as np
from gio import from_txt, CH
G=from_txt(sys.argv[1]); m=G>=0
print('kleuren:',sorted(set(CH[v] for v in G[m].ravel())), len(set(G[m].ravel())),'+ transparant')
ys,xs=np.where(m); print('bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max(),'=',xs.max()-xs.min()+1,'x',ys.max()-ys.min()+1)
ok=set('KSMD')
bad=[]
for y in range(64):
    for x in range(64):
        if not m[y,x]: continue
        if any(not (0<=yy<64 and 0<=xx<64) or not m[yy,xx] for yy,xx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]):
            if CH[G[y,x]] not in ok: bad.append((x,y,CH[G[y,x]]))
print('rand niet-lijn:',bad)
# losse pixels: geen 4-buur met dezelfde kleur
seen=np.zeros_like(m); small=[]
for y in range(64):
    for x in range(64):
        if not m[y,x] or seen[y,x]: continue
        c=G[y,x]; st=[(y,x)]; seen[y,x]=1; comp=[]
        while st:
            a,b=st.pop(); comp.append((b,a))
            for yy,xx in [(a-1,b),(a+1,b),(a,b-1),(a,b+1)]:
                if 0<=yy<64 and 0<=xx<64 and not seen[yy,xx] and G[yy,xx]==c: seen[yy,xx]=1; st.append((yy,xx))
        if len(comp)<3: small.append((CH[c],comp))
print('clusters <3 px:',len(small))
for s in small: print('  ',s)
print('--- 8-verbonden componenten < 3 px (niet C/v):')
seen=np.zeros_like(m)
for y in range(64):
    for x in range(64):
        if not m[y,x] or seen[y,x]: continue
        c=G[y,x]; st=[(y,x)]; seen[y,x]=1; comp=[]
        while st:
            a,b=st.pop(); comp.append((b,a))
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    yy,xx=a+dy,b+dx
                    if 0<=yy<64 and 0<=xx<64 and not seen[yy,xx] and G[yy,xx]==c: seen[yy,xx]=1; st.append((yy,xx))
        if len(comp)<3 and CH[c] not in 'C': print('  ',CH[c],comp)
