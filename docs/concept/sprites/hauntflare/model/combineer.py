# Model Hauntflare: r4_b als basis, staart van r4_a (zelfde natieve raster 99x99, pitch 10,24).
# Staart = alles wat niet wit, niet bolroze en niet ringbruin is, vanaf een zaadpixel, onder y=59.
import sys; from PIL import Image; import numpy as np; from collections import deque
DX,DY=int(sys.argv[1]),int(sys.argv[2]); OUT=sys.argv[3]
A=np.asarray(Image.open('model/nat_r4_a.png')).astype(int); B=np.asarray(Image.open('model/nat_r4_b.png')).astype(int).copy()
def wit(c): return c.min()>=0xf0
def roze(c): return c[0]>=0xf0 and c[2]>=0x75 and not wit(c)
def zwart(c): return c.max()<0x40
def staart(img,seed,ymin):
    H,W,_=img.shape; m=np.zeros((H,W),bool); q=deque([seed]); m[seed[1],seed[0]]=True
    def ok(x,y):
        c=img[y,x]
        if y<ymin or wit(c) or roze(c): return False
        if zwart(c):   # zwarte lijn alleen als hij niet aan bolroze grenst
            for ex,ey in((1,0),(-1,0),(0,1),(0,-1)):
                if 0<=x+ex<W and 0<=y+ey<H and roze(img[y+ey,x+ex]): return False
        return True
    while q:
        x,y=q.popleft()
        for ex,ey in((1,0),(-1,0),(0,1),(0,-1)):
            X,Y=x+ex,y+ey
            if 0<=X<W and 0<=Y<H and not m[Y,X] and ok(X,Y): m[Y,X]=True; q.append((X,Y))
    return m
mb=staart(B,(62,68),59); ma=staart(A,(60,68),59)
print('staartpixels b',mb.sum(),'a',ma.sum())
B[mb]=255
# kleuren van a naar het palet van b
ANK={(0xd6,0x3b,0x4d):(0xcb,0x43,0x5a),(0xf4,0x86,0x59):(0xf8,0x85,0x6c),(0xe6,0x63,0x82):(0xe8,0x5f,0x80),
     (0xb6,0x47,0x2a):(0xba,0x3c,0x26),(0x6c,0x21,0x30):(0x24,0x16,0x1a),(0x1a,0x15,0x19):(0x24,0x16,0x1a)}
ks=np.array(list(ANK.keys())); vs=np.array(list(ANK.values()))
ys,xs=np.where(ma)
for y,x in zip(ys,xs):
    X,Y=x+DX,y+DY
    if not wit(B[Y,X]): continue          # alleen achter de bol/ring/handen
    k=np.argmin(((ks-A[y,x])**2).sum(1)); B[Y,X]=vs[k]
Image.fromarray(B.astype('uint8')).save(OUT)
