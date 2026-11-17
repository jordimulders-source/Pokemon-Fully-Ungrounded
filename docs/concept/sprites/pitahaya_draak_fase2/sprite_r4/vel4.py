# vel r3: hoofdversie | variant lipB | model (zelfde maat) op 8x; bek 12x van beide + model; 1x en 2x op licht/donker
import numpy as np; from PIL import Image
def rgba(f):
    Image.open(f).save('_t.png',transparency=0); return Image.open('_t.png').convert('RGBA')
def op(c,img):
    b=Image.new('RGBA',img.size,c+(255,)); b.alpha_composite(img); return b.convert('RGB')
A=rgba('pitahaya2_r4.png'); B=rgba('pitahaya2_r4_lipB.png')
o=np.asarray(Image.open('pitahaya2_r4.png')); ys,xs=np.where(o>0); bx=(xs.min(),ys.min(),xs.max()+1,ys.max()+1)
mod=Image.open('../model/model.png').convert('RGB'); M=np.asarray(mod).astype(int); my,mx=np.where(M.sum(2)<735); mb=(mx.min(),my.min(),mx.max()+1,my.max()+1)
can=Image.new('RGB',(64,64),(255,255,255)); can.paste(mod.crop(mb).resize((bx[2]-bx[0],bx[3]-bx[1]),Image.LANCZOS),(bx[0],bx[1]))
cr=(0,26,64,64); W,H=64*8,38*8
out=Image.new('RGB',(3*W+40,H+20+18*12+20+140),(235,235,240))
for k,im in enumerate([op((215,215,225),A),op((215,215,225),B),can]): out.paste(im.crop(cr).resize((W,H),Image.NEAREST),(k*(W+20),0))
kb=(2,40,20,56)
nat=Image.open('natief.png').convert('RGB').crop((2+3*kb[0],3*(kb[1]-13),2+3*kb[2],3*(kb[3]-13)))   # model op zijn eigen raster (natief), zelfde uitsnede
for k,im in enumerate([op((215,215,225),A).crop(kb),op((215,215,225),B).crop(kb),nat]): out.paste(im.resize((18*12,16*12),Image.NEAREST),(k*(18*12+20),H+20))
y=H+20+16*12+20
for k,im in enumerate([A,B]):       # links hoofdversie, rechts lipB: 1x licht/donker, 2x licht/donker
    for j,c in enumerate([(248,248,248),(40,40,48)]):
        out.paste(op(c,im),(k*560+j*70,y))
        out.paste(op(c,im.resize((128,128),Image.NEAREST)).crop((0,50,128,128)),(k*560+150+j*140,y))
out.save('vel.png')
