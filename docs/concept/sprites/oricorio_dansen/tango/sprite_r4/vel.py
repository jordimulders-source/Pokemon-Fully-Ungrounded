# vel.png r3: r3 (B) | r2 B | model op 8x ; poten 12x r3|r2 ; 1x licht/donker
import numpy as np; from PIL import Image, ImageDraw
Z=8
def ld(p):
    im=Image.open(p); im.load(); return im.convert('RGBA').crop((0,0,64,64))
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
s4=ld('tango_r4.png'); s3=ld('../sprite_r3/tango_r3.png'); s2=ld('../sprite_r2/tango_B.png')
W=Image.new('RGB',(532*3,512+40+260+40),(230,230,230)); d=ImageDraw.Draw(W)
for i,(im,t) in enumerate(((s4,'r4 (8x)'),(s3,'r3 (8x)'),(s2,'r2 B (8x)'))):
    W.paste(op(im,(255,255,255),Z),(i*532,30)); d.text((i*532+4,8),t,fill='black')
y=600; d.text((4,y-18),'franje/poten 12x: r4 | r3 | r2 B',fill='black')
for i,im in enumerate((s4,s3,s2)): W.paste(op(im.crop((10,44,42,62)),(255,255,255),12),(i*400,y))
d.text((1210,y-18),'1x licht/donker | 2x groen',fill='black')
W.paste(op(s4,(255,255,255),1),(1210,y)); W.paste(op(s4,(40,40,48),1),(1280,y)); W.paste(op(s4,(152,208,160),2),(1350,y))
W.save('vel.png'); print(W.size)
