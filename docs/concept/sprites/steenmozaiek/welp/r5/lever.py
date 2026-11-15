import numpy as np
from PIL import Image, ImageDraw
from toon import big, rgba
FIN=np.load('FIN2.npy')
def png64(a,fn):
    h,w=a.shape; full=np.zeros((64,64),'uint8'); x0=(64-w)//2; full[63-h:63,x0:x0+w]=a
    p=Image.fromarray(full,'P'); pal=[255,0,255]+[int(v) for c in FIN[1:] for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(fn,transparency=0)
r5=np.load('welp_r5.npy'); r3=np.load('welp_r3_A_oog1.npy'); r4=np.load('welp_r4.npy')
png64(r5,'welp_r5.png'); big(r5,8,(255,255,255,255)).save('welp_r5_8x.png')
n=Image.open('natief.png').convert('RGBA'); X0=Y0=2; s=3.3
mod=n.crop((X0,Y0,int(X0+50*s),int(Y0+45*s))).resize((50,45),Image.BOX)
modbig=Image.new('RGBA',(400,360),(235,235,225,255)); modbig.alpha_composite(mod.resize((400,360),Image.NEAREST))
row1=[(big(r5,8),'r5'),(big(r3,8),'r3 A oog1'),(big(r4,8),'r4'),(modbig,'model verkleind 50x45')]
box=(0,0,25,24)
kmod=n.crop((int(X0+box[0]*s),int(Y0+box[1]*s),int(X0+box[2]*s),int(Y0+box[3]*s))).resize((25*12,24*12),Image.LANCZOS)
row2=[(big(z[box[1]:box[3],box[0]:box[2]],12),l) for z,l in ((r5,'kop r5'),(r3,'kop r3'),(r4,'kop r4'))]+[(kmod,'kop model')]
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
refs=[Image.open(G+f'{k}/anim_front_gba.png').convert('RGBA').crop((0,0,64,64)) for k in ('growlithe','vulpix')]
w5=Image.open('welp_r5.png').convert('RGBA')
V=Image.new('RGBA',(1680,18+360+30+288+30+64*2+20),(255,255,255,255)); d=ImageDraw.Draw(V); x=0
for im,l in row1: V.alpha_composite(im,(x,18)); d.text((x,3),l,fill=(0,0,0)); x+=im.width+20
x=0; y=18+360+28
for im,l in row2: V.alpha_composite(im,(x,y)); d.text((x,y-14),l,fill=(0,0,0)); x+=im.width+20
y+=288+28; d.text((0,y-14),'1x: Growlithe | r5 | Vulpix, licht en donker',fill=(0,0,0)); x=0
for bg in ((248,248,240,255),(40,44,52,255)):
    for im in (refs[0],w5,refs[1]):
        t=Image.new('RGBA',(64,64),bg); t.alpha_composite(im); V.alpha_composite(t,(x,y)); x+=72
    x+=20
V.save('vel.png'); print(V.size)
