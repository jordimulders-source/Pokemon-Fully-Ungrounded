# vel.py ronde 3: r3 | r1 | model (8x); broek 12x r3|r1|model; varianten; kraagproeven kop 12x naast r1/model/Bibarel; 1x licht/donker
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
from PIL import Image, ImageDraw
fig=np.load('sprite_r1/masker.npy'); yy,xx=np.where(fig)
M=np.asarray(Image.open('model/r10_k8.png').convert('RGB')); mx0,my0=xx.min(),yy.min(); s=64/(xx.max()-mx0+1); oy=64-round((yy.max()-my0+1)*s)
def modelvak(x0,y0,x1,y1,Z):
    W,H=(x1-x0)*Z,(y1-y0)*Z; out=np.full((H,W,3),255,'uint8')
    py,px=np.mgrid[0:H,0:W]; X=(mx0+(x0+px/Z)/s).astype(int); Y=(my0+(y0+py/Z-oy)/s).astype(int)
    ok=(X>=0)&(X<99)&(Y>=0)&(Y<99); out[ok]=M[Y[ok],X[ok]]; return Image.fromarray(out)
def spr(p,z,box=None):
    im=Image.fromarray(rgb(laad(p)))
    if box: im=im.crop(box)
    return im.resize((im.width*z,im.height*z),Image.NEAREST)
V=Image.new('RGB',(2100,2400),'white'); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(spr('sprite_r3/sprite.png',8),'r3 (broek 50/33/17)'),(spr('sprite_r1/sprite.png',8),'r1'),(modelvak(0,0,64,64,8),'model r10_k8'),(spr('sprite_r3/variant_tertielen.png',8),'variant: broek tertielen 33/33/33')]):
    V.paste(im,(10+i*522,30)); d.text((10+i*522,10),t+' 8x',fill='black')
y=570; bb=(12,36,56,64)
for i,(im,t) in enumerate([(spr('sprite_r3/sprite.png',12,bb),'broek r3 12x'),(spr('sprite_r1/sprite.png',12,bb),'broek r1'),(modelvak(*bb,12),'model')]):
    V.paste(im,(10+i*540,y+20)); d.text((10+i*540,y),t,fill='black')
y+=370; kb=(14,8,46,34)
B=Image.open('../../../../graphics/pokemon/bibarel/anim_front.png').convert('RGB').crop((4,6,36,32)).resize((32*12,26*12),Image.NEAREST)
for i,(im,t) in enumerate([(spr('sprite_r3/kraag_proef.png',12,kb),'kraagproef 1: Bibarel-wang rechts, binnen de kraagzone'),(spr('sprite_r3/kraag_proef2.png',12,kb),'kraagproef 2: bolletjes 1-2 px over stam/schouder'),(spr('sprite_r3/sprite.png',12,kb),'r3 = r1-kraag'),(modelvak(*kb,12),'model'),(B,'Bibarel Gen 3')]):
    V.paste(im,(10+i*400,y+20)); d.text((10+i*400,y),t,fill='black')
y+=350
for j,bg in enumerate([(248,248,248),(40,40,48)]):
    for i,p in enumerate(['sprite_r3/sprite.png','sprite_r3/variant_tertielen.png','sprite_r1/sprite.png','sprite_r3/kraag_proef.png','sprite_r3/kraag_proef2.png']):
        o=laad(p); im=Image.new('RGB',(64,64),bg); im.paste(Image.fromarray(rgb(o)),(0,0),Image.fromarray(((o>0)*255).astype('uint8')))
        V.paste(im,(10+i*80,y+20+j*80))
d.text((10,y),'1x licht/donker: r3, tertielen, r1, kraagproef 1, kraagproef 2',fill='black')
V.crop((0,0,2100,y+190)).save('sprite_r3/vel.png')
