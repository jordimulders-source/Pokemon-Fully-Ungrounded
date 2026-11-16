# r5: naadmasker drempelen in de ijszone en uitdunnen tot 1 px (Zhang-Suen)
import numpy as np, sys
from gio import from_txt, CH
D=np.load('r5_D.npy'); o=from_txt('r4.txt'); H,W=o.shape
C={c:i for i,c in enumerate(CH)}
TH=float(sys.argv[1]) if len(sys.argv)>1 else 0.15
ice=set(C[c] for c in 'WLMDS')
# ijszone = kop+lijf: ijspixels links van de kern, niet de buitenlijn
fixed=np.zeros_like(o,bool)
for y in range(H):
    for x in range(W):
        if o[y,x]==C['K']: fixed[y,x]=1
        if o[y,x]==C['S'] and any(not(0<=y+a<H and 0<=x+b<W) or o[y+a,x+b]<0 for a,b in((1,0),(-1,0),(0,1),(0,-1))): fixed[y,x]=1
zone=np.zeros_like(o,bool)
for y in range(24,61):
    kx=[x for x in range(22,40) if o[y,x]==C['K']] if y>=39 else []
    lim=kx[0] if kx else 34
    for x in range(0,lim):
        if o[y,x] in ice and not fixed[y,x]: zone[y,x]=1
# kop: alleen rechts tot de kern (S-lijn) en onder de ogen-rij niet de ogen
zone[:,:]&=True
B=(D>=TH)&zone
def zs(B):
    B=B.copy().astype(np.uint8); ch=True
    while ch:
        ch=False
        for step in (0,1):
            rm=[]
            for y in range(1,H-1):
                for x in range(1,W-1):
                    if not B[y,x]: continue
                    P=[B[y-1,x],B[y-1,x+1],B[y,x+1],B[y+1,x+1],B[y+1,x],B[y+1,x-1],B[y,x-1],B[y-1,x-1]]
                    n=sum(P)
                    if n<2 or n>6: continue
                    a=sum(1 for i in range(8) if P[i]==0 and P[(i+1)%8]==1)
                    if a!=1: continue
                    if step==0 and (P[0]*P[2]*P[4]==0) and (P[2]*P[4]*P[6]==0): rm.append((y,x))
                    if step==1 and (P[0]*P[2]*P[6]==0) and (P[0]*P[4]*P[6]==0): rm.append((y,x))
            for p in rm: B[p]=0; ch=True
    return B.astype(bool)
S=zs(B)
np.save('r5_seam.npy',S); np.save('r5_zone.npy',zone); np.save('r5_fixed.npy',fixed)
for y in range(24,61):
    print('%2d '%y+''.join('#' if S[y,x] else ('-' if zone[y,x] else ('.' if o[y,x]<0 else CH[o[y,x]].lower())) for x in range(36)))
