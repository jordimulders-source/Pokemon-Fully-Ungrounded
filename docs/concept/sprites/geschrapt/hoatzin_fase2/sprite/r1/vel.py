# vel.png: sprite 8x | model op dezelfde schaal 8x | Pidgeot/Swellow (gba) 8x | 1x licht/donker | kop 12x: sprite | model | onderlaag
import numpy as np; from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def rgba(path):
    im=Image.open(path)
    if im.mode=='P':
        a=np.asarray(im); pal=np.array(im.getpalette()[:768]).reshape(-1,3)
        out=np.zeros(a.shape+(4,),'uint8'); out[...,:3]=pal[a]; out[...,3]=(a!=0)*255; return Image.fromarray(out,'RGBA')
    return im.convert('RGBA')
spr=rgba('hoatzin.png'); ond=Image.open('onderlaag.png').convert('RGBA')
spr.resize((512,512),Image.NEAREST).save('hoatzin_8x.png')
# model op dezelfde schaal: natieve uitsnede -> 51x63 (box) op dezelfde plek
N=Image.open('natief.png').convert('RGB'); Z=np.load('zones_nat.npy'); ys,xs=np.where(Z!='.')
x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1; TH=63; s=(y1-y0)/TH; TW=int(np.ceil((x1-x0)/s))
mc=N.crop((x0,y0,x0+TW*s,y1)).resize((TW*8,TH*8),Image.LANCZOS)
modelbig=Image.new('RGBA',(512,512),(255,255,255,255)); modelbig.paste(mc,(((64-TW)//2)*8,(64-TH)*8))
def frame(fr):
    b=Image.new('RGBA',(512,512),(255,255,255,255)); b.alpha_composite(fr.crop((0,0,64,64)).resize((512,512),Image.NEAREST)); return b
pid=rgba(G+'pidgeot/anim_front_gba.png').crop((0,0,64,64)); swe=rgba(G+'swellow/anim_front_gba.png').crop((0,0,64,64))
W=512*4+40*5; vel=Image.new('RGBA',(W,512+40+560),(225,225,225,255)); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate([(frame(spr),'r1 8x'),(modelbig,'model zelfde schaal'),(frame(pid),'Pidgeot'),(frame(swe),'Swellow')]):
    vel.paste(im,(40+i*552,30)); d.text((40+i*552,10),t,fill=(0,0,0,255))
y=600
d=ImageDraw.Draw(vel)
for j,bgc in enumerate([(248,248,248),(40,40,48),(120,168,120)]):
    b=Image.new('RGBA',(64,64),bgc+(255,)); b.alpha_composite(spr); vel.paste(b,(40+j*80,y))
    b2=Image.new('RGBA',(128,128),bgc+(255,)); b2.alpha_composite(spr.resize((128,128),Image.NEAREST)); vel.paste(b2,(40+j*150,y+80))
d.text((40,y-15),'1x en 2x op licht/donker/groen',fill=(0,0,0,255))
# kop 12x
box=(0,14,20,30)  # in 64-coord. (x0,y0,x1,y1) rond kop
bx=(4,15,24,30)
def wit(im):
    b=Image.new('RGBA',im.size,(255,255,255,255)); b.alpha_composite(im); return b
def crop12(im): return wit(im).crop(bx).resize(((bx[2]-bx[0])*12,(bx[3]-bx[1])*12),Image.NEAREST)
mb=modelbig.resize((64,64),Image.BOX)  # niet gebruikt
mk=Image.new('RGBA',(64*12,64*12)); 
mkop=modelbig.crop((bx[0]*8,bx[1]*8,bx[2]*8,bx[3]*8)).resize(((bx[2]-bx[0])*12,(bx[3]-bx[1])*12),Image.LANCZOS)
xx=520
for k,(im,t) in enumerate([(crop12(spr),'kop r1 12x'),(mkop,'model'),(crop12(ond),'onderlaag'),(crop12(rgba('hoatzin_oogB.png')),'variant oog B')]):
    vel.paste(im,(xx+k*260,y)); d.text((xx+k*260,y-15),t,fill=(0,0,0,255))
vel.save('vel.png'); print(vel.size)
