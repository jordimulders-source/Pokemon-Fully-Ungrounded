# Controle: kleuren, losse pixels, open buitenlijn, losse lijnpixels binnenin, tintvlakjes < 3 px (behalve glans/oog/lijn)
import numpy as np, sys
from collections import deque, Counter
from txt import CH
for v in 'A':
    a=np.load(f'sprite_{v}.npy'); H,W=a.shape
    used=Counter(CH[x] for x in a.flatten() if x)
    print('==',v,'kleuren incl. transparant:',len(used)+1, dict(used))
    openr=[];los=[];lijn=[]
    for y in range(H):
        for x in range(W):
            if not a[y,x]: continue
            nb4=[(y+dy,x+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
            edge=any(not(0<=yy<H and 0<=xx<W) or a[yy,xx]==0 for yy,xx in nb4)
            if edge and CH[a[y,x]] not in '#dbL': openr.append((y,x))
            n8=[(y+dy,x+dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=y+dy<H and 0<=x+dx<W]
            if all(a[p]==0 for p in n8): los.append((y,x))
            if CH[a[y,x]] in '#d' and not edge and not any(CH[a[p]] in '#dE' for p in n8): lijn.append((y,x))
    seen=np.zeros_like(a,bool); klein=[]
    for y in range(H):
        for x in range(W):
            if a[y,x]==0 or seen[y,x]: continue
            c=a[y,x]; q=deque([(y,x)]); seen[y,x]=1; comp=[]
            while q:
                cy,cx=q.popleft(); comp.append((cy,cx))
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    ny,nx=cy+dy,cx+dx
                    if 0<=ny<H and 0<=nx<W and not seen[ny,nx] and a[ny,nx]==c: seen[ny,nx]=1; q.append((ny,nx))
            if len(comp)<3 and CH[c] not in 'wE#dbL': klein.append((CH[c],comp))
    print(' open rand',openr,'| los',los,'| losse lijnpixels binnen',lijn)
    print(' tintvlakjes <3 px:',len(klein),klein)
