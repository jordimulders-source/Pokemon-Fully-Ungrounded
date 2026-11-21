# vel.png: per variant 8x naast het model (zelfde schaal) ; close-up poten 12x naast Baile/Pom-Pom ; 5 snavels 12x ; 1x licht/donker
import numpy as np; from PIL import Image, ImageDraw
Z=8; R='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/oricorio/'
def ld(p):
    im=Image.open(p); im.load(); return im.convert('RGBA').crop((0,0,64,64))
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
spr={v:ld('tango_%s.png'%v) for v in 'ABC'}
a=np.asarray(spr['A'])[:,:,3]; sy,sx=np.where(a>0)
na=np.asarray(Image.open('natief.png').convert('RGB')); bgm=na.min(2)>=225; yy,xx=np.where(~bgm)
nb=Image.fromarray(na).crop((xx.min(),yy.min(),xx.max()+1,yy.max()+1))
mod=Image.new('RGB',(512,512),'white')
m=nb.resize((int(round(nb.width*0.6*Z)),int(round(nb.height*0.6*Z))),Image.NEAREST)
mod.paste(m,((sx.max()+1)*Z-m.width,(sy.max()+1)*Z-m.height))   # rechtsonder uitgelijnd
W=Image.new('RGB',(532*4,512+40+330+40+170),(230,230,230)); d=ImageDraw.Draw(W)
T={'A':'rood = binnenkant split','B':'rood = franjezoom','C':'rood = accent bij de knot'}
for i,v in enumerate('ABC'):
    W.paste(op(spr[v],(255,255,255),Z),(i*532,30)); d.text((i*532+4,8),'tango_%s (8x)  %s'%(v,T[v]),fill='black')
W.paste(mod,(3*532,30)); d.text((3*532+4,8),'model gemini_r5 (natief x0,6 = zelfde schaal)',fill='black')
y=600; d.text((4,y-18),'poten 12x: tango | Baile (bron) | Pom-Pom',fill='black')
W.paste(op(spr['A'].crop((10,44,40,62)),(255,255,255),12),(0,y))
W.paste(op(ld(R+'anim_front.png').crop((16,44,40,62)),(255,255,255),12),(370,y))
W.paste(op(ld(R+'pom_pom/anim_front.png').crop((22,42,46,60)),(255,255,255),12),(670,y))
x=990; d.text((x,y-18),"snavels 12x: tango | model (kale reductie) | Baile | Pom-Pom | Pa'u | Sensu",fill='black')
pk=np.asarray(spr['A']); rz=np.where((pk[:,:,0]>200)&(pk[:,:,3]>0)&(np.arange(64)[:,None]<30)); ty,tx=rz[0].min(),rz[1].min()-3
W.paste(op(spr['A'].crop((tx-1,ty-1,tx+11,ty+9)),(255,255,255),12),(x,y)); x+=150
from palet import pal
bz=np.load('basis.npy')[7:17,9:21]; P=pal(); ba=np.zeros(bz.shape+(4,),'uint8')
for i,c in enumerate(P):
    if i: ba[bz==i,:3]=c; ba[bz==i,3]=255
W.paste(op(Image.fromarray(ba),(255,255,255),12),(x,y)); x+=150
for f,(y0,x0) in [('',(17,15)),('pom_pom/',(18,24)),('pau/',(18,20)),('sensu/',(18,30))]:
    W.paste(op(ld(R+f+'anim_front.png').crop((x0,y0,x0+12,y0+10)),(255,255,255),12),(x,y)); x+=150
y2=y+260; d.text((4,y2-16),'1x licht/donker   |   2x op gevechtsgroen',fill='black')
for i,v in enumerate('ABC'):
    W.paste(op(spr[v],(255,255,255),1),(i*150,y2)); W.paste(op(spr[v],(40,40,48),1),(i*150+70,y2))
    W.paste(op(spr[v],(152,208,160),2),(500+i*140,y2))
W.save('vel.png'); print(W.size)
