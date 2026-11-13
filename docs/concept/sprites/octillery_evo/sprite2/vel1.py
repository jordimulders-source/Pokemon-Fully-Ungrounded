# vel1.py raster uit.png : snel totaalbeeld: model64 4x | sprite 4x | 2x | 1x (licht en donker)
import cfg,sys
from PIL import Image
a=cfg.read(sys.argv[1]); m=cfg.model64()
BG=(208,208,176,255); DK=(72,80,96,255)
v=Image.new('RGB',(256*2+128+64+40,256+10+140),(255,255,255))
v.paste(m.resize((256,256),Image.NEAREST),(0,0)); v.paste(cfg.rgba(a,BG).resize((256,256),Image.NEAREST),(264,0))
v.paste(cfg.rgba(a,BG).resize((128,128),Image.NEAREST),(528,0)); v.paste(cfg.rgba(a,DK).resize((128,128),Image.NEAREST),(528,132))
v.paste(cfg.rgba(a,BG),(664,0)); v.paste(cfg.rgba(a,DK),(664,70)); v.paste(m,(664,140))
v.paste(m.resize((128,128),Image.NEAREST),(0,266)); 
import os
for i,n in enumerate(['octillery','tentacruel','gyarados','scizor']):
    g=Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/%s/anim_front_gba.png'%n).convert('RGB').crop((0,0,64,64))
    v.paste(g.resize((128,128),Image.NEAREST),(136+i*132,266))
v.save(sys.argv[2])
