# vel: A | B | model verkleind (kale reductie van het onbewerkte model) op 8x, plus 1x (en 2x) op licht en donker
from PIL import Image,ImageDraw
def rgba(p): return Image.open(p).convert('RGBA')
m0=Image.open('natief.png').convert('RGB'); m=Image.new('RGB',(120,120),'white'); m.paste(m0,(10,10)); S=82/60; oy=63-round(73/S)
mv=m.resize((64,64),Image.BOX,box=(20-2*S,23-oy*S,20+62*S,23+(64-oy)*S)).convert('RGBA')
ims=[rgba('A.png'),rgba('B.png'),mv]; lab=['A (geen mond)','B (mond, naad eroverheen)','model v8 verkleind (box, zelfde raster)']
V=Image.new('RGB',(3*520+20,512+40+150),(255,255,255)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate(zip(ims,lab)):
    b=Image.new('RGBA',(64,64),(255,255,255,255)); b.alpha_composite(im); V.paste(b.resize((512,512),Image.NEAREST).convert('RGB'),(10+i*520,30)); d.text((10+i*520,10),t,fill=(0,0,0))
x=10
for bgc in ((248,248,240),(40,48,64)):
    for im in ims[:2]:
        for z in (1,2):
            b=Image.new('RGBA',(64*z,64*z),bgc+(255,)); b.alpha_composite(im.resize((64*z,64*z),Image.NEAREST)); V.paste(b.convert('RGB'),(x,560)); x+=64*z+10
V.save('vel.png')
