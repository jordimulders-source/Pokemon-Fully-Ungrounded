# vel.py ronde 6: r6 | r1 | Gemini r5 | model r10 (8x, vergelijkbare schaal); tuinbroek 12x r6 | r5-uitsnede; 1x licht/donker
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
G5=Image.open('gemini/r5.png').convert('RGB')
g5=G5.crop((60,100,960,1000)).resize((512,512),Image.LANCZOS)
V=Image.new('RGB',(2110,1500),'white'); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(spr('sprite_r6/sprite.png',8),'r6'),(spr('sprite_r1/sprite.png',8),'r1'),(g5,'Gemini r5 (vorm)'),(modelvak(0,0,64,64,8),'model r10_k8 (kleuren)')]):
    V.paste(im,(10+i*522,30)); d.text((10+i*522,10),t+' 8x',fill='black')
y=570; bb=(12,26,56,62)
V.paste(spr('sprite_r6/sprite.png',12,bb),(10,y+20)); d.text((10,y),'tuinbroek r6 12x',fill='black')
V.paste(G5.crop((250,360,720,820)).resize((432,432),Image.LANCZOS),(560,y+20)); d.text((560,y),'Gemini r5 uitsnede',fill='black')
V.paste(modelvak(*bb,12),(1010,y+20)); d.text((1010,y),'model r10',fill='black')
y+=480
for j,bg in enumerate([(248,248,248),(40,40,48)]):
    for i,p in enumerate(['sprite_r6/sprite.png','sprite_r5/sprite.png','sprite_r1/sprite.png']):
        o=laad(p); im=Image.new('RGB',(64,64),bg); im.paste(Image.fromarray(rgb(o)),(0,0),Image.fromarray(((o>0)*255).astype('uint8')))
        V.paste(im,(10+i*80,y+20+j*80))
d.text((10,y),'1x licht/donker: r6, r5, r1',fill='black')
V.crop((0,0,2110,y+190)).save('sprite_r6/vel.png')
