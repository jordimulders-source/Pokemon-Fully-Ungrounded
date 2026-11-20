# vel.png: r6 | r5 (buik D) | model zelfde schaal | Taillow | Pidgeot, 8x (Taillow 8x op 64) ; daaronder 1x en 2x op licht en donker
import numpy as np; from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def rgba(path):
    im=Image.open(path); a=np.asarray(im)[:64]; pal=np.array(im.getpalette()[:768]).reshape(-1,3)
    out=np.zeros(a.shape+(4,),'uint8'); out[...,:3]=pal[a]; out[...,3]=(a!=0)*255; return Image.fromarray(out,'RGBA')
spr=rgba('hoatzin.png'); r5=rgba('r6.png')
spr.resize((512,512),Image.NEAREST).save('hoatzin_8x.png')
N=Image.open('natief.png').convert('RGB'); Z=np.load('zones_nat.npy'); ys,xs=np.where(Z!='.')
x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1; TH=63; s=(y1-y0)/TH; TW=int(np.ceil((x1-x0)/s))
mc=N.crop((x0,y0,x0+TW*s,y1)).resize((TW*8,TH*8),Image.LANCZOS)
model=Image.new('RGBA',(512,512),(255,255,255,255)); model.paste(mc,(((64-TW)//2)*8,(64-TH)*8))
mod1=model.resize((64,64),Image.BOX)
def frame(fr):
    b=Image.new('RGBA',(512,512),(255,255,255,255)); b.alpha_composite(fr.resize((512,512),Image.NEAREST)); return b
rij=[(spr,'r7'),(r5,'r6'),(None,'model'),(rgba(G+'taillow/anim_front_gba.png'),'Taillow'),(rgba(G+'pidgeot/anim_front_gba.png'),'Pidgeot')]
W=40+len(rij)*552; vel=Image.new('RGBA',(W,512+60+260),(225,225,225,255)); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate(rij):
    vel.paste(model if im is None else frame(im),(40+i*552,30)); d.text((40+i*552,10),t+' 8x',fill=(0,0,0,255))
y=580
for i,(im,t) in enumerate(rij):
    if im is None: continue
    for j,bgc in enumerate([(248,248,248),(40,40,48)]):
        b=Image.new('RGBA',(64,64),bgc+(255,)); b.alpha_composite(im); vel.paste(b,(40+i*552+j*72,y))
        b2=Image.new('RGBA',(128,128),bgc+(255,)); b2.alpha_composite(im.resize((128,128),Image.NEAREST)); vel.paste(b2,(40+i*552+j*140,y+80))
d.text((40,y-15),'1x en 2x op licht en donker',fill=(0,0,0,255))
vel.convert('RGB').save('vel.png'); print(vel.size)
