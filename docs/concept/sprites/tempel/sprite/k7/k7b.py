import sys, numpy as np
sys.path.insert(0,'../k1')
from gereedschap import *
a0,pal=laad('../k6/tempel.png')
H,W=a0.shape
BLOK={0,1,2,7,12,10,11}
LICHT={4:3,5:4,6:5}; DONKER={3:4,4:5,5:6,6:15}
vast=np.zeros_like(a0,bool)
for (x0,y0,x1,y1) in OGEN: vast[y0:y1+1,x0:x1+1]=True
vast|=deurmasker(a0)
def blk(x,y): return not(0<=x<W and 0<=y<H) or a0[y,x] in BLOK
def run(x,y,dx,dy):
    n=0
    while not blk(x+dx*(n+1),y+dy*(n+1)): n+=1
    return n
FR=0.67
def maak(MINW=4,MINH=3):
    a=a0.copy()
    for y in range(H):
      for x in range(W):
        T=a0[y,x]
        if T not in DONKER or vast[y,x]: continue
        l,r,u,d=run(x,y,-1,0),run(x,y,1,0),run(x,y,0,-1),run(x,y,0,1)
        w=l+r+1; h=u+d+1
        top = blk(x,y-1) and blk(x,y-1) and a0[y-1,x] in (1,2,7) and h>=MINH and w>=MINW and l < FR*w
        left= a0[y,x-1] in (1,2,7) and w>=MINW and h>=MINH and u < FR*h
        bot = a0[y+1,x] in (1,2,7) and h>=MINH and w>=MINW and r < FR*w
        right=a0[y,x+1] in (1,2,7) and w>=MINW and h>=MINH and d < FR*h
        L=top or left; D=bot or right
        if L and not D and T in LICHT: a[y,x]=LICHT[T]
        elif D and not L: a[y,x]=DONKER[T]
    return a
def comp(b,x,y):
    c=b[y,x]; st=[(x,y)]; s={(x,y)}
    while st:
        q=st.pop()
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            u,v=q[0]+dx,q[1]+dy
            if 0<=u<W and 0<=v<H and (u,v) not in s and b[v,u]==c: s.add((u,v)); st.append((u,v))
    return s
def filt(a):
    for it in range(6):
        ch=0
        for y in range(H):
            for x in range(W):
                if a[y,x]!=a0[y,x]:
                    s=comp(a,x,y)
                    if len(s)<3:
                        for (u,v) in s:
                            if a[v,u]!=a0[v,u]: a[v,u]=a0[v,u]; ch+=1
        if not ch: break
    return a
if __name__=='__main__':
    a=filt(maak())
    bewaar(a,pal,'tempel_auto.png'); print((a!=a0).sum())
    from PIL import Image
    im=Image.open('tempel_auto.png').convert('RGBA'); b=Image.new('RGBA',(64,64),(255,255,255,255)); b.alpha_composite(im); b.convert('RGB').resize((512,512),Image.NEAREST).save('auto8.png')
