# vel.png r3: r3 | r2 | model op 8x ; 5 snavels 12x (r3, Baile, Pom-Pom, Pa'u, Sensu) ; poten 12x (r2, r3, Pa'u) ; 1x/2x licht en donker
import numpy as np; from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/oricorio/'
def rgba(p): return Image.open(p).convert('RGBA')
def f1(p): return rgba(p).crop((0,0,64,64))
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
r3=rgba('cumbia.png'); r2=rgba('r2_ref.png'); o=np.load('cumbia_kls.npy')
na=np.asarray(Image.open('natief.png').convert('RGB')); bgm=na.min(2)>=225; yy,xx=np.where(~bgm)
nb=Image.fromarray(na).crop((xx.min(),yy.min(),xx.max()+1,yy.max()+1)); sy,sx=np.where(o>0)
m=nb.resize(((sx.max()-sx.min()+1)*8,(sy.max()-sy.min()+1)*8),Image.NEAREST)
mod=Image.new('RGB',(512,512),'white'); mod.paste(m,(sx.min()*8,sy.min()*8))
W=Image.new('RGB',(3*522,30+512+40+150+40+200+20),(230,230,230)); d=ImageDraw.Draw(W)
for k,(im,t) in enumerate([(op(r3,'white',8),'r3 (Pom-Pom-snavel, poten vast)'),(op(r2,'white',8),'r2'),(mod,'model gemini_r2, zelfde schaal')]):
    W.paste(im,(k*522,30)); d.text((k*522+4,8),t,fill='black')
y=572; d.text((4,y),'snavels 12x: r3 | Baile | Pom-Pom | Pa\'u | Sensu (Gen 3, frame 1)',fill='black'); y+=18
crops=[(r3,(15,13,27,23)),(f1(G+'anim_front.png'),(19,18,31,28)),(f1(G+'pom_pom/anim_front.png'),(23,17,35,27)),(f1(G+'pau/anim_front.png'),(19,17,31,27)),(f1(G+'sensu/anim_front.png'),(29,19,41,29))]
x=0
for im,c in crops:
    W.paste(op(im.crop(c),(255,255,255) if im is r3 else (153,211,165),12),(x,y)); x+=12*12+12
y+=140; d.text((4,y),'poten 12x: r2 | r3 | Pa\'u    en 1x/2x op licht en donker',fill='black'); y+=18
W.paste(op(r2.crop((16,48,46,63)),'white',12),(0,y)); W.paste(op(r3.crop((16,48,46,63)),'white',12),(372,y))
W.paste(op(f1(G+'pau/anim_front.png').crop((14,48,44,63)),(153,211,165),12),(744,y))
W.paste(op(r3,(255,255,255),1),(1120,y)); W.paste(op(r3,(40,40,48),1),(1190,y))
W.paste(op(r3,(255,255,255),2),(1260,y)); W.paste(op(r3,(40,40,48),2),(1260+130,y)) if 1260+130+128<=W.width else None
W.save('vel.png'); print(W.size)
