# vel.png r4: r4 | r3 | model op 8x ; poten 12x: r4 | r3 | Pa'u | Sensu ; r4 en r3 op 1x licht/donker
import numpy as np; from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/oricorio/'
def rgba(p): return Image.open(p).convert('RGBA')
def f1(p): return rgba(p).crop((0,0,64,64))
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
r4=rgba('cumbia.png'); r3=rgba('r3_ref.png'); o=np.load('cumbia_kls.npy')
na=np.asarray(Image.open('natief.png').convert('RGB')); bgm=na.min(2)>=225; yy,xx=np.where(~bgm)
nb=Image.fromarray(na).crop((xx.min(),yy.min(),xx.max()+1,yy.max()+1)); sy,sx=np.where(o>0)
m=nb.resize(((sx.max()-sx.min()+1)*8,(sy.max()-sy.min()+1)*8),Image.NEAREST)
mod=Image.new('RGB',(512,512),'white'); mod.paste(m,(sx.min()*8,3*8))
W=Image.new('RGB',(3*522,30+512+40+192+40+140),(230,230,230)); d=ImageDraw.Draw(W)
for k,(im,t) in enumerate([(op(r4,'white',8),'r4 (poten + voeten van Pa\'u)'),(op(r3,'white',8),'r3'),(mod,'model gemini_r2 (ter info)')]):
    W.paste(im,(k*522,30)); d.text((k*522+4,8),t,fill='black')
y=572; d.text((4,y),'poten 12x: r4 | r3 | Pa\'u | Sensu (Gen 3, frame 1)',fill='black'); y+=18
crops=[(r4,(14,48,46,62),'white'),(r3,(14,48,46,62),'white'),(f1(G+'pau/anim_front.png'),(12,48,44,62),(153,211,165)),(f1(G+'sensu/anim_front.png'),(32,46,64,60),(153,211,165))]
x=0
for im,c,bg in crops: W.paste(op(im.crop(c),bg,12)if False else op(im.crop(c),bg,12).resize((32*12//2*1,14*12//2*1)) if False else op(im.crop(c),bg,12),(x,y)); x+=32*12+6
y+=14*12+22; d.text((4,y),'1x op licht en donker: r4 | r3',fill='black'); y+=16
for k,im in enumerate((r4,r3)):
    W.paste(op(im,(255,255,255),1),(k*160,y)); W.paste(op(im,(40,40,48),1),(k*160+70,y))
W.save('vel.png'); print(W.size)
