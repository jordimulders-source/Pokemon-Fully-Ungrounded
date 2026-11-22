# kijk.py SPRITE.png UIT.png x0 y0 x1 y1 : close-up van de sprite (20x, met coordinaten) naast het natieve model van precies hetzelfde
# gebied (rijen/kolommen die bij het schrappen bleven; de geschrapte zijn in het model als dunne grijze streep zichtbaar)
import sys; sys.path.insert(0,'gereedschap')
from PIL import Image, ImageDraw; import numpy as np; from gemeen import *; import schrap as S
x0,y0,x1,y1=map(int,sys.argv[3:7]); z=20
o=laden(sys.argv[1]); A=rgb(o,(255,255,255)).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
a,c,L=klassen(); S.PRIO={11:4,5:4,4:4}; _,rows,cols=S.schrap_merge(c)
kr=[i for i in range(c.shape[0]) if i not in rows]; kk=[i for i in range(c.shape[1]) if i not in cols]
ys=[kr[y-Y0] for y in range(y0,y1) if 0<=y-Y0<len(kr)]; xs=[kk[x-X0] for x in range(x0,x1) if 0<=x-X0<len(kk)]
v0,v1=ys[0],ys[-1]+1; u0,u1=xs[0],xs[-1]+1
B=Image.fromarray(a[v0:v1,u0:u1].astype('uint8')).resize(((u1-u0)*15,(v1-v0)*15),Image.NEAREST)
W=Image.new('RGB',(A.width+B.width+10,max(A.height,B.height)),'white'); W.paste(A,(0,0)); W.paste(B,(A.width+10,0))
d=ImageDraw.Draw(W)
for i in range(x1-x0+1): d.line([(i*z,0),(i*z,A.height)],fill=(200,200,200))
for j in range(y1-y0+1): d.line([(0,j*z),(A.width,j*z)],fill=(200,200,200))
for i in range(x1-x0): d.text((i*z+2,1),str((x0+i)%100),fill=(0,140,255))
for j in range(y1-y0): d.text((1,j*z+9),str(y0+j),fill=(0,140,255))
for r in rows:
    if v0<=r<v1: d.line([(A.width+10,(r-v0)*15+7),(W.width,(r-v0)*15+7)],fill=(150,150,150))
for k in cols:
    if u0<=k<u1: d.line([(A.width+10+(k-u0)*15+7,0),(A.width+10+(k-u0)*15+7,B.height)],fill=(150,150,150))
W.save(sys.argv[2])
