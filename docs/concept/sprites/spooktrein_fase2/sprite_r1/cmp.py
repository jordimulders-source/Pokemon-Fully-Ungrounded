# vergelijk: sprite-regio op 12x naast hetzelfde stuk van het model (natief raster, zelfde schaal)
import sys; from PIL import Image; import numpy as np
VAR,x0,y0,x1,y1=sys.argv[1],*map(int,sys.argv[2:6]); OUT=sys.argv[6]
sp=Image.open(f'{VAR}.png').convert('RGBA'); bg=Image.new('RGBA',sp.size,'white'); sp=Image.alpha_composite(bg,sp).convert('RGB')
Z=12; a=sp.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
# modelstuk: zelfde gebied terugrekenen via schaal uit meta
s,X0,Y0,oy,XC,k=[float(v) for v in open(f'{VAR}.meta').read().split()]
def inv(u): return X0+u if u<XC-X0 else XC+(u-(XC-X0))/k
mx0,mx1=inv(x0/s),inv(x1/s); my0,my1=Y0+(y0-oy)/s,Y0+(y1-oy)/s
m=Image.open('natief.png').crop((int(mx0),int(my0),int(np.ceil(mx1)),int(np.ceil(my1)))).resize(a.size,Image.NEAREST)
v=Image.new('RGB',(a.width*2+10,a.height),'white'); v.paste(a,(0,0)); v.paste(m,(a.width+10,0)); v.save(OUT)
