# vel_ek3.png: ek2 8x | ek3 8x | poten 12x naast Rhydon- en Camerupt-poten 12x | ek3 2x/1x
import numpy as np
from PIL import Image,ImageDraw
R='../../../../../../graphics/pokemon/'
def S(f,bg=(255,255,255)):
    sp=Image.open(f).convert('RGBA'); b=Image.new('RGBA',sp.size,bg+(255,)); b.alpha_composite(sp); return b.convert('RGB')
def G3(n,bg=(255,255,255)):
    im=Image.open(R+n+'/anim_front_gba.png'); L=open(R+n+'/normal_gba.pal').read().split()[3:]
    im.putpalette([int(v) for v in L[:48]]); im.info['transparency']=0
    sp=im.convert('RGBA').crop((0,0,64,64)); b=Image.new('RGBA',sp.size,bg+(255,)); b.alpha_composite(sp); return b.convert('RGB')
Z=12
crops=[('ek3 poten',S('ek3.png').crop((4,47,52,63))),('rhydon poten (Gen 3)',G3('rhydon').crop((20,44,60,62))),('camerupt poten (Gen 3)',G3('camerupt').crop((5,38,60,54)))]
W=max(c.width for _,c in crops)*Z
o=Image.new('RGB',(2*512+30,22+512+20+sum(c.height*Z+20 for _,c in crops)+160),(235,235,235)); d=ImageDraw.Draw(o)
d.text((10,6),'ek2 8x',fill=0); d.text((542,6),'ek3 8x',fill=0)
o.paste(S('ek2.png').resize((512,512),Image.NEAREST),(10,22)); o.paste(S('ek3.png').resize((512,512),Image.NEAREST),(542,22))
y=22+512+20
for t,c in crops:
    d.text((10,y-14),t+' 12x',fill=0); o.paste(c.resize((c.width*Z,c.height*Z),Image.NEAREST),(10,y)); y+=c.height*Z+20
d.text((10,y-6),'ek3 2x / 1x op licht en donker',fill=0)
o.paste(S('ek3.png').resize((128,128),Image.NEAREST),(10,y+8)); o.paste(S('ek3.png',(40,44,52)).resize((128,128),Image.NEAREST),(146,y+8))
o.paste(S('ek3.png'),(282,y+8)); o.paste(S('ek3.png',(40,44,52)),(282,y+76))
o.save('vel_ek3.png')
