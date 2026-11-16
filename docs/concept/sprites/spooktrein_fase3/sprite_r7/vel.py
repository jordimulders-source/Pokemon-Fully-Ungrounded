# Vel r7: kop 16x A | B | origineel (geest_kop_zoom) | Weepinbell-mond; daaronder A en B op 1x, 2x, 8x.
from PIL import Image, ImageDraw
def op(f,bg=(255,255,255),crop=None):
    im=Image.open(f).convert('RGBA')
    if crop: im=im.crop(crop)
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
Z=16; V=Image.new('RGB',(2200,1400),(235,235,235)); d=ImageDraw.Draw(V)
d.text((10,4),'kop kleine geest 16x: A (mond als model) | B (Weepinbell-opbouw) | origineel geest_kop_zoom | Weepinbell',fill=(0,0,0))
x=10; box=(14,0,40,16)
for v in 'AB':
    c=op('sprite_r7/sprite_%s.png'%v,crop=box).resize((26*Z,16*Z),Image.NEAREST); V.paste(c,(x,20)); d.text((x,20+16*Z+2),v,fill=(0,0,0)); x+=26*Z+12
k=Image.open('model/geest_kop_zoom.png').convert('RGB'); k=k.resize((int(k.width*16*Z/k.height),16*Z)); V.paste(k,(x,20)); x+=k.width+12
w=op('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/weepinbell/anim_front.png',crop=(12,33,32,52)); V.paste(w.resize((20*Z//2*1,19*Z//2*1),Image.NEAREST) if False else w.resize((w.width*Z//1*1//1,w.height*Z),Image.NEAREST).resize((w.width*Z*16//19//1,16*Z)),(x,20))
Y=20+16*Z+30
for v in 'AB':
    d.text((10,Y),'variant %s: 1x, 2x (licht/donker) en 8x'%v,fill=(0,0,0)); x=10
    for bg in [(255,255,255),(48,48,64)]:
        s=op('sprite_r7/sprite_%s.png'%v,bg); V.paste(s,(x,Y+16)); V.paste(s.resize((128,128),Image.NEAREST),(x+70,Y+16)); x+=210
    V.paste(op('sprite_r7/sprite_%s.png'%v).resize((512,512),Image.NEAREST),(x,Y+16)); Y+=16+512+20
V=V.crop((0,0,2200,Y)); V.save('sprite_r7/vel.png'); print(V.size)
