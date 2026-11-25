# Achtergrond = met de rand verbonden lichte pixels (>=thr); wit binnen de omlijning blijft figuur.
import numpy as np
from collections import deque
def bgmask(a, thr=232):
    L=a.astype(int).mean(axis=2) if a.ndim==3 else a; light=L>=thr
    H,W=light.shape; bg=np.zeros_like(light); q=deque()
    for y in range(H):
        for x in (0,W-1):
            if light[y,x] and not bg[y,x]: bg[y,x]=1; q.append((y,x))
    for x in range(W):
        for y in (0,H-1):
            if light[y,x] and not bg[y,x]: bg[y,x]=1; q.append((y,x))
    while q:
        y,x=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            v,u=y+dy,x+dx
            if 0<=v<H and 0<=u<W and light[v,u] and not bg[v,u]: bg[v,u]=1; q.append((v,u))
    return bg.astype(bool)
