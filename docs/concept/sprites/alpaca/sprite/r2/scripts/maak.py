# Palpaca r1 stap 2-3: zones/tonen -> oud palet (stap A), technisch opschonen (stap B: buitenlijn, binnenlijnen, ruis).
import numpy as np; from PIL import Image
from scipy import ndimage
zone=np.load('zone_t.npy'); T=np.load('tone_t.npy'); C=np.load('rgb_t.npy'); H,W=zone.shape
pal=[tuple(map(int,l.split())) for l in open('../normal.pal').read().split('\n')[3:19]]
P=np.array(pal,float)
def pidx(z,l,rgb,y=0,x=0):
    if z=='W':
        # r2: hals (model 184-195) licht, alleen kinschaduw (167-179) in 4; kop: grens 212 zodat de modelschaduw onder de kuif
        # (193-211) en de sikkel rechtsonder op de wang (190-213) als tintvorm meekomen (Jordi: hoekige kop oplossen met kleur en schaduw)
        g=182 if (19<=y<=22 and 3<=x<=14) else 212 if (y<=18 and x<=16) else 198
        return 2 if l>=237 else 3 if l>=g else 4
    if z=='D': return 11 if l>=118 else 15   # r2: verre achterpoot grijsbeige (11) met donkerder grijsbeige (15) waar hij achter het lijf verdwijnt
    if z=='G': return 7 if l>=135 else 8 if l>=95 else 9 if l>=58 else 10
    if z=='T': return 8 if l>=98 else 9 if l>=66 else 10
    if z=='P': return 14
    if z=='C':
        c=[12,13,14]; return c[int(np.argmin([((P[i]-rgb)**2).sum() for i in c]))]
    if z=='E': return 1 if l<90 else 2 if l>=200 else 6
    if z=='K': return 1
# wol: toonkaart licht gladgestreken binnen de wol (volume blijft, korrel weg)
w=(zone=='W').astype(float); Tw=ndimage.gaussian_filter(T*w,0.6)/np.maximum(ndimage.gaussian_filter(w,0.6),1e-6)
T=np.where(zone=='W',0.5*T+0.5*Tw,T)
A=np.zeros((H,W),int)
for y in range(H):
  for x in range(W):
    if zone[y,x]!='.': A[y,x]=pidx(zone[y,x],T[y,x],C[y,x],y,x)
np.save('stapA.npy',A)
# r2 kop: schaduwtint 4 op de wang alleen als sikkel langs de rand rechts/onder (<= 2 px van de omtrek), niet als groot vlak
for y in range(11,19):
  for x in range(0,17):
    if A[y,x]==4 and zone[y,x]=='W':
        rand=[(y,x+1),(y,x+2),(y+1,x),(y+2,x),(y+1,x+1)]
        if not any(not(0<=yy<H and 0<=xx<W) or zone[yy,xx] in('.','K') and (xx>=x) for yy,xx in rand if True):
            A[y,x]=3
B=A.copy(); fg=A>0
BULT={tuple(b) for b in np.load('bult.npy')}
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
    if (x,y) in BULT: licht=(0,-1) in bl or ((-1,0) in bl and (0,1) not in bl and x<16)  # r2: krulbultje links/boven = lichtkant
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
