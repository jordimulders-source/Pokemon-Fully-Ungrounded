# vel.py: sprite 8x | kale reductie 8x | model ; kop 12x naast model ; varianten 4x ; 1x op licht en donker
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
from PIL import Image, ImageDraw
def x8(p,z=8):
    im=Image.open(p); im=im.convert('RGBA') if im.mode!='P' else Image.fromarray(rgb(laad(p)))
    return im.convert('RGB').resize((im.width*z,im.height*z),Image.NEAREST)
fig=np.load('sprite_r1/masker.npy'); yy,xx=np.where(fig)
M=Image.open('model/r10_k8.png').convert('RGB'); mx0,my0=xx.min(),yy.min(); s=64/(xx.max()-mx0+1); oy=64-round((yy.max()-my0+1)*s)
def modelvak(x0,y0,x1,y1,Z):
    A=np.asarray(M); W,H=(x1-x0)*Z,(y1-y0)*Z; out=np.full((H,W,3),255,'uint8')
    py,px=np.mgrid[0:H,0:W]; X=(mx0+(x0+px/Z)/s).astype(int); Y=(my0+(y0+py/Z-oy)/s).astype(int)
    ok=(X>=0)&(X<99)&(Y>=0)&(Y<99); out[ok]=A[Y[ok],X[ok]]; return Image.fromarray(out)
V=Image.new('RGB',(1600,1500),'white'); d=ImageDraw.Draw(V)
V.paste(x8('sprite_r1/sprite.png'),(10,30)); d.text((10,10),'sprite r1 (tuinbroek A: tot de enkels) 8x',fill='black')
V.paste(x8('sprite_r1/kaal_C.png'),(540,30)); d.text((540,10),'kale reductie (meerderheid per modelkleur, factor 0,711) 8x',fill='black')
V.paste(modelvak(0,0,64,64,8),(1070,30)); d.text((1070,10),'werkmodel r10_k8 op dezelfde schaal',fill='black')
y=560
V.paste(x8('sprite_r1/sprite.png',12).crop((14*12,4*12,46*12,30*12)),(10,y+20)); d.text((10,y),'kop 12x',fill='black')
V.paste(modelvak(14,4,46,30,12),(410,y+20)); d.text((410,y),'model kop, zelfde schaal',fill='black')
V.paste(x8('graphics_bibarel.png',12) if False else Image.new('RGB',(1,1),'white'),(0,0))
y2=y+350
for i,(p,t) in enumerate([('sprite_r1/sprite_A_enkels.png','A: tuinbroek tot de enkels'),('sprite_r1/sprite_B_halve_dij.png','B: tot halverwege de dij'),('sprite_r1/sprite_A_klepvoorstel.png','voorstel Claude: klep 1 tint lichter')]):
    V.paste(x8(p,4),(10+i*270,y2+20)); d.text((10+i*270,y2),t,fill='black')
# 1x op licht en donker
for j,bg in enumerate([(248,248,248),(40,40,48)]):
    for i,p in enumerate(['sprite_r1/sprite_A_enkels.png','sprite_r1/sprite_B_halve_dij.png']):
        o=laad(p); im=Image.new('RGB',(64,64),bg); im.paste(Image.fromarray(rgb(o)),(0,0),Image.fromarray(((o>0)*255).astype('uint8')))
        V.paste(im,(830+i*80,y2+20+j*80))
d.text((830,y2),'1x licht / donker (A, B)',fill='black')
# 2x
o=laad('sprite_r1/sprite.png'); im=Image.new('RGB',(64,64),(248,248,248)); im.paste(Image.fromarray(rgb(o)),(0,0),Image.fromarray(((o>0)*255).astype('uint8')))
V.paste(im.resize((128,128),Image.NEAREST),(1010,y2+20)); d.text((1010,y2+150),'2x',fill='black')
V.crop((0,0,1600,y2+300)).save('sprite_r1/vel.png')
