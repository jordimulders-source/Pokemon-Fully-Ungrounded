# vel.png: sprite 8x naast het model (zelfde maat), close-ups 12x, 1x op licht en donker
import sys,numpy as np; from PIL import Image, ImageDraw
from view import rgba
g=np.load(sys.argv[1]); out=sys.argv[2]
S=968/62; m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
def modelbox(x0,y0,x1,y1,w,h):
    mb=(24+(x0-1)*S,1+(y0-4)*S,24+(x1-1)*S,1+(y1-4)*S)
    return mw.crop(tuple(int(round(v))+200 for v in mb)).resize((w,h),Image.LANCZOS)
def sp(x0,y0,x1,y1,z,bg=(255,255,255)):
    im=rgba(g).crop((x0,y0,x1,y1)); b=Image.new('RGBA',im.size,bg+(255,)); return Image.alpha_composite(b,im).convert('RGB').resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
W=64*8*2+40
zones=[('hoofd/mond/ogen',(12,20,46,44)),('linkerarm + kruis',(0,15,16,34)),('rechterarm + kruis',(42,13,64,36)),('Shuppet links',(2,37,17,57)),('Shuppet rechts',(45,41,63,63))]
rows=[]
c=Image.new('RGB',(W,560),'white'); d=ImageDraw.Draw(c)
c.paste(sp(0,0,64,64,8),(10,30)); c.paste(modelbox(0,0,64,64,512,512),(10+512+20,30))
d.text((10,8),'sprite 8x',fill=(0,0,0)); d.text((542,8),'model (zelfde maat)',fill=(0,0,0))
rows.append(c)
for naam,(x0,y0,x1,y1) in zones:
    z=12; w,h=(x1-x0)*z,(y1-y0)*z
    c=Image.new('RGB',(max(W,2*w+30),h+30),'white'); d=ImageDraw.Draw(c); d.text((10,8),naam+' 12x',fill=(0,0,0))
    c.paste(sp(x0,y0,x1,y1,z),(10,25)); c.paste(modelbox(x0,y0,x1,y1,w,h),(w+20,25)); rows.append(c)
c=Image.new('RGB',(W,180),'white'); d=ImageDraw.Draw(c); d.text((10,4),'1x en 2x op licht en donker',fill=(0,0,0))
c.paste(sp(0,0,64,64,1,(248,248,248)),(10,30)); c.paste(sp(0,0,64,64,1,(40,40,48)),(90,30))
c.paste(sp(0,0,64,64,2,(248,248,248)),(170,30)); c.paste(sp(0,0,64,64,2,(40,40,48)),(310,30))
c.paste(modelbox(0,0,64,64,64,64),(460,30)); c.paste(modelbox(0,0,64,64,128,128),(540,30))
rows.append(c)
H=sum(r.height for r in rows); V=Image.new('RGB',(max(r.width for r in rows),H),'white'); y=0
for r in rows: V.paste(r,(0,y)); y+=r.height
V.save(out); print(V.size)
