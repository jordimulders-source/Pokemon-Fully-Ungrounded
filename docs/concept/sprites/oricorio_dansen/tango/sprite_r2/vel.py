# vel.png r2: A/B/C | r1 (A) | model op 8x ; poten 12x r2|r1 ; kop 12x r2|r1 ; 1x licht/donker
import numpy as np; from PIL import Image, ImageDraw
Z=8
def ld(p):
    im=Image.open(p); im.load(); return im.convert('RGBA').crop((0,0,64,64))
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
spr={v:ld('tango_%s.png'%v) for v in 'ABC'}; r1=ld('../sprite_r1/tango_A.png')
a=np.asarray(spr['A'])[:,:,3]; sy,sx=np.where(a>0)
na=np.asarray(Image.open('natief.png').convert('RGB')); bgm=na.min(2)>=225; yy,xx=np.where(~bgm)
nb=Image.fromarray(na).crop((xx.min(),yy.min(),xx.max()+1,yy.max()+1))
mod=Image.new('RGB',(512,512),'white'); m=nb.resize((int(round(nb.width*0.6*Z)),int(round(nb.height*0.6*Z))),Image.NEAREST)
mod.paste(m,((sx.max()+1)*Z-m.width,(sy.max()+1)*Z-m.height))
W=Image.new('RGB',(532*5,512+40+260+40+250+40+140),(230,230,230)); d=ImageDraw.Draw(W)
T={'A':'rood = smalle split','B':'rood = franjezoom','C':'rood = accent bij de knot'}
for i,v in enumerate('ABC'):
    W.paste(op(spr[v],(255,255,255),Z),(i*532,30)); d.text((i*532+4,8),'r2 tango_%s (8x)  %s'%(v,T[v]),fill='black')
W.paste(op(r1,(255,255,255),Z),(3*532,30)); d.text((3*532+4,8),'r1 tango_A (8x)',fill='black')
W.paste(mod,(4*532,30)); d.text((4*532+4,8),'model gemini_r5 (zelfde schaal)',fill='black')
y=600; d.text((4,y-18),'poten 12x: r2 | r1',fill='black')
W.paste(op(spr['A'].crop((10,44,42,62)),(255,255,255),12),(0,y)); W.paste(op(r1.crop((10,44,42,62)),(255,255,255),12),(400,y))
x=820; d.text((x,y-18),'kop 12x: r2 | r1',fill='black')
W.paste(op(spr['A'].crop((20,4,44,22)),(255,255,255),12),(x,y)); W.paste(op(r1.crop((20,4,44,22)),(255,255,255),12),(x+300,y))
y2=y+300; d.text((4,y2-16),'1x licht/donker | 2x gevechtsgroen',fill='black')
for i,v in enumerate('ABC'):
    W.paste(op(spr[v],(255,255,255),1),(i*150,y2)); W.paste(op(spr[v],(40,40,48),1),(i*150+70,y2))
    W.paste(op(spr[v],(152,208,160),2),(500+i*140,y2))
W.save('vel.png'); print(W.size)
