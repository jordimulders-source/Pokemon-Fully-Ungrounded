# Lijnschets fase 2 (v6b): looplijn van het lijf die 1x om de pijl krult en dan opricht; pijl; plek kop en handen.
from PIL import Image, ImageDraw
import math
im=Image.new('RGB',(1024,1024),'white'); d=ImageDraw.Draw(im)
G=(140,140,140); GB=(210,210,210)
bx,by,fx,fy=700,700,260,470
ang=math.atan2(fy-by,fx-bx);ux,uy=math.cos(ang),math.sin(ang);nx,ny=-uy,ux;w=30
def cr(p,n=40):
    out=[];P=[p[0]]+p+[p[-1]]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        for k in range(n):
            t=k/n;t2=t*t;t3=t2*t
            out.append(tuple(0.5*((2*p1[j])+(-p0[j]+p2[j])*t+(2*p0[j]-5*p1[j]+4*p2[j]-p3[j])*t2+(-p0[j]+3*p1[j]-3*p2[j]+p3[j])*t3) for j in (0,1)))
    return out
# deel 1: uit de achterkant naar achteren en omlaag, dan terug naar de pijl
start=cr([(bx,by),(790,740),(800,820),(740,840)],30)
# deel 2: helix om de pijl, 1 slag, van s=110 naar s=260
R=72; hel=[]
for k in range(181):
    t=k/180; s=40+250*t; th=-math.pi/2+3*math.pi*t
    hel.append((bx+ux*s+nx*R*math.sin(th), by+uy*s+ny*R*math.sin(th), math.cos(th)>0))
# helix begint onderaan (sin=-1) = kant waar 'start' eindigt
# deel 3: van het eind van de helix omhoog in een S naar de kop
ex,ey=hel[-1][:2]
up=cr([(ex,ey),(ex+60,ey-60),(570,330),(510,260)],30)
# achter de pijl
for a,b in zip(hel,hel[1:]):
    if not a[2]: d.line([a[:2],b[:2]],fill=GB,width=10)
d.line(up,fill=G,width=12,joint='curve')
# pijl
poly=[(bx+nx*w,by+ny*w),(fx+nx*w,fy+ny*w),(fx-nx*w,fy-ny*w),(bx-nx*w,by-ny*w)]
d.polygon(poly,fill='white',outline=(0,0,0),width=6)
tx,ty=fx+90*ux,fy+90*uy
d.polygon([(fx+nx*(w+10),fy+ny*(w+10)),(tx,ty),(fx-nx*(w+10),fy-ny*(w+10))],fill='white',outline=(0,0,0),width=6)
# voor de pijl
d.line(start+[hel[0][:2]],fill=G,width=12,joint='curve')
for a,b in zip(hel,hel[1:]):
    if a[2]: d.line([a[:2],b[:2]],fill=G,width=12)
# kop en handen
d.ellipse([420,170,600,320],outline=G,width=8)
for s,(sx,sy) in [(320,(560,380)),(400,(540,360))]:
    hx,hy=bx+ux*s-nx*(w+12),by+uy*s-ny*(w+12)
    d.line([(sx,sy),(hx,hy)],fill=G,width=10); d.ellipse([hx-18,hy-18,hx+18,hy+18],outline=G,width=8,fill='white')
im.save('schets/lijnschets_v6.png')
