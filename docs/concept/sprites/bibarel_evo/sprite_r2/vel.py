# vel.py ronde 2: r2 | r1 | model (8x); kop 12x r2|r1|model|Bibarel; benen/romp 12x r2|model; paletvoorstel 4x; 1x licht/donker
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
from PIL import Image, ImageDraw
fig=np.load('sprite_r1/masker.npy'); yy,xx=np.where(fig)
M=np.asarray(Image.open('model/r10_k8.png').convert('RGB')); mx0,my0=xx.min(),yy.min(); s=64/(xx.max()-mx0+1); oy=64-round((yy.max()-my0+1)*s)
def modelvak(x0,y0,x1,y1,Z):
    W,H=(x1-x0)*Z,(y1-y0)*Z; out=np.full((H,W,3),255,'uint8')
    py,px=np.mgrid[0:H,0:W]; X=(mx0+(x0+px/Z)/s).astype(int); Y=(my0+(y0+py/Z-oy)/s).astype(int)
    ok=(X>=0)&(X<99)&(Y>=0)&(Y<99); out[ok]=M[Y[ok],X[ok]]; return Image.fromarray(out)
def spr(p,z,box=None,pal=None):
    o=laad(p); P=np.array(pal or PAL,'uint8'); im=Image.fromarray(P[o])
    if box: im=im.crop(box)
    return im.resize((im.width*z,im.height*z),Image.NEAREST)
V=Image.new('RGB',(1700,2000),'white'); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(spr('sprite_r2/sprite.png',8),'r2'),(spr('sprite_r1/sprite.png',8),'r1'),(modelvak(0,0,64,64,8),'model r10_k8')]):
    V.paste(im,(10+i*540,30)); d.text((10+i*540,10),t+' 8x',fill='black')
y=570; kb=(14,8,46,34)
B=Image.open('../../../../graphics/pokemon/bibarel/anim_front.png').convert('RGB').crop((4,6,36,32)).resize((32*12,26*12),Image.NEAREST)
for i,(im,t) in enumerate([(spr('sprite_r2/sprite.png',12,kb),'kop r2 12x'),(spr('sprite_r1/sprite.png',12,kb),'kop r1'),(modelvak(*kb,12),'model'),(B,'Bibarel Gen 3 (bron kraag/ogen), 12x')]):
    V.paste(im,(10+i*400,y+20)); d.text((10+i*400,y),t,fill='black')
y=y+350; bb=(12,32,56,64)
V.paste(spr('sprite_r2/sprite.png',12,bb),(10,y+20)); d.text((10,y),'benen/romp r2 12x',fill='black')
V.paste(modelvak(*bb,12),(560,y+20)); d.text((560,y),'model',fill='black')
y=y+420
PV=list(PAL); PV[6]=(228,200,156); PV[15]=(196,158,112)
V.paste(spr('sprite_r2/sprite.png',4),(10,y+20)); d.text((10,y),'r2 4x',fill='black')
V.paste(spr('sprite_r2/sprite.png',4,pal=PV),(280,y+20)); d.text((280,y),'ter info: zelfde pixels, cremeschaduw/-donker lichter (paletkeuze)',fill='black')
for j,bg in enumerate([(248,248,248),(40,40,48)]):
    for i,p in enumerate(['sprite_r2/sprite.png','sprite_r1/sprite.png']):
        o=laad(p); im=Image.new('RGB',(64,64),bg); im.paste(Image.fromarray(rgb(o)),(0,0),Image.fromarray(((o>0)*255).astype('uint8')))
        V.paste(im,(600+i*80,y+20+j*80))
d.text((600,y),'1x licht/donker (r2, r1)',fill='black')
V.crop((0,0,1700,y+300)).save('sprite_r2/vel.png')
