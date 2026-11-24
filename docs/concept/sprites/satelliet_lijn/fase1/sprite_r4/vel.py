# vel.py: r4 8x | r3 8x ; r4 en r3 op 1x en 2x op licht/donker/groen ; oog r4 12x | model 12x (zelfde schaal)
from PIL import Image, ImageDraw
f=0.617; X0,Y0,OX,OY=17,16,9,14
src=Image.open('../model/model_gekozen_natief.png').convert('RGB')
padd=Image.new('RGB',(299,299),'white'); padd.paste(src,(100,100))
x0=X0-OX/f+100; y0=Y0-OY/f+100; k=1/f
big=padd.resize((2990,2990),Image.NEAREST)
m=big.crop((int(x0*10),int(y0*10),int((x0+64*k)*10),int((y0+64*k)*10))).resize((64,64),Image.BOX)
def ld(path):
    p=Image.open(path); p.save('/tmp/claude-0/sat/_vl.png',transparency=0); return Image.open('/tmp/claude-0/sat/_vl.png').convert('RGBA')
s4=ld('sprite.png'); s3=ld('../sprite_r3/sprite.png')
def on(s,c):
    b=Image.new('RGBA',(64,64),c+(255,)); b.alpha_composite(s); return b.convert('RGB')
G=(152,208,160); LI=(248,248,248); DK=(40,40,48)
o=Image.new('RGB',(1040,1160),(250,250,250)); d=ImageDraw.Draw(o)
o.paste(on(s4,G).resize((512,512),Image.NEAREST),(0,0)); o.paste(on(s3,G).resize((512,512),Image.NEAREST),(528,0))
d.text((4,514),'r4 (8x) - ±985 px',fill=(0,0,0)); d.text((532,514),'r3 (8x) - 1548 px',fill=(0,0,0))
yy=540
for i,c in enumerate((LI,DK,G)):
    o.paste(on(s4,c),(10+i*150,yy)); o.paste(on(s3,c),(80+i*150,yy))
d.text((10,yy+68),'1x: r4 | r3 op licht / donker / groen',fill=(0,0,0))
yy=630
for i,c in enumerate((LI,DK)):
    o.paste(on(s4,c).resize((128,128),Image.NEAREST),(10+i*290,yy)); o.paste(on(s3,c).resize((128,128),Image.NEAREST),(146+i*290,yy))
d.text((10,yy+130),'2x: r4 | r3 op licht en donker',fill=(0,0,0))
box=(8,28,23,43); z=12; w=(box[2]-box[0])*z; h=(box[3]-box[1])*z; yy=790
o.paste(on(s4,G).crop(box).resize((w,h),Image.NEAREST),(0,yy)); o.paste(m.crop(box).resize((w,h),Image.NEAREST),(w+16,yy))
d.text((2*w+30,yy+4),'oog r4 12x | model zelfde schaal',fill=(0,0,0))
o.save('vel.png')
w8=Image.new('RGBA',(512,512),(255,255,255,255)); w8.alpha_composite(s4.resize((512,512),Image.NEAREST)); w8.convert('RGB').save('sprite_8x_wit.png')
