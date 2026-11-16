# r4 stap 1: lijf onder de kop opnieuw: schuine naden (polylijnen gemeten op model_12x), schotsen per vlak belicht.
from gio import from_txt, to_txt, CH
import numpy as np, math
o=from_txt('r3.txt'); H,W=o.shape
C={c:i for i,c in enumerate(CH)}
ice=set(C[c] for c in 'WLMDS')
def ch(y,x): return '.' if o[y,x]<0 else CH[o[y,x]]
# vaste pixels: buitenlijn (S naast transparant) en alle K
fixed=np.zeros_like(o,bool)
for y in range(H):
    for x in range(W):
        c=ch(y,x)
        if c=='K': fixed[y,x]=1
        if c=='S':
            for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                q,r=y+dy,x+dx
                if not(0<=q<H and 0<=r<W) or o[q,r]<0: fixed[y,x]=1
zone=np.zeros_like(o,bool)
for y in range(39,61):
    kx=[x for x in range(22,40) if o[y,x]==C['K']]
    lim=kx[0] if kx else 34
    for x in range(0,min(lim,34)):
        if o[y,x] in ice and not fixed[y,x]: zone[y,x]=1
seam=np.zeros_like(o,bool)
def line(pts):
    for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
        if abs(x1-x0)>=abs(y1-y0):
            lo,hi=sorted((x0,x1))
            for c in range(int(math.floor(lo)),int(math.floor(hi))+1):
                xc=min(max(c+0.5,lo),hi); t=(xc-x0)/(x1-x0) if x1!=x0 else 0
                seam[int(math.floor(y0+(y1-y0)*t)),c]=1
        else:
            lo,hi=sorted((y0,y1))
            for r in range(int(math.floor(lo)),int(math.floor(hi))+1):
                yc=min(max(r+0.5,lo),hi); t=(yc-y0)/(y1-y0)
                seam[r,int(math.floor(x0+(x1-x0)*t))]=1
NADEN={
'A':[(1,42.0),(5,43.2),(9.5,45.4)],
'B':[(9.5,45.4),(12.5,44.0),(16,43.2),(19,42.0),(21,40.6),(22.6,39.2)],
'C':[(12.5,44.0),(17,45.5),(21,46.5),(24,47.2),(26.5,45.8),(28.5,44.0),(29.3,42.5)],
'D':[(5,43.2),(7,45.3),(8.8,47.5),(9.2,49.5),(8.6,51.5),(7.5,53.0),(5.5,53.8)],
'F':[(9.2,49.5),(9.8,52),(11.5,53.2),(14,54.0),(18,55.2),(21.5,56.0),(23.5,56.4)],
'G':[(24,47.2),(24.5,48.5),(25.3,50.7),(26.5,52.3),(28.3,54.0)],
'I':[(23.5,56.4),(25.5,56.2),(27.5,54.8),(28.3,54.2),(31,54.0),(32.5,54.2)],
'J':[(14,54.0),(14.8,56.5),(14.3,58.5),(15,59.6)],
'K':[(21.5,56.0),(23.3,56.8),(24.7,58),(25.3,59.6)],
}
for p in NADEN.values(): line(p)
# 4-verbonden dubbelpixels in trapjes weghalen (alleen 8-verbonden lijn houden)
for _ in range(2):
    for y in range(1,H-1):
        for x in range(1,W-1):
            if not seam[y,x]: continue
            # L-hoek: buur rechts en buur onder beide naad en diagonaal ook -> overbodig
            for dy,dx in ((1,1),(1,-1),(-1,1),(-1,-1)):
                if seam[y+dy,x] and seam[y,x+dx] and not seam[y+dy,x+dx]:
                    pass
seam&=zone|(seam&~fixed&(o>=0))
seam&=~fixed
# vlakken labelen
lab=-np.ones_like(o); n=0
for y in range(H):
    for x in range(W):
        if zone[y,x] and not seam[y,x] and lab[y,x]<0:
            st=[(y,x)]; lab[y,x]=n
            while st:
                a,b=st.pop()
                for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                    q,r=a+dy,b+dx
                    if 0<=q<H and 0<=r<W and zone[q,r] and not seam[q,r] and lab[q,r]<0: lab[q,r]=n; st.append((q,r))
            n+=1
np.save('r4_lab.npy',lab); np.save('r4_seam.npy',seam)
for y in range(36,61):
    print('%2d '%y+''.join(('#' if seam[y,x] else (chr(65+lab[y,x]) if lab[y,x]>=0 else ch(y,x).lower() if ch(y,x)!='.' else ' ')) for x in range(36)))
