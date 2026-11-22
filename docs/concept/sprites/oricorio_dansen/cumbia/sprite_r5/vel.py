# vel.png r5: r5 | r4 | model op 8x ; kop 12x r5 | r4 ; 1x licht/donker r5 | r4 ; palet r5
import numpy as np; from PIL import Image, ImageDraw
from palet import pal
def rgba(p): return Image.open(p).convert('RGBA')
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
r5=rgba('cumbia.png'); r4=rgba('r4_ref.png'); o=np.load('cumbia_r5.npy')
na=np.asarray(Image.open('natief.png').convert('RGB')); bgm=na.min(2)>=225; yy,xx=np.where(~bgm)
nb=Image.fromarray(na).crop((xx.min(),yy.min(),xx.max()+1,yy.max()+1)); sy,sx=np.where(o>0)
m=nb.resize(((sx.max()-sx.min()+1)*8,(sy.max()-sy.min()+1+1)*8),Image.NEAREST)
mod=Image.new('RGB',(512,512),'white'); mod.paste(m,(sx.min()*8,sy.min()*8))
W=Image.new('RGB',(3*522,30+512+30+300+30+70),(230,230,230)); d=ImageDraw.Draw(W)
for k,(im,t) in enumerate([(op(r5,'white',8),'r5 (kleur/lijn na eindkeuring)'),(op(r4,'white',8),'r4'),(mod,'model gemini_r2 (toonbron)')]):
    W.paste(im,(k*522,30)); d.text((k*522+4,8),t,fill='black')
y=572; d.text((4,y-16),'kop 12x: r5 | r4',fill='black')
W.paste(op(r5.crop((14,3,46,28)),'white',12)if False else op(r5.crop((16,3,40,28)),'white',12),(0,y)); W.paste(op(r4.crop((16,3,40,28)),'white',12),(300,y))
W.paste(op(r5,(255,255,255),1),(620,y)); W.paste(op(r5,(40,40,48),1),(690,y)); W.paste(op(r4,(255,255,255),1),(780,y)); W.paste(op(r4,(40,40,48),1),(850,y))
d.text((620,y+70),'1x: r5 licht/donker | r4 licht/donker',fill='black')
W.paste(op(r5,(255,255,255),2),(940,y)); W.paste(op(r5,(40,40,48),2),(1080,y))
p=pal('r5'); y2=y+310
for i,c in enumerate(p[1:]): d.rectangle([i*40,y2,i*40+36,y2+36],fill=c); d.text((i*40+2,y2+40),str(i+1),fill='black')
W.save('vel.png'); print(W.size)
