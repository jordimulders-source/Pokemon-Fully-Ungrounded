# vel.py rN : octi.png + vel.png (model | sprite 8x | close-ups | 1x licht/donker | naast Octillery Gen 3)
import cfg,sys,os,numpy as np
from PIL import Image,ImageDraw
d=sys.argv[1]; a=cfg.read(d+'/raster.txt'); cfg.topng(a,d+'/octi.png')
src=Image.open(cfg.MODEL).convert('RGB')
def modelcrop(x0,y0,x1,y1,z):
    bx=cfg.X0+(x0-cfg.LEFT)*cfg.S; by=cfg.Y0+(y0-cfg.TOP)*cfg.S
    big=Image.new('RGB',(3000,2000),(255,255,255)); big.paste(src,(1000,1000))
    return big.crop((int(1000+bx),int(1000+by),int(1000+bx+(x1-x0)*cfg.S),int(1000+by+(y1-y0)*cfg.S))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def sp(x0,y0,x1,y1,z,bg=(255,255,255,255)):
    return cfg.rgba(a,bg).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
W=2*512+30; o=Image.new('RGB',(W,1500),(235,235,235)); D=ImageDraw.Draw(o)
D.text((10,4),'model (zelfde schaal)',fill=(0,0,0)); D.text((532,4),d+' sprite 8x',fill=(0,0,0))
o.paste(modelcrop(0,0,64,64,8),(10,18)); o.paste(sp(0,0,64,64,8),(532,18))
y=545
D.text((10,y),'kop: model | sprite (16x)',fill=(0,0,0))
o.paste(modelcrop(17,32,43,52,16),(10,y+14)); o.paste(sp(17,32,43,52,16),(10+26*16+10,y+14))
y2=y+14+20*16+10
D.text((10,y2),'onderste kanon: model | sprite (12x)',fill=(0,0,0))
o.paste(modelcrop(4,48,38,64,12),(10,y2+14)); o.paste(sp(4,48,38,64,12),(10+34*12+10,y2+14))
y3=y2+14+16*12+12
D.text((10,y3),'1x licht / donker',fill=(0,0,0))
im=Image.open(d+'/octi.png').convert('RGBA')
for i,bg in enumerate([(255,255,255),(40,48,64)]):
    b=Image.new('RGB',(64,64),bg); b.paste(im,(0,0),im); o.paste(b,(10+i*74,y3+14))
D.text((200,y3),'8x naast Octillery (Gen 3)',fill=(0,0,0))
oc=Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/octillery/anim_front_gba.png').crop((0,0,64,64)).convert('RGBA')
for i,img in enumerate([oc,im]):
    b=Image.new('RGB',(64,64),(255,255,255)); b.paste(img,(0,0),img); o.paste(b.resize((256,256),Image.NEAREST),(200+i*266,y3+14))
o=o.crop((0,0,W,y3+14+256+10)); o.save(d+'/vel.png'); print(o.size)
