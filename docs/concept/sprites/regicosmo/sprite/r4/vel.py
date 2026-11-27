# vel.png: rij 1 r3 | r4a | r4b | r4c op 8x; rij 2: elk op 1x en 2x (wit en donker) + model 1x.
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from PIL import Image, ImageDraw; import gemeen as g, vel_basis as vb
D=g.D; BG=(255,255,255); G=16
ims=[vb.laad(os.path.join(D,'../r3/regicosmo_r3.png'))]+[vb.laad(os.path.join(D,'regicosmo_%s.png'%n)) for n in ('r4a','r4b','r4c')]
nm=['r3','r4a','r4b','r4c']
V=Image.new('RGB',(4*512+5*G,512+3*G+40+150),(200,200,200)); dr=ImageDraw.Draw(V)
for i,im in enumerate(ims):
    V.paste(vb.op(im,BG).resize((512,512),0),(G+i*(512+G),G+20)); dr.text((G+i*(512+G),4),nm[i],fill=(0,0,0))
y=512+2*G+20; x=G
for i,im in enumerate(ims):
    for bg in [(255,255,255),(40,40,56)]:
        V.paste(vb.op(im,bg),(x,y)); V.paste(vb.op(im,bg).resize((128,128),0),(x+70,y)); x+=210
mod=vb.modelvak().resize((64,64),Image.LANCZOS); V.paste(mod,(x,y)); V.paste(mod.resize((128,128)),(x+70,y))
V.save(os.path.join(D,'vel.png'))
