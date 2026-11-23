# Kale reductie van het natieve model (60x88) naar 43x63: oppervlakdekking per toonband.
# Niets getekend: elke spritepixel = de toonband van het model met de meeste dekking (zwart beschermd vanaf 30%).
from PIL import Image; import numpy as np; from collections import deque
a=np.asarray(Image.open('natief.png').convert('L')).astype(float)[5:93,12:72]
H,W=a.shape
# banden: 0 achtergrond, 1 zwart, 2 donker(D), 3 midden(m), 4 licht-midden(n), 5 lichtgrijs(l), 6 wit
band=np.select([a<25,a<66,a<115,a<160,a<225],[1,2,3,4,5],6)
# achtergrond = wit verbonden met de rand + ingesloten gaten (tussen benen, tussen arm en lijf)
bg=np.zeros_like(band,bool); q=deque()
for y in range(H):
    for x in range(W):
        if (y in(0,H-1) or x in(0,W-1)) and band[y,x]==6: bg[y,x]=1; q.append((y,x))
for s in [(62,38),(38,48)]:   # zaden ingesloten achtergrond (natief, uitsnede-coord.)
    assert band[s]==6, s; bg[s]=1; q.append(s)
while q:
    y,x=q.popleft()
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<H and 0<=xx<W and not bg[yy,xx] and band[yy,xx]==6: bg[yy,xx]=1; q.append((yy,xx))
band[bg]=0
np.save('band_natief.npy',band)
OH=63; s=H/OH; OW=int(round(W/s))
out=np.zeros((OH,OW),int)
def cov(j,i):
    c=np.zeros(7)
    y0,y1=j*s,(j+1)*s; x0,x1=i*s,(i+1)*s
    for y in range(int(y0),min(H,int(np.ceil(y1)))):
        wy=min(y1,y+1)-max(y0,y)
        for x in range(int(x0),min(W,int(np.ceil(x1)))):
            wx=min(x1,x+1)-max(x0,x); c[band[y,x]]+=wy*wx
    return c/c.sum()
for j in range(OH):
    for i in range(OW):
        c=cov(j,i)
        if c[0]>=0.5: continue
        if c[1]>=0.3: out[j,i]=1; continue
        c2=c.copy(); c2[0]=0; c2[1]=0
        out[j,i]=int(np.argmax(c2)) if c2.sum()>0 else 1
np.save('kaal.npy',out)
print(OW,OH)
for j,r in enumerate(out): print('%2d '%j+''.join('.#DmnlW'[v] for v in r))
