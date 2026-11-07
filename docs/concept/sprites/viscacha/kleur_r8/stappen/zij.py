# zij.py X0 Y0 X1 Y1 z out raster : [sprite+grid | model+grid | model met spritelijnen (1/2/B rood, 8 oranje)]
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r8/stappen')
from tl import *
x0,y0,x1,y1,z=map(int,sys.argv[1:6]); out=sys.argv[6]; R=raster(sys.argv[7])
spr=grid(rimg(R).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),x0,y0,z)
m=grid(model(x0,y0,x1,y1,z),x0,y0,z)
o=model(x0,y0,x1,y1,z); d=ImageDraw.Draw(o)
for y in range(y0,y1):
  for x in range(x0,x1):
    ch=R[y][x]; cx=(x-x0)*z+z//2; cy=(y-y0)*z+z//2; r=max(1,z//6)
    if ch in '12B': d.rectangle([cx-r,cy-r,cx+r,cy+r],fill=(255,0,0))
    elif ch in '8F': d.rectangle([cx-r,cy-r,cx+r,cy+r],fill=(255,140,0))
    elif ch=='.': pass
o=grid(o,x0,y0,z)
ims=[spr,m,o]; W=sum(i.width for i in ims)+20; O=Image.new('RGB',(W,ims[0].height),'white'); x=0
for i in ims: O.paste(i,(x,0)); x+=i.width+10
O.save(out)
