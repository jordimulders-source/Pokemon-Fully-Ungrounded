# vel.png: sprite 8x naast het model (zelfde maat), close-ups 12x, 1x op licht en donker
import sys,numpy as np; from PIL import Image, ImageDraw
from view import rgba
g=np.load(sys.argv[1]); out=sys.argv[2]; g1=np.load('r1.npy')
S=968/62; m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
def modelbox(x0,y0,x1,y1,w,h):
    mb=(24+(x0-1)*S,1+(y0-4)*S,24+(x1-1)*S,1+(y1-4)*S)
    return mw.crop(tuple(int(round(v))+200 for v in mb)).resize((w,h),Image.LANCZOS)
def sp(x0,y0,x1,y1,z,bg=(255,255,255),G=None):
    im=rgba(g if G is None else G).crop((x0,y0,x1,y1)); b=Image.new('RGBA',im.size,bg+(255,)); return Image.alpha_composite(b,im).convert('RGB').resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
W=64*8*3+60
zones=[('hoofd/mond/ogen',(12,20,46,46)),('linkerarm + kruis + bel',(0,15,16,40)),('rechterarm + kruis + bel',(40,10,64,36)),('Shuppet links + draden',(0,36,17,58)),('Shuppet rechts + draden',(44,26,64,63)),('kraag, punt, stomp',(22,42,46,59))]
rows=[]
c=Image.new('RGB',(W,560),'white'); d=ImageDraw.Draw(c)
c.paste(sp(0,0,64,64,8),(10,30)); c.paste(sp(0,0,64,64,8,G=g1),(542,30)); c.paste(modelbox(0,0,64,64,512,512),(1074,30))
d.text((10,8),'r2 8x',fill=(0,0,0)); d.text((542,8),'r1 8x',fill=(0,0,0)); d.text((1074,8),'model (zelfde maat)',fill=(0,0,0))
rows.append(c)
for naam,(x0,y0,x1,y1) in zones:
    z=12; w,h=(x1-x0)*z,(y1-y0)*z
    c=Image.new('RGB',(max(W,3*w+40),h+30),'white'); d=ImageDraw.Draw(c); d.text((10,8),naam+' 12x (r2 | r1 | model)',fill=(0,0,0))
    c.paste(sp(x0,y0,x1,y1,z),(10,25)); c.paste(sp(x0,y0,x1,y1,z,G=g1),(w+20,25)); c.paste(modelbox(x0,y0,x1,y1,w,h),(2*w+30,25)); rows.append(c)
c=Image.new('RGB',(W,180),'white'); d=ImageDraw.Draw(c); d.text((10,4),'1x en 2x op licht en donker',fill=(0,0,0))
c.paste(sp(0,0,64,64,1,(248,248,248)),(10,30)); c.paste(sp(0,0,64,64,1,(40,40,48)),(90,30))
c.paste(sp(0,0,64,64,2,(248,248,248)),(170,30)); c.paste(sp(0,0,64,64,2,(40,40,48)),(310,30))
c.paste(modelbox(0,0,64,64,64,64),(460,30)); c.paste(modelbox(0,0,64,64,128,128),(540,30))
rows.append(c)
H=sum(r.height for r in rows); V=Image.new('RGB',(max(r.width for r in rows),H),'white'); y=0
for r in rows: V.paste(r,(0,y)); y+=r.height
V.save(out); print(V.size)
