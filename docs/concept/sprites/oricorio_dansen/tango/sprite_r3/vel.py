# vel.png r3: r3 (B) | r2 B | model op 8x ; poten 12x r3|r2 ; 1x licht/donker
import numpy as np; from PIL import Image, ImageDraw
Z=8
def ld(p):
    im=Image.open(p); im.load(); return im.convert('RGBA').crop((0,0,64,64))
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
s3=ld('tango_r3.png'); s2=ld('../sprite_r2/tango_B.png')
a=np.asarray(s3)[:,:,3]; sy,sx=np.where(a>0)
na=np.asarray(Image.open('natief.png').convert('RGB')); bgm=na.min(2)>=225; yy,xx=np.where(~bgm)
nb=Image.fromarray(na).crop((xx.min(),yy.min(),xx.max()+1,yy.max()+1))
mod=Image.new('RGB',(512,512),'white'); m=nb.resize((int(round(nb.width*0.6*Z)),int(round(nb.height*0.6*Z))),Image.NEAREST)
mod.paste(m,((sx.max()+1)*Z-m.width,(sy.max()+1)*Z-m.height))
W=Image.new('RGB',(532*3,512+40+260+40+150),(230,230,230)); d=ImageDraw.Draw(W)
W.paste(op(s3,(255,255,255),Z),(0,30)); d.text((4,8),'r3 tango (B, 8x)',fill='black')
W.paste(op(s2,(255,255,255),Z),(532,30)); d.text((536,8),'r2 tango_B (8x)',fill='black')
W.paste(mod,(1064,30)); d.text((1068,8),'model gemini_r5 (zelfde schaal)',fill='black')
y=600; d.text((4,y-18),'poten/franje 12x: r3 | r2 B',fill='black')
W.paste(op(s3.crop((10,44,42,62)),(255,255,255),12),(0,y)); W.paste(op(s2.crop((10,44,42,62)),(255,255,255),12),(400,y))
y2=y+250; d.text((820,y-18),'1x licht/donker | 2x gevechtsgroen',fill='black')
W.paste(op(s3,(255,255,255),1),(820,y)); W.paste(op(s3,(40,40,48),1),(890,y)); W.paste(op(s3,(152,208,160),2),(970,y))
W.save('vel.png'); print(W.size)
