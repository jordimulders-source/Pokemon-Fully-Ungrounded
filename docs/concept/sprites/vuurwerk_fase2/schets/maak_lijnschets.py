# Lijnschets fase 2 (v6): alleen de looplijn van het lijf + de pijl; kop/armen niet getekend.
from PIL import Image, ImageDraw
import math
im=Image.new('RGB',(1024,1024),'white'); d=ImageDraw.Draw(im)
def cr(p,n=40):
    out=[];P=[p[0]]+p+[p[-1]]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        for k in range(n):
            t=k/n;t2=t*t;t3=t2*t
            out.append(tuple(0.5*((2*p1[j])+(-p0[j]+p2[j])*t+(2*p0[j]-5*p1[j]+4*p2[j]-p3[j])*t2+(-p0[j]+3*p1[j]-3*p2[j]+p3[j])*t3) for j in (0,1)))
    return out
pts=cr([(660,655),(770,740),(730,860),(570,885),(440,800),(430,640),(480,470),(510,360),(490,280)])
G=(150,150,150)
bx,by,fx,fy=665,650,250,435
d.line(pts[:165],fill=G,width=10,joint='curve')
ang=math.atan2(fy-by,fx-bx);ux,uy=math.cos(ang),math.sin(ang);nx,ny=-uy,ux;w=30
poly=[(bx+nx*w,by+ny*w),(fx+nx*w,fy+ny*w),(fx-nx*w,fy-ny*w),(bx-nx*w,by-ny*w)]
d.polygon(poly,fill='white',outline=(0,0,0),width=6)
tx,ty=fx+90*ux,fy+90*uy
d.polygon([(fx+nx*(w+10),fy+ny*(w+10)),(tx,ty),(fx-nx*(w+10),fy-ny*(w+10))],fill='white',outline=(0,0,0),width=6)
d.line(pts[160:],fill=G,width=10,joint='curve')
# kop: alleen een cirkel als plek
d.ellipse([400,190,560,330],outline=G,width=8)
# handen: twee stippen op de pijl
for x,y in [(330,470),(420,520)]: d.ellipse([x-18,y-18,x+18,y+18],outline=G,width=8)
im.save('schets/lijnschets_v6.png')
