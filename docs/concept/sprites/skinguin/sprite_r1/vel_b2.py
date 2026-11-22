# vel_B2.png: A | B2 op 8x naast elkaar, daaronder beide op 1x (licht en donker)
from PIL import Image, ImageDraw
G=24; V=Image.new('RGB',(2*512+3*G,512+2*G+30+64+G),(255,255,255)); d=ImageDraw.Draw(V)
def plak(im,x,y,bg):
    t=Image.new('RGBA',im.size,bg); t.alpha_composite(im); V.paste(t.convert('RGB'),(x,y))
for i,n in enumerate(('A','B2')):
    im=Image.open(f'skinguin_{n}.png').convert('RGBA')
    im.resize((512,512),Image.NEAREST).save(f'skinguin_{n}_8x.png')
    plak(im.resize((512,512),Image.NEAREST),G+i*(512+G),G,(232,232,232,255))
    plak(im,G+i*(512+G),512+2*G+30,(248,248,248,255)); plak(im,G+i*(512+G)+64+G,512+2*G+30,(40,44,56,255))
d.text((G,6),'A (8x)',fill=(0,0,0)); d.text((2*G+512,6),'B2: verre ski omlaag, tussenruimte gem 4,4 -> 2,4 px, max 6 -> 3 (8x)',fill=(0,0,0))
d.text((G,512+2*G+12),'1x op licht en donker',fill=(0,0,0))
V.save('vel_B2.png')
