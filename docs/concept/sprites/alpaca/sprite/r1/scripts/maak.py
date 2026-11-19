# Palpaca r1 stap 2-3: zones/tonen -> oud palet (stap A), technisch opschonen (stap B: buitenlijn, binnenlijnen, ruis).
import numpy as np; from PIL import Image
from scipy import ndimage
zone=np.load('zone_t.npy'); T=np.load('tone_t.npy'); C=np.load('rgb_t.npy'); H,W=zone.shape
pal=[tuple(map(int,l.split())) for l in open('../../../ronde17/variant_kop/normal.pal').read().split('\n')[3:19]]
P=np.array(pal,float)
def pidx(z,l,rgb):
    if z=='W': return 2 if l>=237 else 3 if l>=198 else 4
    if z=='D': return 4 if l>=152 else 5 if l>=118 else 6
    if z=='G': return 7 if l>=135 else 8 if l>=95 else 9 if l>=58 else 10
    if z=='T': return 8 if l>=98 else 9 if l>=66 else 10
    if z=='P': return 14
    if z=='C':
        c=[11,12,13,14]; return c[int(np.argmin([((P[i]-rgb)**2).sum() for i in c]))]
    if z=='E': return 1 if l<90 else 2 if l>=200 else 15
    if z=='K': return 1
# wol: toonkaart licht gladgestreken binnen de wol (volume blijft, korrel weg)
w=(zone=='W').astype(float); Tw=ndimage.gaussian_filter(T*w,0.6)/np.maximum(ndimage.gaussian_filter(w,0.6),1e-6)
T=np.where(zone=='W',0.5*T+0.5*Tw,T)
A=np.zeros((H,W),int)
for y in range(H):
  for x in range(W):
    if zone[y,x]!='.': A[y,x]=pidx(zone[y,x],T[y,x],C[y,x])
np.save('stapA.npy',A)
B=A.copy(); fg=A>0
def nb(y,x):
    for dy,dx in((-1,0),(1,0),(0,-1),(0,1)): yield y+dy,x+dx,dy,dx
def isbg(y,x): return not(0<=y<H and 0<=x<W) or not fg[y,x]
# 1. ruis in de wol: tintvlakjes < 3 px nemen de meest voorkomende buurtint (binnen wol 2-5) aan
for it in range(2):
  for t in (2,3,4,5):
    lab,n=ndimage.label((B==t)&(zone=='W'))
    for k in range(1,n+1):
        m=lab==k
        if m.sum()>=3 or (t==2 and m.sum()>=2): continue
        rr=ndimage.binary_dilation(m)&~m&(zone=='W')&(B>=2)&(B<=5)
        if rr.any(): B[m]=np.bincount(B[rr]).argmax()
# 2. buitenlijn: randpixels van het silhouet; lichtkant (achtergrond links/boven) = selout, schaduwkant = zwart
rand=np.zeros_like(fg)
for y in range(H):
  for x in range(W):
    if not fg[y,x]: continue
    bl=[(dy,dx) for yy,xx,dy,dx in nb(y,x) if isbg(yy,xx)]
    if not bl: continue
    rand[y,x]=True
    licht=any(d in bl for d in((-1,0),(0,-1))) and not any(d in bl for d in((1,0),(0,1)))
    z=zone[y,x]
    if z in('G','T'): B[y,x]=10 if licht else 1
    elif z=='D': B[y,x]=1
    elif z=='C': B[y,x]=1
    else: B[y,x]=6 if licht else 1
# 3. binnenlijnen (K binnenin): donkere modellijn (toon < 135) = 5, lichte krullijn = schaduwtint 4, tussen onderdelen (raakt D/G/C) zwart
for y in range(H):
  for x in range(W):
    if zone[y,x]=='K' and not rand[y,x]:
        nz={zone[yy,xx] for yy,xx,_,_ in nb(y,x) if 0<=yy<H and 0<=xx<W}
        B[y,x]=1 if nz&{'D','G','C','T'} else 5 if T[y,x]<135 else 4
# 4. losse lijnpuntjes: een binnenlijnpixel 5 zonder lijnbuur (5/1/6, 8-buren) wordt de zachte schaduwtint 4 (geen 1-px-vlekje)
for y in range(H):
  for x in range(W):
    if B[y,x]==5 and zone[y,x]=='K':
        nb8=B[max(0,y-1):y+2,max(0,x-1):x+2]
        if ((nb8==5)|(nb8==1)|(nb8==6)).sum()<=1: B[y,x]=4
np.save('stapB.npy',B)
def save(arr,fn,scale=1):
    im=Image.fromarray(arr.astype('uint8'),'P'); im.putpalette(sum(pal,())) ; im.save(fn,transparency=0)
S=np.zeros((64,64),int); oy=64-H-2; ox=(64-W)//2+1
S[oy:oy+H,ox:ox+W]=B
np.save('plaats.npy',np.array([oy,ox]))
save(S,'../palpaca.png')
print(oy,ox)
for y in range(H): print('%2d '%y+''.join('.' if v==0 else '0123456789abcdef'[v] for v in B[y]))
