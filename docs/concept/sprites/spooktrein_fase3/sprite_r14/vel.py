# Vel r14: r14 | r13 | model 8x; koeienvanger 12x met Jordi's schetslijnen (rood) erover: r14 | r13 | model; wolken rechts 12x r14 | r13; 1x/2x.
import sys; sys.path.insert(0,'sprite_r14')
from PIL import Image, ImageDraw; import numpy as np
from jordi_lijnen import lijnpixels
def op(f,bg=(255,255,255)):
    im=Image.open(f).convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
m=Image.open('model/model.webp').convert('RGB'); K=13.77
def mod(x0,y0,x1,y1,Z,dx=2): # model op het r14-raster (r14 = r13 + 2 px naar rechts)
    X=102+(x0-dx)*K; Y=71+(y0-2)*K
    return m.crop((int(X),int(Y),int(X+(x1-x0)*K),int(Y+(y1-y0)*K))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
def spr(f,box,Z): return op(f).crop(box).resize(((box[2]-box[0])*Z,(box[3]-box[1])*Z),Image.NEAREST)
P=[(sx,sy) for sx,sy in lijnpixels() if 0<=sx<26 and 42<=sy<62]
def schets(im,box,Z,dx):
    d=ImageDraw.Draw(im)
    for sx,sy in P:
        X=(sx+dx-box[0])*Z; Y=(sy-box[1])*Z; d.point((X,Y),fill=(255,0,0))
    return im
R14,R13='sprite_r14/sprite.png','sprite_r13/sprite.png'
kb=(0,42,28,62); kb13=(0,42,28,62)
rows=[('r14 | r13 | model, 8x',[spr(R14,(0,0,64,64),8),spr(R13,(0,0,64,64),8),mod(0,0,64,64,8)]),
      ('koeienvanger 12x, rood = Jordi\'s schets (alleen ter vergelijking): r14 | r13 | model',
       [schets(spr(R14,kb,12),kb,12,2),schets(spr(R13,kb13,12),kb13,12,0),schets(mod(*kb,12),kb,12,2)]),
      ('wolkpunten rechts 12x (r14 x46-63 | r13 x44-63)',[spr(R14,(46,18,64,42),12),spr(R13,(44,18,64,42),12)])]
W=max(sum(i.size[0]+16 for i in r) for _,r in rows)+20; H=sum(max(i.size[1] for i in r)+30 for _,r in rows)+180
V=Image.new('RGB',(W,H),(235,235,235)); d=ImageDraw.Draw(V); y=6
for t,r in rows:
    d.text((10,y),t,fill=(0,0,0)); x=10
    for i in r: V.paste(i,(x,y+16)); x+=i.size[0]+16
    y+=max(i.size[1] for i in r)+30
x=10; d.text((10,y),'1x / 2x op licht en donker: r14 | r13',fill=(0,0,0))
for f in [R14,R13]:
    for bg in [(255,255,255),(48,48,64)]:
        s=op(f,bg); V.paste(s,(x,y+16)); V.paste(s.resize((128,128),Image.NEAREST),(x+70,y+16)); x+=220
V.save('sprite_r14/vel.png'); print(V.size)
