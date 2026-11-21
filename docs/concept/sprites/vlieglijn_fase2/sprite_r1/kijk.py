# kijk.py raster.txt x0 y0 x1 y1 S out.png : sprite-uitsnede op S x naast het model op dezelfde schaal met spritepixelraster.
import sys,numpy as np; from PIL import Image,ImageDraw
from kaal_pal import PAL
f,x0,y0,x1,y1,S,o=sys.argv[1],*map(int,sys.argv[2:7]),sys.argv[7]
a=np.loadtxt(f,dtype=int)
P=np.array(PAL,'uint8'); c=P[a]; c[a==0]=(235,245,235)
sp=Image.fromarray(c).crop((x0,y0,x1,y1)); sp=sp.resize((sp.width*S,sp.height*S),Image.NEAREST)
nat=Image.open('natief.png').convert('RGB')
X0,Y0,fx,fy,OX,OY=21,12,109/56,123/63,4,1
box=(X0+(x0-OX)*fx,Y0+(y0-OY)*fy,X0+(x1-OX)*fx,Y0+(y1-OY)*fy)
m=nat.transform(sp.size,Image.EXTENT,box,Image.NEAREST)
v=Image.new('RGB',(sp.width*2+10,sp.height),'white'); v.paste(sp,(0,0)); v.paste(m,(sp.width+10,0))
d=ImageDraw.Draw(v)
for k in range(x1-x0+1):
    for off in (0,sp.width+10):
        col=(255,0,0) if (x0+k)%5==0 else (200,200,255)
        d.line([(off+k*S,0),(off+k*S,sp.height)],fill=col,width=1)
for k in range(y1-y0+1):
    col=(255,0,0) if (y0+k)%5==0 else (200,200,255)
    d.line([(0,k*S),(v.width,k*S)],fill=col,width=1)
v.save(o)
