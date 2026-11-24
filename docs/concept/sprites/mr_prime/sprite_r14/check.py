# Kleine tintclusters (<3 px, 4-buren) en randpixels zonder omlijning in de drie zones
import numpy as np; from collections import deque
K=np.load('K14.npy')
Z=[(44,58,26,42),(41,64,44,64),(36,44,49,55)]
zm=np.zeros((64,64),bool)
for x0,x1,y0,y1 in Z: zm[y0:y1,x0:x1]=1
for c in range(1,9):
    seen=np.zeros((64,64),bool)
    for sy,sx in zip(*np.where(K==c)):
        if seen[sy,sx]: continue
        m=np.zeros((64,64),bool); q=deque([(sy,sx)]); m[sy,sx]=seen[sy,sx]=1
        while q:
            y,x=q.popleft()
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                v,u=y+dy,x+dx
                if 0<=v<64 and 0<=u<64 and K[v,u]==c and not m[v,u]: m[v,u]=seen[v,u]=1; q.append((v,u))
        if m.sum()<3 and (m&zm).any():
            ys,xs=np.where(m); print('cluster kleur',c,'grootte',m.sum(),list(zip(xs,ys)))
# vulpixel die aan transparant grenst (open rand)
for y in range(64):
    for x in range(64):
        if zm[y,x] and K[y,x]>0:
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                v,u=y+dy,x+dx
                if 0<=v<64 and 0<=u<64 and K[v,u]<0: print('open rand',(x,y),'kleur',K[y,x]); break
