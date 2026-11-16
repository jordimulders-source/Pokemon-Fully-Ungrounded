# Vel r9: r9 | r8 | model 8x; 16x geest+schoorsteen r9 | natief model; overlay ogen+mond; 1x/2x.
from PIL import Image, ImageDraw
def op(f,bg=(255,255,255),crop=None):
    im=Image.open(f).convert('RGBA')
    if crop: im=im.crop(crop)
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
V=Image.new('RGB',(1640,1700),(235,235,235)); d=ImageDraw.Draw(V)
m=Image.open('model/model.webp').convert('RGB'); K=13.77; BX,BY,OY=102,71,2
for i,(im,t) in enumerate([(op('sprite_r9/sprite.png'),'r9'),(op('sprite_r8/sprite.png'),'r8'),
        (m.crop((int(BX),int(BY-OY*K),int(BX+64*K),int(BY+62*K))).resize((512,512),Image.LANCZOS),'model')]):
    V.paste(im.resize((512,512),Image.NEAREST) if im.size[0]==64 else im,(10+i*542,20)); d.text((10+i*542,4),t+' 8x',fill=(0,0,0))
Y=550; Z=16; d.text((10,Y),'geest + schoorsteen 16x: r9 | natief model (rijen r6-28) | overlay ogen+mond (rood = donker in model)',fill=(0,0,0))
V.paste(op('sprite_r9/sprite.png',crop=(7,0,48,21)).resize((41*Z,21*Z),Image.NEAREST),(10,Y+16))
V.paste(Image.open('model/natief.png').convert('RGB').crop((22,6,63,29)).resize((41*Z,23*Z),Image.NEAREST),(10+41*Z+12,Y+16))
Y+=16+23*Z+20; V.paste(Image.open('sprite_r9/overlay.png'),(10,Y))
x=10+720+20
for bg in [(255,255,255),(48,48,64)]:
    s=op('sprite_r9/sprite.png',bg); V.paste(s,(x,Y)); V.paste(s.resize((128,128),Image.NEAREST),(x+70,Y)); x+=210
V=V.crop((0,0,1640,Y+490)); V.save('sprite_r9/vel.png'); print(V.size)
