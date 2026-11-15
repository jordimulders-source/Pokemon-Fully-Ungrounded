# Model "Jordi": pose en balkleur r4_b, ogen+mond r3_b, handen r4_a, ring r4_c, vlammen r3_b met de vlamkleuren van r4_a.
# Alles op het natieve raster van r4_b (99x99, pitch 10,24). r3_b heeft een ander raster (12,8): die delen
# worden op volle resolutie verschoven (bol r3_b -> bol r4_b) en op het r4_b-raster bemonsterd.
import sys; from PIL import Image; import numpy as np; from collections import deque
STAART=sys.argv[1]  # 'r3_b' of 'r4_b'
OUT=sys.argv[2]
L=lambda n: np.asarray(Image.open(n).convert('RGB')).astype(int)
B=L('model/nat_r4_b.png').copy(); C=L('model/nat_r4_c.png'); A=L('model/nat_r4_a.png'); F3=L('gemini/r3_b.png')
H,W,_=B.shape
def wit(c): return c.min()>=0xe8
def roze(c): return c[0]>=0xf0 and c[2]>=0x75 and not wit(c)
def ring(c): return (0x70<=c[0]<=0xa0 and 0x40<=c[1]<=0x60 and c[2]>=0x48) or (abs(c[0]-c[2])<0x30 and 0x50<=c[0]<=0xd0 and c[1]<c[0])
def zwart(c): return c.max()<0x40
def flood(img,seed,ok):
    m=np.zeros(img.shape[:2],bool); q=deque([seed]); m[seed[1],seed[0]]=True
    while q:
        x,y=q.popleft()
        for ex,ey in((1,0),(-1,0),(0,1),(0,-1)):
            X,Y=x+ex,y+ey
            if 0<=X<img.shape[1] and 0<=Y<img.shape[0] and not m[Y,X] and ok(img,X,Y): m[Y,X]=True; q.append((X,Y))
    return m
def buur_roze(img,x,y):
    return any(0<=x+ex<img.shape[1] and 0<=y+ey<img.shape[0] and roze(img[y+ey,x+ex]) for ex,ey in((1,0),(-1,0),(0,1),(0,-1)))
def vlamok(ymin=None,ymax=None):
    def ok(img,x,y):
        c=img[y,x]
        if (ymin is not None and y<ymin) or (ymax is not None and y>ymax): return False
        if wit(c) or roze(c) or ring(c): return False
        if zwart(c) and buur_roze(img,x,y): return False
        return True
    return ok
nietwit=lambda img,x,y: not wit(img[y,x])
# 1. ring van r4_c: alle pixels die in r4_b of r4_c ringkleur hebben, plus de donkere omlijning ernaast
M=np.zeros((H,W),bool)
for y in range(H):
    for x in range(W):
        if (ring(B[y,x]) or ring(C[y,x])) and not (x>=48 and y>=58) and not (y<=30 and x>=50): M[y,x]=True
D=M.copy()
for y in range(1,H-1):
    for x in range(1,W-1):
        if not M[y,x] and M[y-1:y+2,x-1:x+2].any() and zwart(C[y,x]): D[y,x]=True
B[D]=C[D]
# 2. handen: r4_b-handen weg, r4_a-handen op hetzelfde zwaartepunt
def hand(img,seed): return flood(img,seed,nietwit)
BB=L('model/nat_r4_b.png')
def zoek(img,box):
    for y in range(box[1],box[3]):
        for x in range(box[0],box[2]):
            if not wit(img[y,x]) and not ring(img[y,x]): return (x,y)
FAR=(zoek(BB,(76,52,90,62)),zoek(A,(76,50,90,60)))
for sb,sa in(((28,72),(22,72)),FAR):
    hb=hand(L('model/nat_r4_b.png'),sb); ha=hand(A,sa)
    yb,xb=np.where(hb); ya,xa=np.where(ha)
    dx=int(round(xb.mean()-xa.mean())); dy=int(round(yb.mean()-ya.mean()))
    B[hb]=255
    for y,x in zip(ya,xa): B[y+dy,x+dx]=A[y,x]
    print('hand',sb,'->',dx,dy,hb.sum(),ha.sum())
# r3_b-bemonstering: doelcel (i,j) -> volle-resolutie punt in r4_b, min verschuiving -> punt in r3_b
P=10.24; X0=9.5+1+P/2; Y0=9.0+1+P/2
SX,SY=21,33   # bol r3_b (490,500) -> bol r4_b (469,467)
def r3(i,j):
    x=int(X0+i*P+SX); y=int(Y0+j*P+SY)
    if not (2<=x<1022 and 2<=y<1022): return np.array([255,255,255])
    return np.median(F3[y-2:y+3,x-2:x+3].reshape(-1,3),axis=0).astype(int)
R3=np.array([[r3(i,j) for i in range(W)] for j in range(H)])
# vlamkleuren r3_b -> r4_a
PAL={(0xd0,0x38,0x50):(0xd6,0x3b,0x4d),(0xc8,0x38,0x48):(0xd6,0x3b,0x4d),(0xf0,0x80,0x60):(0xf4,0x86,0x59),
     (0xf0,0x58,0x68):(0xe6,0x63,0x82),(0xf8,0x78,0xb0):(0xe6,0x63,0x82),(0xf8,0x68,0xa8):(0xe6,0x63,0x82),(0xb0,0x40,0x38):(0xc3,0x48,0x2d),(0x18,0x10,0x10):(0x1a,0x15,0x19)}
ks=np.array(list(PAL)); vs=np.array(list(PAL.values()))
def kleur(c): return vs[np.argmin(((ks-c)**2).sum(1))]
CX,CY,RR=44.3,44.1,21.6
def geo(img,sel):
    m=np.zeros((H,W),bool)
    for y in range(H):
        for x in range(W):
            c=img[y,x]
            if wit(c) or ring(c) or (x-CX)**2+(y-CY)**2<=(RR+0.5)**2: continue
            if sel(x,y): m[y,x]=True
    return m
def plak_vlam(sel):
    mb=geo(BB,sel); m3=geo(R3,sel)
    B[mb]=255
    for y,x in zip(*np.where(m3)):
        if wit(B[y,x]): B[y,x]=kleur(R3[y,x])
    print('vlam',mb.sum(),m3.sum())
# 3. kuif
plak_vlam(lambda x,y: y<=38 and x>=40)
# 4. staart
if STAART=='r3_b': plak_vlam(lambda x,y: y>=58 and x>=44 and not (x>=72 and y<=63))
# 5. gezicht: vak rond de ogen en mond; r3_b-pixels, roze naar het dichtstbijzijnde r4_b-bolroze
x0,x1,y0,y1=22,48,36,56
bolroze=[B[y,x] for y in range(30,60) for x in range(20,65) if roze(B[y,x])]
bolroze=np.unique(np.array(bolroze),axis=0)
for y in range(y0,y1):
    for x in range(x0,x1):
        c=R3[y,x]; cur=B[y,x]
        if not (roze(cur) or zwart(cur) or (cur[0]>0xc0 and cur[1]<0x90)): continue   # alleen op de bol
        if ring(cur) : continue
        if roze(c): B[y,x]=bolroze[np.argmin(((bolroze-c)**2).sum(1))]
        elif not wit(c) or c.min()>=0xe8: B[y,x]=c
# losse stipjes (componenten < 4 px) weg
seen=np.zeros((H,W),bool)
for y in range(H):
    for x in range(W):
        if seen[y,x] or wit(B[y,x]): continue
        m=flood(B,(x,y),nietwit); seen|=m
        if m.sum()<4: B[m]=255
Image.fromarray(B.astype('uint8')).save(OUT)
