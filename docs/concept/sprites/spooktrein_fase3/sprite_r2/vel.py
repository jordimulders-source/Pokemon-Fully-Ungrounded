# Vel r2: r2 8x | r1 8x | model verkleind; close-ups 12x (sprite | model, zelfde uitsnede); 1x en 2x op licht en donker.
from PIL import Image, ImageDraw
def op(f,bg=(255,255,255)):
    im=Image.open(f).convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
r2=op('sprite.png'); r1=op('../sprite_r1/sprite.png'); m=Image.open('../model/model.webp').convert('RGB')
K=13.77; BX,BY,OY=102,71,2           # sprite (x,y) -> model (BX+x*K, BY+(y-OY)*K)
def mcrop(x0,y0,x1,y1,s): return m.crop((int(BX+x0*K),int(BY+(y0-OY)*K),int(BX+x1*K),int(BY+(y1-OY)*K))).resize(((x1-x0)*s,(y1-y0)*s),Image.LANCZOS)
mm=Image.new('RGB',(512,512),'white'); mm.paste(mcrop(0,0,64,64,8),(0,0))
V=Image.new('RGB',(3*524+12,560+4*330+200),(235,235,235)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(r2,'r2 (8x)'),(r1,'r1 (8x)'),(mm,'model verkleind (zelfde uitsnede)')]):
    V.paste(im.resize((512,512),Image.NEAREST) if im.size[0]==64 else im,(12+i*524,28)); d.text((12+i*524,8),t,fill=(0,0,0))
Y=560
for naam,(x0,y0,x1,y1) in [('gezicht',(0,24,30,46)),('koeienvanger',(0,44,27,62)),('kleine geest',(12,0,40,14)),('wolkpunten',(40,14,64,50))]:
    s=12 if (x1-x0)<=30 else 10; h=(y1-y0)*s
    d.text((12,Y),naam+' %dx: r2 | r1 | model'%s,fill=(0,0,0))
    x=12
    for im in [r2.crop((x0,y0,x1,y1)).resize(((x1-x0)*s,h),Image.NEAREST),r1.crop((x0,y0,x1,y1)).resize(((x1-x0)*s,h),Image.NEAREST),mcrop(x0,y0,x1,y1,s)]:
        V.paste(im,(x,Y+16)); x+=im.size[0]+12
    Y+=h+30
d.text((12,Y),'r2 op 1x en 2x, licht en donker',fill=(0,0,0)); x=12
for bg in [(255,255,255),(48,48,64)]:
    s=op('sprite.png',bg); V.paste(s,(x,Y+16)); V.paste(s.resize((128,128),Image.NEAREST),(x+80,Y+16)); x+=240
V=V.crop((0,0,V.size[0],Y+160)); V.save('vel.png'); print(V.size)
