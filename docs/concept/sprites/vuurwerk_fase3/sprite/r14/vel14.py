# vel.png r14: per probeersel linkeroog 16x naast het rechteroog; kop 8x (1-6 + r12 p2); hele sprite 1x (2x getoond).
import numpy as np, json; from PIL import Image, ImageDraw
PAL=json.load(open('../r9/palet.json'))
def rgba(f):
    s=np.asarray(Image.open(f)).astype(int); c=np.zeros((64,64,4),np.uint8); c[...,:3]=np.array(PAL,np.uint8)[s]; c[...,3]=(s>0)*255
    return Image.fromarray(c,'RGBA')
def op(im,c=(255,255,255,255)): b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
fs=[('%d'%n,'sprite_%d.png'%n) for n in range(1,7)]+[('r12 p2','../r12/sprite_B_p2.png')]
KW,KH,Z=26,30,8
vel=Image.new('RGB',(7*(KW*Z+12)+30,40+8*16+40+KH*Z+40+138+20),(232,232,232)); d=ImageDraw.Draw(vel)
y=10; d.text((20,y),'16x: linkeroog (x3-7, y19-25) | rechteroog (x10-15, y18-24), per probeersel',fill=0); y+=16
for i,(lab,f) in enumerate(fs):
    s=op(rgba(f)); x=20+i*(KW*Z+12)
    vel.paste(s.crop((3,19,7,25)).resize((64,96),Image.NEAREST),(x,y+16)); vel.paste(s.crop((10,18,16,24)).resize((96,96),Image.NEAREST),(x+76,y+16))
    d.text((x,y),lab,fill=0)
y+=96+40; d.text((20,y),'kop 8x: 1 | 2 | 3 | 4 | 5 | 6 | r12 p2',fill=0); y+=16
for i,(lab,f) in enumerate(fs):
    vel.paste(op(rgba(f)).crop((0,2,KW,KH+2)).resize((KW*Z,KH*Z),Image.NEAREST),(20+i*(KW*Z+12),y)); d.text((24+i*(KW*Z+12),y+2),lab,fill=(0,0,255))
y+=KH*Z+24; d.text((20,y),'1x (2x getoond): 1 2 3 4 5 6 r12p2',fill=0); y+=16
for i,(lab,f) in enumerate(fs): vel.paste(op(rgba(f),(248,248,248,255)).resize((128,128),Image.NEAREST),(20+i*138,y))
vel.save('vel.png'); print(vel.size)
