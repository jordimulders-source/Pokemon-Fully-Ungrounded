import sys;sys.path.insert(0,'.')
from PIL import Image, ImageDraw
from maak import meet
D='../';G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def rgba(p):
    im=Image.open(p).crop((0,0,64,64)); q=im.convert('RGBA'); A=im.load(); B=q.load()
    for y in range(64):
        for x in range(64):
            if A[x,y]==0: B[x,y]=(0,0,0,0)
    return q,im
names=['A','B','C','r25']; paths=['sprite_A.png','sprite_B.png','sprite_C.png',D+'sprite_r25/sprite.png']
sp=[rgba(p) for p in paths]
mod=Image.open(D+'model/model.webp').convert('RGBA').resize((512,512),Image.LANCZOS)
refs=[rgba(G+n+'/anim_front.png')[0] for n in ['forretress','magcargo','steelix']]
V=Image.new('RGBA',(5*530+20,1060),(248,248,248,255)); d=ImageDraw.Draw(V)
def put(im,x,y,z):
    b=im.resize((im.width*z,im.height*z),Image.NEAREST); V.paste(b,(x,y),b)
for k,((q,im),n) in enumerate(zip(sp,names)):
    x=10+k*530; put(q,x,30,8)
    m=meet([tuple(im.getpalette()[3*i:3*i+3]) for i in range(16)])
    d.text((x,10),f"{n}  zwak<20: metaal {m['metaal'][2]}%  groen {m['groen'][2]}%  groen-metaal {m['groen-metaal'][2]}%",fill=0)
    p=im.getpalette()
    for j,i in enumerate([1,7,10,14,8,11,12,9]):
        c=tuple(p[3*i:3*i+3]); d.rectangle((x+j*60,550,x+j*60+52,590),fill=c)
        d.text((x+j*60,594),f"{i}:{round(.299*c[0]+.587*c[1]+.114*c[2])}",fill=0)
    for j,i in enumerate([13,2,4,3,5,6]):
        c=tuple(p[3*i:3*i+3]); d.rectangle((x+j*60,612,x+j*60+52,652),fill=c)
        d.text((x+j*60,656),f"{i}:{round(.299*c[0]+.587*c[1]+.114*c[2])}",fill=0)
V.paste(mod,(10+4*530,30),mod); d.text((10+4*530,10),'model',fill=0)
y=690; d.text((10,y),'2x: A, B, C, r25, Forretress, Magcargo, Steelix, model',fill=0)
for i,q in enumerate([s[0] for s in sp]+refs): put(q,10+i*140,y+20,2)
m2=mod.resize((128,128),Image.LANCZOS); V.paste(m2,(10+7*140,y+20),m2)
y=850; d.text((10,y),'1x licht en donker',fill=0)
for i,q in enumerate([s[0] for s in sp]+refs): put(q,10+i*72,y+20,1)
V.paste((40,40,48,255),(10,y+90,10+72*7,y+160))
for i,q in enumerate([s[0] for s in sp]+refs): put(q,10+i*72,y+93,1)
V.save('vel.png')
