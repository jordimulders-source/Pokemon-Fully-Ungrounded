import numpy as np
from PIL import Image, ImageDraw
S='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/'; G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
BG=(196,206,200)
def rgba(f,crop=None):
    im=Image.open(f).convert('RGBA')
    if crop: im=im.crop(crop)
    return im
def op(im,k,bg=BG):
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB').resize((im.size[0]*k,im.size[1]*k),Image.NEAREST)
r16=rgba('capykart.png'); r15=rgba('../r15b/capykart_creme.png')
kaal=rgba('../kaal.png'); kk=Image.new('RGBA',(64,64)); kk.paste(kaal,(1,64-kaal.size[1]))
rij1=[r16,r15,kk,rgba(S+'viscacha/af/viscacha.png'),rgba(S+'skinguin/af/skinguin.png')]
lab1=['r16','r15b','model (kale reductie)','viscacha (Zapacha)','skinguin']
kop16=r16.crop((12,8,44,36)); rat=rgba(G+'raticate/anim_front.png',(4,18,36,46)); vis=rgba(S+'viscacha/af/viscacha.png',(2,12,34,40))
tor=r16.crop((42,0,64,34)); pory=rgba(G+'porygon/anim_front.png',(8,16,52,50))
W=5*512+6*8; H=40+512+40+max(28*12,34*12)+40+140
V=Image.new('RGB',(W,H),(40,40,48)); d=ImageDraw.Draw(V)
x=8
for im,l in zip(rij1,lab1): V.paste(op(im,8),(x,32)); d.text((x,10),l,fill=(255,255,255)); x+=520
y=32+512+36; x=8
for im,l in [(kop16,'r16 kop 12x'),(rat,'raticate kop 12x (Gen 3)'),(vis,'viscacha kop 12x'),(tor,'r16 toren 12x'),(pory,'porygon 12x (Gen 3)')]:
    o=op(im,12) if im.size[0]<=32 else op(im,10); V.paste(o,(x,y+16)); d.text((x,y),l,fill=(255,255,255)); x+=o.size[0]+16
y=H-130; x=8
for bg in [(248,248,248),(24,24,32),(152,208,160)]:
    for im in (r16,r15):
        V.paste(op(im,1,bg),(x,y)); V.paste(op(im,2,bg),(x+70,y)); x+=206
    x+=20
d.text((8,y-18),'1x en 2x op licht / donker / Gen 3-groen: r16 links, r15b rechts',fill=(255,255,255))
V.save('vel.png'); print(V.size)
