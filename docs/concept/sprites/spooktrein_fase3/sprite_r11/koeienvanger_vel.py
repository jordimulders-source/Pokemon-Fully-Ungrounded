# Vel koeienvanger: 16x voorstel | r11 | model (x0-25, y42-61); hele sprite 2x voorstel | model; 1x voorstel | r11 | model.
from PIL import Image, ImageDraw
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
def op(f):
    im=Image.open(f).convert('RGBA'); b=Image.new('RGBA',im.size,(255,255,255,255)); b.alpha_composite(im); return b.convert('RGB')
m=Image.open('model/model.webp').convert('RGB'); K=13.77
def mod(x0,y0,x1,y1,Z): return m.crop((int(102+x0*K),int(71+(y0-2)*K),int(102+x1*K),int(71+(y1-2)*K))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
def spr(f,b,Z): return op(f).crop(b).resize(((b[2]-b[0])*Z,(b[3]-b[1])*Z),Image.NEAREST)
def raster(im,Z):
    d=ImageDraw.Draw(im)
    for i in range(0,im.size[0],Z): d.line([(i,0),(i,im.size[1])],fill=(215,215,215))
    for j in range(0,im.size[1],Z): d.line([(0,j),(im.size[0],j)],fill=(215,215,215))
    return im
b=(0,42,26,62)
rij1=[raster(spr('sprite_r11/voorstel.png',b,16),16),raster(spr('sprite_r11/sprite.png',b,16),16),raster(mod(*b,16),16)]
rij2=[spr('sprite_r11/voorstel.png',(0,0,64,64),2),mod(0,0,64,64,2),spr('sprite_r11/sprite.png',(0,0,64,64),2)]
rij3=[op('sprite_r11/voorstel.png'),op('sprite_r11/sprite.png'),mod(0,0,64,64,2).resize((64,64),Image.BOX)]
W=sum(i.size[0]+16 for i in rij1)+20; H=352+128+64+3*24+40
V=Image.new('RGB',(W,H),(235,235,235)); d=ImageDraw.Draw(V); y=6
for t,r in [('koeienvanger 16x: voorstel | r11 | model',rij1),('hele sprite 2x: voorstel | model | r11',rij2),('1x: voorstel | r11 | model',rij3)]:
    d.text((10,y),t,fill=(0,0,0)); x=10
    for i in r: V.paste(i,(x,y+16)); x+=i.size[0]+16
    y+=max(i.size[1] for i in r)+30
V.save('sprite_r11/koeienvanger_vel.png'); print(V.size)
