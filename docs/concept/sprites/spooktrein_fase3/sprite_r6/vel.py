# Vel r6: r6 | r4 | model (8x); 16x: kleine geest r6 | model-kop (natief, zelfde maat) | Weepinbell/Bellsprout-mond;
# koeienvanger r6 | r4 | model; 1x/2x op licht en donker.
from PIL import Image, ImageDraw
def op(f,bg=(255,255,255),crop=None):
    im=Image.open(f).convert('RGBA');
    if crop: im=im.crop(crop)
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
r6=op('sprite_r6/sprite.png'); r4=op('sprite_r4/sprite.png'); m=Image.open('model/model.webp').convert('RGB')
K=13.77; BX,BY,OY=102,71,2
def mcrop(x0,y0,x1,y1,s): return m.crop((int(BX+x0*K),int(BY+(y0-OY)*K),int(BX+x1*K),int(BY+(y1-OY)*K))).resize((int((x1-x0)*s),int((y1-y0)*s)),Image.LANCZOS)
V=Image.new('RGB',(1760,2400),(235,235,235)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(r6,'r6'),(r4,'r4'),(mcrop(0,0,64,64,8),'model')]):
    V.paste(im.resize((512,512),Image.NEAREST) if im.size[0]==64 else im,(10+i*522,24)); d.text((10+i*522,6),t+' (8x)',fill=(0,0,0))
Y=560; Z=16
d.text((10,Y),'kleine geest 16x: r6 | model (natief raster, 1-op-1) | mondvoorbeeld Weepinbell en Bellsprout (Gen 3, 16x)',fill=(0,0,0))
g=r6.crop((14,0,52,16)).resize((38*Z,16*Z),Image.NEAREST); V.paste(g,(10,Y+16))
n=Image.open('model/natief.png').convert('RGB').crop((29,6,63,22)).resize((34*Z,16*Z),Image.NEAREST); V.paste(n,(10+38*Z+10,Y+16))
x=10+38*Z+10+34*Z+10
for nm,box in (('weepinbell',(12,33,32,52)),('bellsprout',(13,20,25,31))):
    w=op('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/%s/anim_front.png'%nm,crop=box); V.paste(w.resize((w.size[0]*Z,w.size[1]*Z),Image.NEAREST),(x,Y+16)); x+=w.size[0]*Z+10
Y+=16*Z+40
d.text((10,Y),'koeienvanger 16x: r6 | r4 | model',fill=(0,0,0)); x=10
for im in (r6,r4):
    c=im.crop((0,44,26,62)).resize((26*Z,18*Z),Image.NEAREST); V.paste(c,(x,Y+16)); x+=26*Z+10
V.paste(mcrop(0,44,26,62,Z),(x,Y+16)); Y+=18*Z+40
d.text((10,Y),'lijf/kieren 12x: r6 | r4 | model',fill=(0,0,0)); x=10
for im in (r6,r4):
    c=im.crop((20,14,46,40)).resize((26*12,26*12),Image.NEAREST); V.paste(c,(x,Y+16)); x+=26*12+10
V.paste(mcrop(20,14,46,40,12),(x,Y+16)); Y+=26*12+40
d.text((10,Y),'r6 op 1x en 2x, licht en donker',fill=(0,0,0)); x=10
for bg in [(255,255,255),(48,48,64)]:
    s=op('sprite_r6/sprite.png',bg); V.paste(s,(x,Y+16)); V.paste(s.resize((128,128),Image.NEAREST),(x+80,Y+16)); x+=240
V=V.crop((0,0,V.size[0],Y+160)); V.save('sprite_r6/vel.png'); print(V.size)
