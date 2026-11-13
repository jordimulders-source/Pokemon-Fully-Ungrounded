# maak_vel_r1.py: vergelijkingsvel voor r1 (vanuit sprite3/kleur/): python3 maak_vel_r1.py
from PIL import Image, ImageDraw; import numpy as np
GFX='../../../../../../graphics/pokemon/'
def spr(path,box=(0,0,64,64),z=1,bg=(255,255,255)):
    im=Image.open(path).crop((0,0,64,64)); a=np.array(im); rgb=np.array(im.convert('RGB')); rgb[a==0]=bg
    x0,y0,x1,y1=box; return Image.fromarray(rgb).crop(box).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
def model(box=(0,0,64,64),z=1):
    x0,y0,x1,y1=box; n=Image.open('../nat_A.png').convert('RGB')
    return n.crop((24+2*x0,21+2*y0,24+2*x1,21+2*y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
W=Image.new('RGB',(1600,2100),(255,255,255)); d=ImageDraw.Draw(W)
def put(im,x,y,t): W.paste(im,(x,y+12)); d.text((x,y),t,fill=(0,0,0)); return x+im.width+8
x=put(model(z=8),4,0,'model (nat_A, 8x)'); x=put(spr('basis.png',z=8),x,0,'basis 8x'); put(spr('r1.png',z=8),x,0,'r1 8x')
y=532
for naam,box,z in (('kop+ogen',(18,22,46,40),14),('mantel',(28,4,58,26),8)):
    x=4
    for t,im in (('model',model(box,z)),('basis',spr('basis.png',box,z)),('r1',spr('r1.png',box,z))): x=put(im,x,y,naam+' '+t)
    y+=(box[3]-box[1])*z+18
x=4
for naam,box,z in (('mond',(16,37,34,50),16),('wratten rechts',(44,20,63,48),8)):
    for t,im in (('model',model(box,z)),('r1',spr('r1.png',box,z))): x=put(im,x,y,naam+' '+t)
x=put(model((0,20,20,50),8),x,y,'links model'); put(spr('r1.png',(0,20,20,50),8),x,y,'links r1')
y+=260
box=(9,46,62,63); x=put(model(box,14),4,y,'rupsbanden model'); put(spr('r1.png',box,14),x,y,'rupsbanden r1 (zuignappen)')
y+=17*14+18
x=4
for bg in ((255,255,255),(40,40,48),(205,205,172)):
    for z in (1,2,4): x=put(spr('r1.png',z=z,bg=bg),x,y,'%dx'%z)
y+=280; x=4
for n in ('octillery','scizor','r1','crawdaunt','magcargo','groudon'):
    p='r1.png' if n=='r1' else GFX+n+'/anim_front_gba.png'
    x=put(spr(p,z=2,bg=(205,205,172)),x,y,n)
x+=20
for n in ('octillery','r1','groudon'):
    p='r1.png' if n=='r1' else GFX+n+'/anim_front_gba.png'
    x=put(spr(p,z=4,bg=(205,205,172)),x,y,n+' 4x')
W=W.crop((0,0,1600,y+280)); W.save('vel_r1.png'); print(W.size)
