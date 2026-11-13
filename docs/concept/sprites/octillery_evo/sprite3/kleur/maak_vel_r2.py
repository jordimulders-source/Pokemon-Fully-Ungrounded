# maak_vel_r2.py: vergelijkingsvel voor r2 (vanuit sprite3/kleur/): python3 maak_vel_r2.py
from PIL import Image, ImageDraw; import numpy as np
GFX='../../../../../../graphics/pokemon/'; BG=(205,205,172)
def spr(path,box=(0,0,64,64),z=1,bg=BG):
    im=Image.open(path).crop((0,0,64,64)); a=np.array(im); rgb=np.array(im.convert('RGB')); rgb[a==0]=bg
    x0,y0,x1,y1=box; return Image.fromarray(rgb).crop(box).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
def model(box=(0,0,64,64),z=1):
    x0,y0,x1,y1=box; n=Image.open('../nat_A.png').convert('RGB')
    return n.crop((24+2*x0,21+2*y0,24+2*x1,21+2*y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
W=Image.new('RGB',(1640,4200),(255,255,255)); d=ImageDraw.Draw(W)
def put(im,x,y,t): W.paste(im,(x,y+12)); d.text((x,y),t,fill=(0,0,0)); return x+im.width+8
x=put(model(z=8),4,0,'model (nat_A, 8x)'); x=put(spr('r1.png',z=8),x,0,'r1 8x'); put(spr('r2.png',z=8),x,0,'r2 8x')
y=536
def rij(naam,box,z):
    global y
    x=4
    for t,im in (('model',model(box,z)),('r1',spr('r1.png',box,z)),('r2',spr('r2.png',box,z))): x=put(im,x,y,naam+' '+t+' %dx'%z)
    y+=(box[3]-box[1])*z+20
rij('linkerkanon',(2,21,20,46),16)
rij('rechterkanon',(40,22,56,44),16)
rij('kleine tentakels links',(0,36,22,51),16)
rij('tentakels rechts',(42,19,64,49),16)
rij('mond',(16,37,35,51),16)
rij('rupsband links + zuignappen',(9,47,31,63),16)
rij('rupsband rechts + zuignappen',(28,46,62,63),15)
for f in ('r1.png','r2.png'):
    x=4
    for bg in (BG,(40,40,48),(255,255,255)):
        for z in (1,2,4): x=put(spr(f,z=z,bg=bg),x,y,f[:2]+' %dx'%z)
    y+=280
x=4
for n in ('octillery','scizor','r2','crawdaunt','groudon'):
    p='r2.png' if n=='r2' else GFX+n+'/anim_front_gba.png'
    x=put(spr(p,z=2),x,y,n+' 2x')
x+=20
for n in ('octillery','r2','groudon'):
    p='r2.png' if n=='r2' else GFX+n+'/anim_front_gba.png'
    x=put(spr(p,z=4),x,y,n+' 4x')
W=W.crop((0,0,1640,y+280)); W.save('vel_r2.png'); print(W.size)
