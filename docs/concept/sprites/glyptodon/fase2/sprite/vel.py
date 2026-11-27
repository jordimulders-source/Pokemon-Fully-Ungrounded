# vel.py rN : sprite 8x | model verkleind 8x ; close-ups 12x (stekel+band, staartaanzet, kop/oog: sprite | model) ; 1x op licht en donker
import sys,numpy as np
from PIL import Image,ImageDraw
from vergelijk import model1x
r=sys.argv[1]
sp=Image.open(r+'.png').convert('RGBA')
def op(bg): b=Image.new('RGBA',(64,64),bg); b.alpha_composite(sp); return b.convert('RGB')
m=model1x()
L=op((255,255,255,255))
W=64*8*2+24; secties=[('stekel + band',(9,5,29,27)),('staartaanzet',(40,38,62,56)),('kop / oog',(0,35,26,50))]
hs=[ (y1-y0)*12 for _,(x0,y0,x1,y1) in secties]
H=64*8+20+sum(h+20 for h in hs)+90
o=Image.new('RGB',(max(W,2*22*12+40),H),(235,235,235)); d=ImageDraw.Draw(o)
d.text((4,2),r+' (8x)',fill=0); d.text((64*8+16,2),'model verkleind (8x)',fill=0)
o.paste(L.resize((512,512),Image.NEAREST),(4,16)); o.paste(m.resize((512,512),Image.NEAREST),(64*8+16,16))
y=16+512+8
for (nm,(x0,y0,x1,y1)),h in zip(secties,hs):
    d.text((4,y),nm+f'  x{x0}-{x1-1} y{y0}-{y1-1}  (12x: sprite | model)',fill=0); y+=14
    w=(x1-x0)*12
    o.paste(L.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(4,y)); o.paste(m.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(w+16,y))
    y+=h+6
d.text((4,y),'1x op licht en donker',fill=0); y+=14
o.paste(op((248,248,248,255)),(4,y)); o.paste(op((40,44,52,255)),(80,y)); o.paste(op((96,160,112,255)),(156,y))
o=o.crop((0,0,o.width,y+70)); o.save('vel_'+r+'.png')
