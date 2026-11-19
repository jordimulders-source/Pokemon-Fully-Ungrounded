# Vormschets fase 2 (v5: kop 1-4 van Jordi 19 nov). python3 schets/maak_vormschets.py
from PIL import Image, ImageDraw
import math
W=1024; im=Image.new('RGB',(W,W),'white'); d=ImageDraw.Draw(im)
def cr(p,n=40):
    out=[];P=[p[0]]+p+[p[-1]]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        for k in range(n):
            t=k/n;t2=t*t;t3=t2*t
            out.append(tuple(0.5*((2*p1[j])+(-p0[j]+p2[j])*t+(2*p0[j]-5*p1[j]+4*p2[j]-p3[j])*t2+(-p0[j]+3*p1[j]-3*p2[j]+p3[j])*t3) for j in (0,1)))
    return out
pts=cr([(660,655),(770,740),(730,860),(570,885),(440,800),(430,640),(480,470),(510,360),(490,280)])
N=len(pts)
def rad(i): return 26+64*min(1,i/(N*0.85))**1.6
OUT=(60,30,40)
def body(rng):
    for i in rng:
        x,y=pts[i];r=rad(i)+6;d.ellipse([x-r,y-r,x+r,y+r],fill=OUT)
    for i in rng:
        x,y=pts[i];r=rad(i);t=i/N
        c=tuple(int(a*(1-t)+b*t) for a,b in zip((215,40,60),(250,150,185)))
        d.ellipse([x-r,y-r,x+r,y+r],fill=c)
bx,by,fx,fy=665,650,250,435;w=46
ang=math.atan2(fy-by,fx-bx);nx,ny=-math.sin(ang),math.cos(ang);ux,uy=math.cos(ang),math.sin(ang)
def tube():
    poly=[(bx+nx*w,by+ny*w),(fx+nx*w,fy+ny*w),(fx-nx*w,fy-ny*w),(bx-nx*w,by-ny*w)]
    d.polygon(poly,fill=(240,120,170))
    for k in range(1,9):
        t=k/9;cx,cy=bx+(fx-bx)*t,by+(fy-by)*t;c=[(250,215,60),(190,40,120)][k%2];s=14
        d.polygon([(cx+nx*w-ux*s+ux*25,cy+ny*w-uy*s+uy*25),(cx+nx*w+ux*s+ux*25,cy+ny*w+uy*s+uy*25),(cx-nx*w+ux*s,cy-ny*w+uy*s),(cx-nx*w-ux*s,cy-ny*w-uy*s)],fill=c)
    d.polygon(poly,outline=OUT,width=8)
    tx,ty=fx+120*ux,fy+120*uy
    d.polygon([(fx+nx*(w+16),fy+ny*(w+16)),(tx,ty),(fx-nx*(w+16),fy-ny*(w+16))],fill=(245,130,180),outline=OUT,width=8)
    d.ellipse([bx-26,by-46,bx+26,by+46],fill=(120,70,50),outline=OUT,width=6)
cross=[i for i in range(N) if 165<=i<225]
body([i for i in range(N) if i not in cross]); tube(); body(cross)
CREAM=(250,240,215)
# 3. vlammenkam, naar achteren gestreken (geen losse kieuwpunten)
kam=[(380,190),(470,150),(560,140),(700,110),(620,175),(720,170),(630,220),(700,250),(560,260),(500,250)]
d.polygon(kam,fill=(240,80,110),outline=OUT,width=8)
# 1. lange, platte kop met spitsere snuit
kop=[(235,262),(250,232),(290,212),(450,188),(540,200),(575,240),(560,290),(480,315),(330,312),(262,300),(235,262)]
kop=cr(kop,12)
d.polygon(kop,fill=CREAM,outline=OUT,width=8)
# 4. klierbult achter het oog
d.chord([440,170,560,250],180,360,fill=CREAM,outline=OUT,width=8)
d.line([(446,212),(554,212)],fill=CREAM,width=10)
# 2. halfgeloken oog
d.ellipse([380,210,430,250],fill=(30,20,30)); d.ellipse([398,218,410,230],fill='white')
d.chord([372,198,438,262],180,360,fill=CREAM)
d.line([(372,230),(440,226)],fill=OUT,width=9)
# grijns
d.line([(250,282),(330,292),(400,282)],fill=OUT,width=8,joint='curve')
d.line([(395,282),(410,270)],fill=OUT,width=8)
for (sx,sy),(ex,ey) in [((480,410),(420,540)),((455,375),(330,470))]:
    d.line([(sx,sy),(ex,ey)],fill=OUT,width=46);d.line([(sx,sy),(ex,ey)],fill=(250,160,190),width=32)
    d.ellipse([ex-28,ey-28,ex+28,ey+28],fill=(250,160,190),outline=OUT,width=6)
im.save('schets/vormschets_v5.png')
