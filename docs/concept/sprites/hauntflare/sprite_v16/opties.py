# v16-opties: rechter mondhoek punteriger (naar Jordi's haakje + pixelref) en mondkleur als gloeiende kern (bestaande vlamtinten).
from PIL import Image, ImageDraw, ImageFont; import numpy as np
im=Image.open('sprite_v15/hauntflare_v15.png'); pal=im.getpalette(); V=np.array(im)
MOND=[(x,y) for y in range(33,39) for x in range(19,34)]
def hoek(a,k):
    if k=='K1':   # hoek 1 px naar rechts, punt omhoog op (34,32)
        a[33,33]=10; a[33,34]=1; a[32,34]=1
    if k=='K2':   # langere punt: tot (35,31)
        a[33,33]=10; a[33,34]=1; a[32,34]=10; a[32,35]=1; a[31,35]=1; a[31,34]=1 if a[31,34]!=1 else 1
def kleur(a,c):
    if c=='orig': return
    bin_,tong={'A':(15,13),'B':(11,12)}[c]
    for x,y in MOND+[(33,33),(34,32)]:
        if a[y,x]==10: a[y,x]=bin_
        elif a[y,x]==5: a[y,x]=tong
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',18)
def rgb(a):
    o=Image.fromarray(a,'P'); o.putpalette(pal); o.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/931d0048-d45a-55a4-a2ad-8ad05568e8ad/scratchpad/o.png',transparency=0)
    r=Image.open('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/931d0048-d45a-55a4-a2ad-8ad05568e8ad/scratchpad/o.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(r); return bg.convert('RGB'),o
rijen=[('orig','v15 mondkleur'),('A','kern: oranjerood + geel'),('B','kern: rood + oranje')]
kols=['K0','K1','K2']
v=Image.new('RGB',(3*(300+20)+20,3*(270+30)+20),'white'); d=ImageDraw.Draw(v)
for i,(c,cn) in enumerate(rijen):
    for j,k in enumerate(kols):
        a=V.copy(); hoek(a,k); kleur(a,c); r,o=rgb(a); o.save(f'sprite_v16/optie_{c}_{k}.png',transparency=0)
        x=20+j*320; y=20+i*300
        d.text((x,y),f'{cn} | hoek {k}',fill='black',font=f)
        v.paste(r.crop((16,26,41,44)).resize((300,216),Image.NEAREST),(x,y+24)); v.paste(r,(x,y+244)); 
v.save('sprite_v16/opties.png')
