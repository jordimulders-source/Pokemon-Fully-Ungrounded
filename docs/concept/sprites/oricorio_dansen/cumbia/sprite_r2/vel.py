# vel.png r2: r2 | r1 | model op 8x ; kop 12x naast Pom-Pom-kop ; 1x licht/donker (kleur B_midden, gekozen door Jordi)
import numpy as np; from PIL import Image, ImageDraw
def rgba(path):
    return Image.open(path).convert('RGBA')
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
r2=rgba('cumbia.png'); r1=rgba('../sprite_r1/cumbia.png')
o=np.load('cumbia_kls.npy')
na=np.asarray(Image.open('natief.png').convert('RGB')); bgm=na.min(2)>=225; yy,xx=np.where(~bgm)
nb=Image.fromarray(na).crop((xx.min(),yy.min(),xx.max()+1,yy.max()+1)); sy,sx=np.where(o>0)
m=nb.resize(((sx.max()-sx.min()+1)*8,(sy.max()-sy.min()+1)*8),Image.NEAREST)
mod=Image.new('RGB',(512,512),'white'); mod.paste(m,(sx.min()*8,sy.min()*8))
W=Image.new('RGB',(3*522,30+512+30+290),(230,230,230)); d=ImageDraw.Draw(W)
for k,(im,t) in enumerate([(op(r2,'white',8),'r2 (Pom-Pom-oog, wit glimpje)'),(op(r1,'white',8),'r1 (Pa\'u-oog)'),(mod,'model gemini_r2, zelfde schaal')]):
    W.paste(im,(k*522,30)); d.text((k*522+4,8),t,fill='black')
y=572; d.text((4,y),'kop r2 12x  |  Pom-Pom (Gen 3, bron oog) 12x  |  1x op licht en donker',fill='black'); y+=20
W.paste(op(r2.crop((14,4,42,24)),'white',12),(0,y))
pom=rgba('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/oricorio/pom_pom/anim_front.png').crop((22,8,50,28))
W.paste(op(pom,(153,211,165),12),(350,y))
W.paste(op(r2,(255,255,255),1),(720,y)); W.paste(op(r2,(40,40,48),1),(800,y))
W.paste(op(r2,(255,255,255),2),(880,y)); W.paste(op(r2,(40,40,48),2),(1020,y))
W.save('vel.png'); print(W.size)
