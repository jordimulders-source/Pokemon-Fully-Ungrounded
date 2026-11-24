"""Maakt capykart_r7_8x.png en vel.png (r6 | r7 | capybarrel af op 8x, plus 1x op licht/donker)."""
from PIL import Image, ImageDraw
import os
D=os.path.dirname(os.path.abspath(__file__))
def rgba(p):
    im=Image.open(p); pal=im.getpalette(); px=im.load()
    o=Image.new('RGBA',im.size,(0,0,0,0)); po=o.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            i=px[x,y]
            if i: po[x,y]=tuple(pal[3*i:3*i+3])+(255,)
    return o
r6=rgba(os.path.join(D,'..','sprite','r6','capykart.png'))
r7=rgba(os.path.join(D,'capykart_r7.png'))
cb=rgba(os.path.join(D,'..','..','capybarrel','af','capybarrel.png'))
big=lambda im,k=8: im.resize((im.width*k,im.height*k),Image.NEAREST)
r7_8=Image.new('RGBA',(512,512),(255,255,255,255)); r7_8.alpha_composite(big(r7)); r7_8.convert('RGB').save(os.path.join(D,'capykart_r7_8x.png'))
BG=(236,236,236,255); W=3*512+4*16; H=512+40+16+80+16
v=Image.new('RGBA',(W,H),BG); d=ImageDraw.Draw(v)
for i,(im,t) in enumerate([(r6,'r6 (voor)'),(r7,'r7 (omlijningsronde)'),(cb,'capybarrel af (maatstaf)')]):
    x=16+i*(512+16)
    tile=Image.new('RGBA',(512,512),(255,255,255,255)); tile.alpha_composite(big(im)); v.paste(tile,(x,24))
    d.text((x,6),t,fill=(0,0,0,255))
    for j,bg in enumerate([(255,255,255,255),(40,40,48,255)]):
        s=Image.new('RGBA',(72,72),bg); s.alpha_composite(im,(4,4)); v.paste(s,(x+j*84,24+512+24))
v.convert('RGB').save(os.path.join(D,'vel.png'))
