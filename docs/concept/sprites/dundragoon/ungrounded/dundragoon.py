import sys, math
# Testsprite (niet in de game). Draaien: python3 tools/grounded/fakemon/dundragoon.py tools/grounded/fakemon
sys.path.insert(0,sys.argv[1]); S=sys.argv[1]
from sprlib import *
cv=Canvas()
def yel(li,dark=0):
    k=3 if li>0.72 else 2 if li>0.3 else 1 if li>-0.1 else 0
    k=max(0,k-dark); return [4,3,2,0xB][k]
def teal(li,dark=0):
    k=2 if li>0.45 else 1 if li>0.0 else 0
    k=max(0,k-dark); return [0xD,0xC,0xA][k]
def wing(base,mid,tip,wmax,dark):
    cl=bez([base,mid,tip],80); N=len(cl); pix={}
    for i,(cx,cy) in enumerate(cl):
        t=i/(N-1)
        w=wmax*(math.sin(math.pi*min(1,t*1.15))**0.6)*(1-0.25*t)+0.6
        for y in range(int(cy-w-1),int(cy+w+2)):
            for x in range(int(cx-w-1),int(cx+w+2)):
                if math.hypot(x+0.5-cx,y+0.5-cy)<=w:
                    # kant: links van de as = licht
                    if i<N-1: ax,ay=cl[i+1][0]-cx,cl[i+1][1]-cy
                    side=(x+0.5-cx)*(-ay)+(y+0.5-cy)*ax
                    band=(t*3.2)%1
                    col=7 if side>-w*0.1 else 9 if side>-w*0.55 else 8
                    if 0.15<t<0.9 and band<0.16: col=8 if col==7 else 6
                    if dark: col={7:9,9:8,8:6,6:6}[col]
                    if (x,y) not in pix: pix[(x,y)]=col
    return pix
# verre vleugel, verre poot
cv.paint(wing((38,40),(43,23),(49,6),5.2,1),6)
def leg(hip,knee,foot,dark):
    p=tube([hip,knee,foot],lambda t:3.4-1.4*t,lambda x,y,li,t,nx,ny: yel(li,dark+(1 if ny>0.5 else 0)))
    cv.paint(p,1,5)
    f=ellipse(foot[0]-1.5,foot[1]+1.2,3.6,2.0,lambda x,y,li,a,b: teal(li,dark))
    cv.paint(f,0xD,5)
    for k in range(3):  # teentjes
        x,y=int(foot[0]-4+k*2.2),int(foot[1]+3)
        if cv.c[y][x]: cv.c[y][x]=7
leg((42,44),(43,49),(42,54),1)
# lijf: hals, romp, staart
pts=[(20,30),(23,38),(30,42),(37,43),(44,42),(51,39),(55,32),(56,26),(56.5,17),(57,6)]
T0=7/9
def rad(t):
    if t<0.14: return 3.6-2*t
    if t<0.43: return 3.3+3.2*math.sin(math.pi*(t-0.14)/0.29)
    if t<T0: return 3.6-1.0*(t-0.43)/(T0-0.43)
    u=min(1,(t-T0)/(1-T0))
    if u<0.18: return 2.6+2.2*u/0.18
    return 4.8*max(0,1-(u-0.18)/0.82)**0.95+0.35
def body(x,y,li,t,nx,ny):
    if t>T0-0.01:
        u=(t-T0)/(1-T0)
        if u>0.12 and ((u*9+nx*0.9)%1)<0.38: return 4 if li>-0.1 else 1
        return yel(li)
    if ny>0.42: return teal(li)
    if ny<0.05 and 0.22<t<0.44 and (t*14)%1<0.38: return teal(li)
    return yel(li)
BODY=cv.paint(tube(pts,rad,body),1,5)
# nabije poot
leg((32,45),(33,50),(31,55),0)
# rugstekels langs hals, rug en staart
cl=bez(pts)
def spikes(xs,size):
    for sx in xs:
        top=min(y for y in range(W) if cv.part[y][sx]==BODY)
        sp={}
        for dy in range(size):
            for dx in range(size-1-dy, size):
                sp[(sx-size//2+dx+dy//2, top-size+1+dy)]=0xC if dx==size-1 else 0xA
        cv.paint(sp,0xD)
spikes([42,47],5)
# oren: kleine Dunsparce-vleugeltjes (verre eerst, kop eroverheen)
dun=Image.open('graphics/pokemon/dunsparce/anim_front.png').crop((0,0,64,64))
EAR={}
for y in range(19,31):
    for x in range(21,31):
        c=dun.getpixel((x,y))
        if c in (6,7,8,9) or (c==5 and any(dun.getpixel((x+dx,y+dy)) in (6,7,8,9) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))):
            EAR[(x-21,y-19)]=c
def ear(ox,oy,dark):
    pix={}
    for (x,y),c in EAR.items():
        if dark: c={7:9,9:8,8:6,6:6,5:5}[c]
        pix[(x+ox,y+oy)]=c
    for q,c in pix.items():
        if 0<=q[0]<W and 0<=q[1]<W: cv.c[q[1]][q[0]]=c; cv.part[q[1]][q[0]]=99
ear(9,7,1)
# kop met drakensnuit
hx,hy=16,23
def headsh(x,y,li,a,b):
    return yel(li)
def snoutsh(x,y,li,a,b):
    if b>-0.05: return teal(li)
    return yel(li)
hd=ellipse(hx,hy,9,8,headsh,rot=0.12)
sn=ellipse(8,28,7,4.6,snoutsh,rot=0.18)
hd.update(sn)
cv.paint(hd,1,5)
# Dunsparce-oog: blauwe ring, room binnen, slaperig streepje
ex,ey=17,21
for y in range(ey-4,ey+5):
    for x in range(ex-4,ex+5):
        d=math.hypot(x+0.5-ex-0.5,y+0.5-ey-0.5)
        if d<=3.6: cv.c[y][x]=0xC if d>2.7 else (0xA if d>2.1 else 0xB)
for x in range(ex-2,ex+4): cv.c[ey+1][x]=6
cv.c[ey][ex-2]=6; cv.c[ey][ex+3]=6
# mond: lach langs de snuit, tong eruit
for x,y in [(3,30),(4,31),(5,31),(6,32),(7,32),(8,32),(9,32),(10,32),(11,31),(12,31)]: cv.c[y][x]=0xD
for x,y in [(6,33),(7,33),(7,34),(8,34),(8,33)]: cv.c[y][x]=0xE
cv.c[35][7]=5; cv.c[35][8]=5; cv.c[34][6]=5; cv.c[34][9]=5; cv.c[33][9]=5;cv.c[33][5]=5
# neusgat
cv.c[26][3]=0xD; cv.c[26][4]=0xD
# nabij oor
ear(16,6,0)
# nabije vleugel
cv.paint(wing((30,40),(30,22),(37,4),5.6,0),6)
pal=[(152,208,160),(112,88,64),(240,224,120),(216,184,56),(184,136,32),(16,16,16),(88,96,112),(240,248,248),
     (184,200,224),(208,224,240),(104,184,200),(248,240,192),(48,136,160),(32,104,128),(232,112,136),(0,0,0)]
im=cv.save(pal,f'{S}/dundragoon.png')
im.convert('RGBA').resize((384,384),Image.NEAREST).save(f'{S}/dundragoon_zoom.png')
