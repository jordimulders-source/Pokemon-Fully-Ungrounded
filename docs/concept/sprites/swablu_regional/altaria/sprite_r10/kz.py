# kz.py: kop-close-up 20x: r10 | echte Altaria-kop (X18-40, Y10-28). python3 sprite_r10/kz.py sprite.png uit.png
import sys; from PIL import Image, ImageDraw
Z=20
def plat(p,crop):
    im=Image.open(p).convert('RGBA'); im=im.crop((0,0,64,64)); b=Image.new('RGBA',(64,64),(255,255,255,255)); b.alpha_composite(im)
    return b.convert('RGB').crop(crop).resize(((crop[2]-crop[0])*Z,(crop[3]-crop[1])*Z),Image.NEAREST)
a=plat(sys.argv[1],(15,14,37,32)); b=plat('../../../../../graphics/pokemon/altaria/anim_front.png',(17,10,39,28))
out=Image.new('RGB',(a.width*2+20,a.height+16),'white'); out.paste(a,(0,16)); out.paste(b,(a.width+20,16))
d=ImageDraw.Draw(out)
for i in range(22):
    d.text((i*Z+4,2),str((15+i)%100),fill=(200,0,0)); d.text((a.width+20+i*Z+4,2),str((17+i)%100),fill=(200,0,0))
for j in range(18): d.text((2,16+j*Z+4),str(14+j),fill=(200,0,0))
out.save(sys.argv[2])
