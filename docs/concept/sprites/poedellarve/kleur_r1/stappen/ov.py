# ov.py X0 Y0 X1 Y1 z out raster : [sprite | model+grid | model met sprite-lijnen (1/2/3 rood, 4/5 geel stip)]
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poedellarve/kleur_r1/stappen')
from tl import *
X0,Y0,X1,Y1,z=map(int,sys.argv[1:6]); out=sys.argv[6]; rf=sys.argv[7]
pf='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poedellarve/kleur_r1/normal.pal'
R=raster(rf)
spr=grid(rimg(rf,pf).crop((X0,Y0,X1,Y1)).resize(((X1-X0)*z,(Y1-Y0)*z),Image.NEAREST),X0,Y0,z)
m=grid(model(X0,Y0,X1,Y1,z),X0,Y0,z)
o=model(X0,Y0,X1,Y1,z); d=ImageDraw.Draw(o)
for y in range(Y0,Y1):
  for x in range(X0,X1):
    ch=R[y][x]; cx=(x-X0)*z+z//2; cy=(y-Y0)*z+z//2; r=z//5
    if ch in '123': d.rectangle([cx-r,cy-r,cx+r,cy+r],fill=(255,0,0))
    elif ch in '45': d.rectangle([cx-r+1,cy-r+1,cx+r-1,cy+r-1],fill=(255,220,0))
o=grid(o,X0,Y0,z)
ims=[spr,m,o]; W=sum(i.width for i in ims)+20; O=Image.new('RGB',(W,ims[0].height),'white'); x=0
for i in ims: O.paste(i,(x,0)); x+=i.width+10
O.save(out)
