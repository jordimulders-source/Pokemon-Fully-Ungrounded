# vel: B115 | B130 | r2 B | Pincurchin-mond (8x), plus 1x/2x op licht en donker
from PIL import Image,ImageDraw
def rgba(p): return Image.open(p).convert('RGBA')
pin=Image.open('../../../../../../graphics/pokemon/pincurchin/anim_front.png').convert('RGBA').crop((0,0,64,64))
ims=[rgba('B115.png'),rgba('B130.png'),rgba('../r2/B.png'),pin]; lab=['B115','B130','r2 B','Pincurchin (mond x16-26, y37-45)']
V=Image.new('RGB',(4*400+10,384+40+150),'white'); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate(zip(ims,lab)):
    b=Image.new('RGBA',(64,64),(255,255,255,255)); b.alpha_composite(im)
    V.paste(b.resize((384,384),Image.NEAREST).convert('RGB'),(10+i*400,30)); d.text((10+i*400,12),t,fill=(0,0,0))
x=10
for bgc in ((248,248,240),(40,48,64)):
    for im in ims[:2]:
        for z in (1,2):
            b=Image.new('RGBA',(64*z,64*z),bgc+(255,)); b.alpha_composite(im.resize((64*z,64*z),Image.NEAREST)); V.paste(b.convert('RGB'),(x,430)); x+=64*z+10
V.save('vel.png')
