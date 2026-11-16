# Vel r8: kop 16x r8 | r4 | natief model (zelfde schaal als r8) | model 2x; hele sprite r8 | model 8x; 1x/2x.
from PIL import Image, ImageDraw
def op(f,bg=(255,255,255),crop=None):
    im=Image.open(f).convert('RGBA')
    if crop: im=im.crop(crop)
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
Z=16; V=Image.new('RGB',(2300,1500),(235,235,235)); d=ImageDraw.Draw(V)
d.text((10,4),'kop 16x: r8 | r4 | natief model (zelfde schaal als r8) | origineel 2x (LANCZOS)',fill=(0,0,0)); x=10
c=op('sprite_r8/sprite.png',crop=(14,0,44,16)); V.paste(c.resize((30*Z,16*Z),Image.NEAREST),(x,20)); x+=30*Z+12
c=op('sprite_r4/sprite.png',crop=(10,0,40,16)); V.paste(c.resize((30*Z,16*Z),Image.NEAREST),(x,20)); x+=30*Z+12
c=Image.open('sprite_r8/model_geschaald.png').crop((0,0,30,16)); V.paste(c.resize((30*Z,16*Z),Image.NEAREST),(x,20)); x+=30*Z+12
k=Image.open('sprite_r8/model_kop_2x.png').crop((120,40,800,300)); V.paste(k.resize((int(k.width*256/k.height),256)),(x,20))
Y=300; d.text((10,Y),'r8 | model, 8x; daaronder r8 1x/2x licht en donker',fill=(0,0,0))
V.paste(op('sprite_r8/sprite.png').resize((512,512),Image.NEAREST),(10,Y+16))
m=Image.open('model/model.webp').convert('RGB'); K=13.77; BX,BY,OY=102,71,2
V.paste(m.crop((int(BX),int(BY-OY*K),int(BX+64*K),int(BY+62*K))).resize((512,512),Image.LANCZOS),(534,Y+16))
V.paste(Image.open('sprite_r8/overlay.png'),(1060,Y+16)); d.text((1060,Y+16+390),'overlay: rood = donker in geschaald model, blauw = zone ogen+mond',fill=(0,0,0))
Y+=16+512+20; x=10
for bg in [(255,255,255),(48,48,64)]:
    s=op('sprite_r8/sprite.png',bg); V.paste(s,(x,Y)); V.paste(s.resize((128,128),Image.NEAREST),(x+70,Y)); x+=210
V=V.crop((0,0,2300,Y+140)); V.save('sprite_r8/vel.png'); print(V.size)
