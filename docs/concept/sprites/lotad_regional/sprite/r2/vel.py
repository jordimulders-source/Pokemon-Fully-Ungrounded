# vel.png: (1) r1 8x | kleine variant 8x | kale reductie 8x | model op dezelfde schaal 8x
#          (2) kop 12x: r1 | model ; (3) 1x op licht/donker (r1, klein, Lotad) ; (4) r1 8x naast de Gen 3-Lotad 8x
import numpy as np; from PIL import Image, ImageDraw
from gemeen import rgb; from kijk import model_op_schaal, eigen
W=(255,255,255)
def spr(p,z,bg=W): return eigen(p,bg).resize((64*z,64*z),Image.NEAREST)
lot=Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/lotad/anim_front_gba.png').convert('RGBA').crop((0,0,64,64))
def lotz(z,bg=W):
    c=Image.new('RGBA',(64,64),bg+(255,)); c.alpha_composite(lot); return c.convert('RGB').resize((64*z,64*z),Image.NEAREST)
def label(im,t):
    c=Image.new('RGB',(im.width,im.height+16),(220,220,220)); c.paste(im,(0,16)); ImageDraw.Draw(c).text((4,2),t,fill=(0,0,0)); return c
def rij(ims,gap=8):
    w=sum(i.width for i in ims)+gap*(len(ims)-1); h=max(i.height for i in ims)
    c=Image.new('RGB',(w,h),(200,200,200)); x=0
    for i in ims: c.paste(i,(x,0)); x+=i.width+gap
    return c
r0=rij([label(spr('../r1/lotad_gaucho.png',8),'r1 (8x)'),label(spr('lotad_gaucho.png',8),'r2 (8x)'),label(model_op_schaal(43,8),'model r8_1 (zelfde schaal)')])
r0.save('r1_r2_model.png')
r1=rij([label(spr('lotad_gaucho.png',8),'r2 hoofdversie 43x41 (8x)'),label(spr('lotad_gaucho_klein.png',8),'klein 40x38 (8x)'),
        label(spr('kaal.png',8),'kale reductie (8x)'),label(model_op_schaal(43,8),'model r8_1 (zelfde schaal)')])
box=(14,32,40,50); z=12
k1=spr('lotad_gaucho.png',z).crop(tuple(v*z for v in box)); k2=model_op_schaal(43,z).crop(tuple(v*z for v in box))
r2=rij([label(k1,'kop r2 (12x)'),label(k2,'kop model (12x)'),label(lotz(12).crop((14*12,30*12,40*12,50*12)),'Lotad Gen 3 (12x)')])
een=[]
for bg in ((255,255,255),(232,232,216),(152,208,160),(40,40,48)):
    c=Image.new('RGB',(3*64,64),bg)
    for i,p in enumerate(['lotad_gaucho.png','lotad_gaucho_klein.png']):
        c.paste(eigen(p,bg),(i*64,0))
    l=Image.new('RGBA',(64,64),bg+(255,)); l.alpha_composite(lot); c.paste(l.convert('RGB'),(128,0))
    een.append(c.resize((3*64*2,64*2),Image.NEAREST) if False else c)
r3=label(rij(een),'1x: r2 | klein | Gen 3-Lotad op wit, creme, groen, donker')
r4=rij([label(spr('lotad_gaucho.png',8),'r2 (8x)'),label(lotz(8),'Gen 3-Lotad (8x)')])
H=r1.height+r2.height+r3.height+r4.height+48; Wd=max(r.width for r in (r1,r2,r3,r4))
v=Image.new('RGB',(Wd,H),(200,200,200)); y=0
for r in (r1,r2,r3,r4): v.paste(r,(0,y)); y+=r.height+16
v.save('vel.png'); print(v.size)
