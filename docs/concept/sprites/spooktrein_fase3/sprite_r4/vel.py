# Vel r4: r4 | r3 | model (6x); close-ups 12x r4 | r3 | model (koeienvanger, lijf-roest, kleine geest, gezicht); 1x/2x.
from PIL import Image, ImageDraw
def op(f,bg=(255,255,255)):
    im=Image.open(f).convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
r4=op('sprite.png'); r3=op('../sprite_r3/sprite.png'); m=Image.open('../model/model.webp').convert('RGB')
K=13.77; BX,BY,OY=102,71,2
def mcrop(x0,y0,x1,y1,s): return m.crop((int(BX+x0*K),int(BY+(y0-OY)*K),int(BX+x1*K),int(BY+(y1-OY)*K))).resize(((x1-x0)*s,(y1-y0)*s),Image.LANCZOS)
V=Image.new('RGB',(3*400+20,2600),(235,235,235)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(r4,'r4'),(r3,'r3'),(mcrop(0,0,64,64,6),'model')]):
    V.paste(im.resize((384,384),Image.NEAREST) if im.size[0]==64 else im,(10+i*400,24)); d.text((10+i*400,6),t+' (6x)',fill=(0,0,0))
Y=420
for naam,(x0,y0,x1,y1) in [('koeienvanger',(0,44,26,62)),('lijf-roest',(20,14,46,40)),('kleine geest',(12,0,42,15)),('gezicht (bevroren, alleen ooglid)',(0,27,26,49))]:
    s=12; h=(y1-y0)*s; d.text((10,Y),naam+' 12x: r4 | r3 | model',fill=(0,0,0)); x=10
    for im in [r4,r3]:
        c=im.crop((x0,y0,x1,y1)).resize(((x1-x0)*s,h),Image.NEAREST); V.paste(c,(x,Y+16)); x+=c.size[0]+10
    V.paste(mcrop(x0,y0,x1,y1,s),(x,Y+16)); Y+=h+30
d.text((10,Y),'r4 op 1x en 2x, licht en donker',fill=(0,0,0)); x=10
for bg in [(255,255,255),(48,48,64)]:
    s=op('sprite.png',bg); V.paste(s,(x,Y+16)); V.paste(s.resize((128,128),Image.NEAREST),(x+80,Y+16)); x+=240
V=V.crop((0,0,V.size[0],Y+160)); V.save('vel.png'); print(V.size)
