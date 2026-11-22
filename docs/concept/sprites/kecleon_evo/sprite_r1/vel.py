# Vel: sprite 8x | verkleind model 8x (zelfde plek, 64x64) | sprite 1x en 2x op licht en donker.
from PIL import Image, ImageDraw
s=Image.open('kecleon_evo_r1.png').convert('RGBA')
m=Image.new('RGBA',(64,64),(0,0,0,0)); m.alpha_composite(Image.open('model_verkleind63.png').convert('RGBA'),(0,1))
BG=(200,206,214,255)
def op(im,c,f):
    t=Image.new('RGBA',im.size,c); t.alpha_composite(im); return t.resize((im.width*f,im.height*f),Image.NEAREST)
W=Image.new('RGBA',(512*2+30+150,512+20),(235,235,235,255))
W.paste(op(s,BG,8),(10,10)); W.paste(op(m,BG,8),(532,10))
x=1054
for i,c in enumerate([(248,248,248,255),(36,36,44,255)]):
    W.paste(op(s,c,2),(x,10+140*i))
    W.paste(op(s,c,1),(x+32,300+80*i))
d=ImageDraw.Draw(W); d.text((14,12),'sprite r1 (8x)',fill=(0,0,0)); d.text((536,12),'verkleind model (8x)',fill=(0,0,0))
W.convert('RGB').save('vel.png')
