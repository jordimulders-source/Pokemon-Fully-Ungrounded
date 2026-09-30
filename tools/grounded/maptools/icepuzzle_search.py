import random, itertools, json, sys
from collections import deque
X0,X1,Y0,Y1=2,15,2,13
startp={(x,y) for x in range(2,5) for y in range(10,13)}
goalp={(x,y) for x in range(14,16) for y in range(2,5)}
START=(3,11); GOAL=(15,3)
D=((1,0),(-1,0),(0,1),(0,-1))
def graph(rocks,present,snow):
    def kind(p):
        x,y=p
        if not(X0<=x<=X1 and Y0<=y<=Y1) or p in rocks or p in present: return 0
        return 1 if p in snow else 2
    G={}
    q=[START];G[START]=None
    adj={}
    while q:
        p=q.pop(); out=[]
        for dx,dy in D:
            n=(p[0]+dx,p[1]+dy)
            if not kind(n): continue
            c=n
            while kind(c)==2:
                n2=(c[0]+dx,c[1]+dy)
                if not kind(n2): break
                c=n2
            out.append(c)
            if c not in adj and c not in q: adj[c]=None; q.append(c)
        adj[p]=out
    return adj
def check(adj):
    if GOAL not in adj: return None
    rev={}
    for p,o in adj.items():
        for c in o: rev.setdefault(c,[]).append(p)
    for t in (START,GOAL):
        s={t};q=[t]
        while q:
            p=q.pop()
            for c in rev.get(p,[]):
                if c not in s: s.add(c); q.append(c)
        if len(s)!=len(adj): return None
    d={START:0};q=deque([START])
    while q:
        p=q.popleft()
        for c in adj[p]:
            if c not in d: d[c]=d[p]+1; q.append(c)
    return d[GOAL]
rnd=random.Random(int(sys.argv[1])); best=None; pb=0
cells=[(x,y) for x in range(X0,X1+1) for y in range(Y0,Y1+1) if (x,y) not in startp|goalp]
for it in range(int(sys.argv[2])):
    if best and rnd.random()<0.8:
        rocks=set(best[1]); items=list(best[2])
        for _ in range(rnd.randint(1,3)):
            r=rnd.random(); free=[c for c in cells if c not in rocks and c not in items]
            if r<0.5 and rocks: rocks.remove(rnd.choice(sorted(rocks))); rocks.add(rnd.choice(free))
            elif r<0.65 and len(rocks)<16: rocks.add(rnd.choice(free))
            elif r<0.8 and len(rocks)>8: rocks.remove(rnd.choice(sorted(rocks)))
            else: items[rnd.randrange(3)]=rnd.choice(free)
    else:
        items=rnd.sample(cells,3)
        rocks=set(rnd.sample([c for c in cells if c not in items],rnd.randint(8,14)))
    snow=startp|goalp|set(items)
    minlen=99
    for k in range(4):
        for taken in itertools.combinations(items,k):
            present=set(items)-set(taken)
            adj=graph(rocks,present,snow)
            L=check(adj)
            if L is None: minlen=None; break
            for (ix,iy) in present:
                if not any((ix+dx,iy+dy) in adj for dx,dy in D): minlen=None
            if minlen is None: break
            minlen=min(minlen,L)
        if minlen is None: break
    if minlen and (best is None or minlen>=best[0]):
        best=(minlen,sorted(rocks),items); print(best,flush=True) if minlen>pb else None; pb=minlen
        json.dump({'rocks':best[1],'items':best[2],'len':best[0]},open('room2v3_%s.json'%sys.argv[1],'w'))
