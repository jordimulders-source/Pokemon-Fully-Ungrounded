# raster.py x0 y0 x1 y1 UIT [SPRITE]: model (natief, 1024-plaatje) met het spriteraster erover, z=24 per spritepixel; optioneel de sprite ernaast
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
x0,y0,x1,y1=map(int,sys.argv[1:5]); z=int(__import__("os").environ.get("Z","24"))
M=Image.open(MODEL).convert('RGB'); f=lambda u,ph:ph+0.5+P*u
u0=(x0-X0)/S+U0; u1=(x1-X0)/S+U0; v0=(y0-Y0)/S+V0; v1=(y1-Y0)/S+V0
a=M.crop((int(f(u0,FX)),int(f(v0,FY)),int(f(u1,FX)),int(f(v1,FY)))).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
d=ImageDraw.Draw(a)
for i,x in enumerate(range(0,a.width,z)):
    d.line([(x,0),(x,a.height)],fill=(0,160,255)); d.text((x+2,2),str(x0+i),fill=(0,90,200))
for j,y in enumerate(range(0,a.height,z)):
    d.line([(0,y),(a.width,y)],fill=(0,160,255)); d.text((2,y+2),str(y0+j),fill=(0,90,200))
if len(sys.argv)>6:
    sp=Image.open(sys.argv[6]); o=np.asarray(sp); pal=np.array(sp.getpalette()[:48]).reshape(-1,3)
    img=np.full((64,64,3),255,'uint8')
    for k in range(1,16): img[o==k]=pal[k]
    b=Image.fromarray(img).crop((x0,y0,x1,y1)).resize(a.size,Image.NEAREST); d2=ImageDraw.Draw(b)
    for x in range(0,b.width,z): d2.line([(x,0),(x,b.height)],fill=(200,200,200))
    for y in range(0,b.height,z): d2.line([(0,y),(b.width,y)],fill=(200,200,200))
    v=Image.new('RGB',(a.width*2+10,a.height),'white'); v.paste(a,(0,0)); v.paste(b,(a.width+10,0)); a=v
a.save(sys.argv[5])
