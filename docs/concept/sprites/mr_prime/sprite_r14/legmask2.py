import numpy as np; from PIL import Image
from collections import deque
from legmask import N,BG,Lum
H,W=BG.shape
def flood(seed,ok):
    m=np.zeros((H,W),bool); q=deque([seed]); m[seed]=1
    while q:
        y,x=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            v,u=y+dy,x+dx
            if 0<=v<H and 0<=u<W and ok[v,u] and not m[v,u]: m[v,u]=1; q.append((v,u))
    return m
yy,xx=np.mgrid[0:H,0:W]
ok=(~BG)&(Lum>=28)&(xx>=118)&(yy>=126)&~((Lum>190)&(xx<126))
thigh=flood((140,135),ok)
shoe=flood((166,170),(~BG)&(Lum>=28)&(yy>=158))
core=thigh|shoe
# omlijning: donkere pixels die aan de kern grenzen (8-buren)
d=np.zeros_like(core)
for dy in (-1,0,1):
    for dx in (-1,0,1):
        d|=np.roll(np.roll(core,dy,0),dx,1)
outl=d&~core&~BG&(Lum<28)
# tweede ring voor dikke lijnen bij de schoen/enkel
d2=np.zeros_like(core); c2=core|outl
for dy in (-1,0,1):
    for dx in (-1,0,1):
        d2|=np.roll(np.roll(c2,dy,0),dx,1)
outl2=d2&~c2&~BG&(Lum<28)&(yy>=150)
leg=core|outl|outl2
if __name__=='__main__':
    print(thigh.sum(),shoe.sum(),leg.sum())
    x0,x1,y0,y1=100,186,120,178
    for y in range(y0,y1):
        s=''
        for x in range(x0,x1):
            if BG[y,x]: s+=' '
            else:
                c='@#%*+=-:.'[min(8,int(Lum[y,x])//28)]
                s+= c if not leg[y,x] else {'@':'0','#':'1','%':'2','*':'3','+':'4','=':'5','-':'6',':':'7','.':'8'}[c]
        print('%3d '%y+s)
