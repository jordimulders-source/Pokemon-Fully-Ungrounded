# modelcrop.py x0 x1 y0 y1 UIT: sprite-gebied naast hetzelfde gebied in het natieve model (beide 12x per spritepixel)
import sys; sys.path.insert(0,'sprite_r9'); from gemeen2 import *; from PIL import Image
x0,x1,y0,y1=map(int,sys.argv[1:5]); uit=sys.argv[5]; src=sys.argv[6] if len(sys.argv)>6 else 'sprite_r10/guarana2_r10a.png'
Z=12
m=Image.open(NATIEF).convert('RGB'); u0=(x0-X0)/S+U0; v0=(y0-Y0)/S+V0; u1=(x1-X0)/S+U0; v1=(y1-Y0)/S+V0
mc=m.crop((int(u0),int(v0),int(u1),int(v1))).resize(((x1-x0)*Z,(y1-y0)*Z),0)
a=Image.open(src); a.info['transparency']=0; a=a.convert('RGBA'); B=Image.new('RGBA',a.size,(255,255,255,255)); B.alpha_composite(a)
c=B.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),0)
T=Image.new('RGB',(c.width*2+10,c.height),'white'); T.paste(c,(0,0)); T.paste(mc,(c.width+10,0)); T.save(uit)
