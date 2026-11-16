# vel r2 | r1 | model (zelfde schaal) op 8x; 1x/2x licht en donker
from PIL import Image, ImageDraw; import numpy as np
s,X0,Y0,oy,XC,k=[float(v) for v in open('r1.meta').read().split()]
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(np.uint8).copy()
for (x0,x1,y0,y1) in ((165,178,112,122),(157,163,123,129),(181,187,124,130),(169,175,129,132)): a[y0:y1+1,x0:x1+1]=255
m=Image.fromarray(a); L=m.crop((0,0,int(XC),199)); R=m.crop((int(XC),0,199,199)).resize((round((199-XC)*k),199),Image.LANCZOS)
mm=Image.new('RGB',(L.width+R.width,199),'white'); mm.paste(L,(0,0)); mm.paste(R,(L.width,0))
mm=mm.crop((int(X0),int(Y0),mm.width,199)); mm=mm.resize((round(mm.width*s),round(mm.height*s)),Image.LANCZOS)
ref=Image.new('RGB',(64,64),'white'); ref.paste(mm,(0,int(oy))); ref.save('model_geschaald.png')
def load(p,bg=(255,255,255)):
    im=Image.open(p).convert('RGBA'); b=Image.new('RGBA',(64,64),bg+(255,)); return Image.alpha_composite(b,im).convert('RGB')
V=Image.new('RGB',(3*512+4*16,512+40+170),(236,236,236)); d=ImageDraw.Draw(V)
for n,(im,t) in enumerate(((load('sprite.png'),'r2'),(load('../sprite_r1/sprite.png'),'r1'),(ref,'model, zelfde schaal'))):
    V.paste(im.resize((512,512),Image.NEAREST),(16+n*528,24)); d.text((16+n*528,8),t+' 8x',fill=0)
x=16; y=512+40
for p in ('sprite.png','../sprite_r1/sprite.png'):
    for bg in ((255,255,255),(40,44,60)):
        im=load(p,bg); V.paste(im,(x,y)); V.paste(im.resize((128,128),Image.NEAREST),(x+70,y)); x+=215
V.paste(ref,(x,y)); V.paste(ref.resize((128,128),Image.NEAREST),(x+70,y))
d.text((16,512+28),'1x/2x: r2 licht, r2 donker, r1 licht, r1 donker, model',fill=0); V.save('vel.png')
