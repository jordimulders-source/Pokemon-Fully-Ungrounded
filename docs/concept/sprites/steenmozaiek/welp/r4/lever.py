import numpy as np
from PIL import Image, ImageDraw
from toon import big, rgba
FIN=np.load('FIN2.npy')
def png64(a,fn):
    h,w=a.shape; full=np.zeros((64,64),'uint8'); x0=(64-w)//2; full[63-h:63,x0:x0+w]=a
    p=Image.fromarray(full,'P'); pal=[255,0,255]+[int(v) for c in FIN[1:] for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(fn,transparency=0)
a=np.load('welp_r4.npy'); r3=np.load('welp_r3_A_oog1.npy')
png64(a,'welp_r4.png'); big(a,8,(255,255,255,255)).save('welp_r4_8x.png')
n=Image.open('natief.png').convert('RGBA'); X0=Y0=2; s=3.3
mod=n.crop((X0,Y0,int(X0+50*s),int(Y0+45*s))).resize((50,45),Image.BOX)
modbig=Image.new('RGBA',(400,360),(235,235,225,255)); modbig.alpha_composite(mod.resize((400,360),Image.NEAREST))
row1=[(big(a,8),'r4'),(big(r3,8),'r3 A, oog 1 px links'),(modbig,'model verkleind 50x45, 8x')]
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
refs=[Image.open(G+f'{k}/anim_front_gba.png').convert('RGBA').crop((0,0,64,64)) for k in ('growlithe','vulpix')]
w4=Image.open('welp_r4.png').convert('RGBA')
V=Image.new('RGBA',(1280,18+360+40+2*(64*2+10)+10),(255,255,255,255)); d=ImageDraw.Draw(V); x=0
for im,l in row1: V.alpha_composite(im,(x,18)); d.text((x,3),l,fill=(0,0,0)); x+=im.width+20
y=18+360+25; d.text((0,y-14),'1x en 2x: Growlithe | r4 | Vulpix, licht en donker',fill=(0,0,0))
for row,bg in enumerate(((248,248,240,255),(40,44,52,255))):
    x=0
    for z in (1,2):
        for im in (refs[0],w4,refs[1]):
            t=Image.new('RGBA',(64*z,64*z),bg); t.alpha_composite(im.resize((64*z,64*z),Image.NEAREST)); V.alpha_composite(t,(x,y+row*(128+10))); x+=64*z+8
        x+=20
V.save('vel.png'); print(V.size)
