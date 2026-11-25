# Klassen per natieve modelpixel guarana (alleen indelen van modelkleuren, geen tekenen).
# 0 bg, 1 K zwart, 2 R rood (vruchten), 3 G groen (rank, ranken, blad), 4 W oogwit (wit/grijs)
import numpy as np; from PIL import Image
NAMEN=['bg','K','R','G','W']
def klassen(path='gereedschap/natief.png'):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    R,G,B=a[...,0],a[...,1],a[...,2]; L=.299*R+.587*G+.114*B
    c=np.zeros(a.shape[:2],int)
    wt=a.min(2)>=235
    # achtergrond = wit dat met de rand verbonden is; ingesloten wit in de vruchttros (x<52, y<54) = oogwit, elders (gaten in de krullen) = achtergrond
    from collections import deque
    bg=np.zeros(wt.shape,bool); H,W=wt.shape; q=deque()
    for y in range(H):
        for x in (0,W-1):
            if wt[y,x] and not bg[y,x]: bg[y,x]=True; q.append((y,x))
    for x in range(W):
        for y in (0,H-1):
            if wt[y,x] and not bg[y,x]: bg[y,x]=True; q.append((y,x))
    while q:
        y,x=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and wt[yy,xx] and not bg[yy,xx]: bg[yy,xx]=True; q.append((yy,xx))
    YY,XX=np.mgrid[0:H,0:W]
    oogwit=wt&~bg&(XX<52)&(YY<54)
    bg=bg|(wt&~bg&~oogwit)
    sat=a.max(2)-a.min(2)
    zw=(L<45)&~bg
    rood=(R>G+40)&~bg&~zw
    groen=(G>R+8)&~bg&~zw&~rood
    wit=(~bg&~zw&~rood&~groen&(sat<40)&(L>=110))|oogwit
    c[rood]=2; c[groen]=3; c[wit]=4; c[zw]=1
    rest=~bg&(c==0)
    c[rest]=np.where(L[rest]<110,1,4)
    return a,c,L
if __name__=='__main__':
    a,c,L=klassen()
    for i,n in enumerate(NAMEN):
        m=c==i; print(n,m.sum(), a[m].mean(0).astype(int) if m.any() else '', 'L p10/50/90', np.percentile(L[m],[10,50,90]).astype(int) if m.any() else '')
    ch='.KRGW'
    for y in range(17,81): print('%3d '%y+''.join(ch[v] for v in c[y,12:87]))
