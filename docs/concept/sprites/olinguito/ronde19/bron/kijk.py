"""Vergelijking: ronde 18 | samen_f1 | Poochyena | Cyndaquil op 1x en 3x, plus koppen op 8x. kijk.py uit.png"""
import sys
from PIL import Image
S='.123456789abcdef'
pal=[tuple(int(v) for v in r.split('#')[0].split()[1:4]) for r in open('palet.txt') if r.split('#')[0].split()]
def txt(f):
    im=Image.new('RGB',(64,64),(255,255,255))
    for y,l in enumerate(open(f)):
        for x,c in enumerate(l.rstrip('\n')[:64]):
            if c!='.': im.putpixel((x,y),pal[S.index(c)])
    return im
def ref(n):
    im=Image.open('/home/user/projectgrounded/graphics/pokemon/%s/anim_front.png'%n); px=im.load(); rgb=im.convert('RGB')
    o=Image.new('RGB',(64,64),(255,255,255))
    for y in range(64):
        for x in range(64):
            if px[x,y]: o.putpixel((x,y),rgb.getpixel((x,y)))
    return o
ims=[txt('r18_f1.txt'),txt(sys.argv[2] if len(sys.argv)>2 else 'samen_f1.txt'),ref('poochyena'),ref('cyndaquil')]
W=Image.new('RGB',(4*64+4*192+70, 192+20+8*24+10),(255,255,255))
x=0
for im in ims: W.paste(im,(x,60)); x+=68
for im in ims: W.paste(im.resize((192,192),Image.NEAREST),(x,0)); x+=194
x=0
for im,box in [(ims[0],(6,16,42,40)),(ims[1],(6,16,42,40)),(ims[2],(6,10,36,36))]:
    c=im.crop(box); W.paste(c.resize((c.width*8,c.height*8),Image.NEAREST),(x,212)); x+=c.width*8+10
W.save(sys.argv[1])
