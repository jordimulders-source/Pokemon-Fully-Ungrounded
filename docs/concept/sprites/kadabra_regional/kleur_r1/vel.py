# vel.py -> vel.png: sprite 8x | model verkleind 8x | model; close-ups 12x (kop, kaarthand, open hand, nagelvarianten) naast het model; 1x/2x op licht en donker naast de echte Kadabra en de charlatan-Alakazam
import numpy as np, pal
from PIL import Image, ImageDraw
from zij import model, sprite
from meet import s2c
BG=(152,208,160); R=pal.load('raster.txt'); Z=pal.load('variant_zonder_nagel.txt')
M=Image.open('cellen.png').convert('RGB')
a=s2c(0,0); b=s2c(64,64)
big=M.resize((3100,3100),Image.NEAREST)
canvas=Image.new('RGB',(int(b[0]*31)-int(a[0]*31),int(b[1]*31)-int(a[1]*31)),'white')
canvas.paste(big,(-int(a[0]*31),-int(a[1]*31)))
klein=canvas.resize((64,64),Image.BOX)
V=Image.new('RGB',(1600,1700),'white'); D=ImageDraw.Draw(V)
def put(im,x,y,t): D.text((x,y),t,fill=(0,0,0)); V.paste(im,(x,y+14))
put(pal.rgb(R,BG).resize((512,512),0),8,4,'kleur_r1, 8x')
put(klein.resize((512,512),0),530,4,'model verkleind naar 64x64 (BOX), 8x')
put(canvas.resize((512,512),Image.LANCZOS),1052,4,'model (100x100 cellen)')
y=540
def paar(x,y,box,z,t,RR=R):
    s=sprite(RR,*box,z); m=model(*box,z,False); put(s,x,y,t); V.paste(m,(x+s.width+4,y+14)); return x+2*s.width+16
x=paar(8,y,(19,8,41,32),12,'kop 12x: sprite | model')
x=paar(x,y,(0,18,22,36),12,'kaarthand 12x: sprite | model (3 vingers: gestrekt met nagel, 2 gebogen)')
y2=y+12*24+30
x=paar(8,y2,(42,18,64,35),12,'open hand 12x: sprite | model (3 vingers: duim links, omhoog, schuin rechts; elk een wit klauwtje)')
put(sprite(R,1,19,13,30,12),x,y2,'vingertop MET nagel (hoofdsprite)'); put(sprite(Z,1,19,13,30,12),x+160,y2,'ZONDER nagel (model)')
put(sprite(R,1,19,13,30,3),x+330,y2,'3x met'); put(sprite(Z,1,19,13,30,3),x+380,y2,'zonder')
x=paar(x+440,y2,(13,50,30,62),12,'linkervoet 12x')
y3=y2+12*17+40
def echt(fn,bg):
    q=Image.open(fn).crop((0,0,64,64)); p=q.convert('RGBA'); arr=np.asarray(q)
    if q.mode=='P' and 'transparency' not in q.info: p.putalpha(Image.fromarray(((arr!=arr[0,0])*255).astype('uint8')))
    c=Image.new('RGBA',(64,64),bg+(255,)); c.alpha_composite(p); return c.convert('RGB')
KAD='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/kadabra/anim_front_gba.png'; ALA='../../alakazam_regional/af_r2/alakazam_charlatan.png'
for r,(bg,lab) in enumerate([((248,248,240),'licht'),((40,40,56),'donker')]):
    yy=y3+r*240; D.text((8,yy),'1x en 3x op '+lab+': echte Kadabra | kleur_r1 | charlatan-Alakazam | model verkleind',fill=(0,0,0))
    ims=[echt(KAD,bg),pal.rgb(R,bg),echt(ALA,bg)]
    kb=Image.new('RGB',(64,64),bg); arr=np.asarray(klein).copy(); 
    x=8
    for im in ims: V.paste(im,(x,yy+16)); x+=70
    V.paste(klein,(x,yy+16)); x+=90
    for im in ims: V.paste(im.resize((192,192),0),(x,yy+16)); x+=200
    V.paste(klein.resize((192,192),0),(x,yy+16))
V=V.crop((0,0,1600,y3+480)); V.save('vel.png'); print(V.size)
