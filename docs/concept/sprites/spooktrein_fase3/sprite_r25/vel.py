# keuring_vel: boven 8x r25 | r24 | model; midden 2x en 1x r25, r24 naast Gen 3 metaal/geest; onder 16x de reparatiezones.
from PIL import Image, ImageDraw
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/'
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def rgba(p,crop=True):
    im=Image.open(p)
    if crop: im=im.crop((0,0,64,64))
    q=im.convert('RGBA'); A=im.load(); B=q.load()
    for y in range(64):
        for x in range(64):
            if A[x,y]==0: B[x,y]=(0,0,0,0)
    return q
r25=rgba(D+'sprite_r25/sprite.png'); r24=rgba(D+'sprite_r24/sprite.png')
mod=Image.open(D+'model/model.webp').convert('RGBA').resize((512,512),Image.LANCZOS)
refs=[rgba(G+n+'/anim_front.png') for n in ['forretress','skarmory','steelix','magcargo','claydol','gengar','haunter','koffing']]
W=1700; V=Image.new('RGBA',(W,1500),(248,248,248,255)); d=ImageDraw.Draw(V)
def put(im,x,y,z):
    b=im.resize((im.width*z,im.height*z),Image.NEAREST); V.paste(b,(x,y),b)
put(r25,10,30,8); put(r24,540,30,8); V.paste(mod,(1070,30),mod)
d.text((10,10),'r25 (8x)',fill=0); d.text((540,10),'r24 (8x)',fill=0); d.text((1070,10),'model',fill=0)
y=560; d.text((10,y),'2x: r25, r24, Forretress, Skarmory, Steelix, Magcargo, Claydol, Gengar, Haunter, Koffing',fill=0)
for i,im in enumerate([r25,r24]+refs): put(im,10+i*136,y+20,2)
y=720; d.text((10,y),'1x (zelfde volgorde), ook op donker',fill=0)
for i,im in enumerate([r25,r24]+refs): put(im,10+i*70,y+20,1)
V.paste((40,40,48,255),(10,y+90,10+70*10,y+160))
for i,im in enumerate([r25,r24]+refs): put(im,10+i*70,y+93,1)
y=900; d.text((10,y),'16x reparatiezones: schoorsteen (12-25,13-21) | kop/kier (24-33,30-37) | chassis (43-56,37-43); boven r25, onder r24',fill=0)
zones=[(12,13,25,21),(24,30,33,37),(43,37,56,43)]
x=10
for (x0,y0,x1,y1) in zones:
    for j,im in enumerate([r25,r24]):
        c=im.crop((x0,y0,x1+1,y1+1)); put(c,x,y+20+j*(c.height*16+10),16)
    x+=(x1-x0+1)*16+20
V.save(D+'sprite_r25/keuring_vel.png')
