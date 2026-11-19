# Vormschets vuurwerk fase 1 (bijlage voor Gemini): alleen opbouw, geen kleur.
import math
from PIL import Image, ImageDraw
W=1024; im=Image.new('RGB',(W,W),'white'); d=ImageDraw.Draw(im)
K='black'
def tube(pts, w, dashed=False):
    if dashed:
        for i in range(0,len(pts)-1,8):
            d.line(pts[i:i+4],fill=(120,120,120),width=6)
        return
    for x,y in pts: d.ellipse([x-w/2-5,y-w/2-5,x+w/2+5,y+w/2+5],fill=K)
    for x,y in pts: d.ellipse([x-w/2,y-w/2,x+w/2,y+w/2],fill='white')
cx,r,e=480,100,50
def helix(y0,k,t0,t1,n=200):
    return [(cx+r*math.cos(t0+(t1-t0)*i/n), y0+k*(t0+(t1-t0)*i/n if t1>t0 else -(t0+(t1-t0)*i/n))+e*math.sin(t0+(t1-t0)*i/n)) for i in range(n+1)]
arms=[(350,30,0,2.6*math.pi),(420,30,0,2.4*math.pi)]
def split(pts):
    segs=[];cur=[];front=None
    for (x,y),(t) in pts:
        f=math.sin(t)>0
        if front is None or f==front: cur.append((x,y))
        else: segs.append((front,cur)); cur=[cur[-1],(x,y)]
        front=f
    segs.append((front,cur)); return segs
armsegs=[]
for y0,k,t0,t1 in arms:
    n=300; pts=[]
    for i in range(n+1):
        t=t0+(t1-t0)*i/n; s=abs(t)
        pts.append(((cx+r*math.cos(t), y0+k*s+e*math.sin(t)),t))
    armsegs.append((split(pts),pts[-1]))
# 1 achterkant van de armen (gestippeld)
for segs,_ in armsegs:
    for front,p in segs:
        pass
# 2 pijl
d.polygon([(480,150),(370,300),(590,300)],fill='white',outline=K,width=6)
d.rectangle([400,300,560,760],fill='white',outline=K,width=6)
for y in (380,460,540,620,700): d.line([(400,y),(560,y)],fill=K,width=3)
d.polygon([(425,760),(535,760),(520,800),(440,800)],fill='white',outline=K,width=6)
# 3 lijf: vlam uit het mondstuk, buigt omhoog, alleen bovenlijf
def bez(P,n=120):
    out=[]
    for i in range(n+1):
        t=i/n; m=len(P)-1
        x=sum(math.comb(m,j)*(1-t)**(m-j)*t**j*P[j][0] for j in range(m+1))
        y=sum(math.comb(m,j)*(1-t)**(m-j)*t**j*P[j][1] for j in range(m+1))
        out.append((x,y))
    return out
spine=bez([(480,790),(470,900),(690,900),(670,620),(650,400),(640,250)])
L=[];R=[]
for i in range(len(spine)-1):
    (x0,y0),(x1,y1)=spine[i],spine[i+1]
    dx,dy=x1-x0,y1-y0; l=math.hypot(dx,dy) or 1; nx,ny=-dy/l,dx/l
    w=6+40*(i/len(spine))**1.2
    L.append((x0+nx*w,y0+ny*w)); R.append((x0-nx*w,y0-ny*w))
d.polygon(L+R[::-1],fill='white',outline=K,width=6)
# vlamtongen langs de rand

# kop boven de pijl, naar links
d.ellipse([560,150,720,280],fill='white',outline=K,width=6)
d.polygon([(570,205),(530,225),(575,250)],fill='white',outline=K,width=6)
d.ellipse([600,185,622,207],fill=K)
d.line([(545,232),(600,240)],fill=K,width=4)
for x,y in ((690,150),(715,175),(728,210)): d.polygon([(x-15,y+10),(x+15,y-25),(x+10,y+15)],fill='white',outline=K,width=4)
# 4 voorkant van de armen
for segs,end in armsegs:
    for front,p in segs:
        if front and len(p)>1: tube(p,22)
# schouders: arm begint aan het lijf
for y0 in (350,420): tube([(cx+r+i*(40/30),y0-i*(40/30)) for i in range(31)],22)
# handjes onder de krullen
for (x,y),t in [a[1] for a in armsegs]:
    d.ellipse([x-22,y-18,x+22,y+18],fill='white',outline=K,width=6)
    for dx in (-14,0,14): d.ellipse([x+dx-7,y+12,x+dx+7,y+26],fill='white',outline=K,width=4)
im.save('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/vuurwerk_fase1/schets/vormschets.png')
