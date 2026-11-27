# check.py rN: kleuren, oog 1-op-1 t.o.v. natief, losse pixels (clusters van 1-2 px per kleur, 4-buren), rechte runs in de buitenlijn
import numpy as np, sys
D='docs/concept/sprites/hitmonchan_regional/sprite/'
sys.path.insert(0,D); from schrap import schrap
r=sys.argv[1]; S=np.load(D+f'{r}/idx.npy'); H,W=S.shape
q=np.load(D+'natief_q.npy'); rd,cd,kr,kc=schrap(q)
print('figuur',W,'x',H,' kleuren gebruikt',len(set(S.ravel())-{0}))
# oog: natieve rijen 25-30, kolommen 29-36
ry=[kr.index(y) for y in range(25,31)]; cx=[kc.index(x) for x in range(29,37)]
same=(S[np.ix_(ry,cx)]==q[25:31,29:37]).mean() if r=='r1' else None
print('oog in sprite: rijen',ry[0],'-',ry[-1],' kolommen',cx[0],'-',cx[-1], ' (natief 8x6)', ' gelijk aan natief (r1-index):',same)
# clusters
seen=np.zeros_like(S,bool); los=[]
for y in range(H):
    for x in range(W):
        if S[y,x]==0 or seen[y,x]: continue
        c=S[y,x]; st=[(y,x)]; comp=[]; seen[y,x]=True
        while st:
            a,b=st.pop(); comp.append((a,b))
            for da,db in ((1,0),(-1,0),(0,1),(0,-1)):
                u,v=a+da,b+db
                if 0<=u<H and 0<=v<W and not seen[u,v] and S[u,v]==c: seen[u,v]=True; st.append((u,v))
        if len(comp)<=2: los.append((c,len(comp),comp[0]))
print('clusters <=2 px:',len(los))
from collections import Counter; print(' per kleur',sorted(Counter(c for c,_,_ in los).items()))
# buitenlijn: pixels met een achtergrondbuur
P=np.pad(S,1); rand=(S>0)&((P[:-2,1:-1]==0)|(P[2:,1:-1]==0)|(P[1:-1,:-2]==0)|(P[1:-1,2:]==0))
# lange rechte runs van randpixels (horizontaal/verticaal) >=6
runs=[]
for y in range(H):
    n=0
    for x in range(W+1):
        if x<W and rand[y,x] and (y==0 or S[y-1,x]==0 or y==H-1 or S[y+1,x]==0): n+=1
        else:
            if n>=6: runs.append(('h',y,x-n,n))
            n=0
for x in range(W):
    n=0
    for y in range(H+1):
        if y<H and rand[y,x] and (x==0 or S[y,x-1]==0 or x==W-1 or S[y,x+1]==0): n+=1
        else:
            if n>=6: runs.append(('v',x,y-n,n))
            n=0
print('rechte randruns >=6:',runs)
