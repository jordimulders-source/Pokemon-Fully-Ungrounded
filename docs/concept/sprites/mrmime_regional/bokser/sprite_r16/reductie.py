# Kale reductie van het natieve model op de 52-schaal (zelfde methode, oorsprong en schaal als sprite_r10/reductie.py,
# alleen de uitsnede rechts breder (natief x12-84 i.p.v. 12-72), zodat de elleboog van de nabije arm erbij zit).
from PIL import Image; import numpy as np; from collections import deque
a=np.asarray(Image.open('../sprite_r10/natief.png').convert('L')).astype(float)[5:93,12:84]
H,W=a.shape
band=np.select([a<25,a<66,a<115,a<160,a<225],[1,2,3,4,5],6)
bg=np.zeros_like(band,bool); q=deque()
for y in range(H):
    for x in range(W):
        if (y in(0,H-1) or x in(0,W-1)) and band[y,x]==6: bg[y,x]=1; q.append((y,x))
for s in [(62,38),(38,48)]:
    assert band[s]==6, s; bg[s]=1; q.append(s)
while q:
    y,x=q.popleft()
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<H and 0<=xx<W and not bg[yy,xx] and band[yy,xx]==6: bg[yy,xx]=1; q.append((yy,xx))
band[bg]=0
OH=52; s=88/OH; OW=int(W/s)
out=np.zeros((OH,OW),int)
for j in range(OH):
    for i in range(OW):
        c=np.zeros(7); y0,y1=j*s,(j+1)*s; x0,x1=i*s,(i+1)*s
        for y in range(int(y0),min(H,int(np.ceil(y1)))):
            wy=min(y1,y+1)-max(y0,y)
            for x in range(int(x0),min(W,int(np.ceil(x1)))):
                wx=min(x1,x+1)-max(x0,x); c[band[y,x]]+=wy*wx
        c=c/c.sum()
        if c[0]>=0.5: continue
        if c[1]>=0.3: out[j,i]=1; continue
        c2=c.copy(); c2[0]=0; c2[1]=0
        out[j,i]=int(np.argmax(c2)) if c2.sum()>0 else 1
np.save('kaal52_breed.npy',out)
k0=np.load('../sprite_r10/kaal52.npy'); print('gelijk met r10-kaal52 op x<35:',bool((out[:,:35]==k0).all()))
print('   '+''.join(str(x%10) for x in range(OW)))
for j in range(10,30): print('%2d '%j+''.join('.#DmnlW'[v] for v in out[j]))
