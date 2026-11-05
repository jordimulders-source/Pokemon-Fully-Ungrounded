from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
F2='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/nachtaap_evo/af/nachtaap_evo.png'
L=(255,255,255,255); D=(40,40,52,255)
def op(p,bg):
    im=Image.open(p).convert('RGBA')
    if im.size[1]==128: im=im.crop((0,0,64,64))
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b
rows=[('7c zonder patroon','../../kleur/ronde7c/nachtaap_fase3.png'),('A: 3 taps banden (taal fase 2)','optie_A.png'),('B: 3 volle ringen (Furret)','optie_B.png')]
refs=[('fase 2',F2),('furret',G+'furret/anim_front_gba.png'),('dusclops',G+'dusclops/anim_front_gba.png')]
RH=250; W=20+192*2+20+64*2+30+36*8+20
sh=Image.new('RGBA',(W,RH*3+250),(225,225,232,255)); d=ImageDraw.Draw(sh)
for i,(n,p) in enumerate(rows):
    y=i*RH+4; x=10; d.text((x,y),n,fill=(0,0,0,255)); y+=16
    sh.paste(op(p,L).resize((192,192),Image.NEAREST),(x,y)); x+=196
    sh.paste(op(p,D).resize((192,192),Image.NEAREST),(x,y)); x+=210
    sh.paste(op(p,L),(x,y)); sh.paste(op(p,D),(x+68,y)); x+=150
    c=op(p,L).crop((20,27,48,49)); sh.paste(c.resize((c.size[0]*8,c.size[1]*8),Image.NEAREST),(x,y))
    d.text((x,y+180),'8x rug',fill=(0,0,0,255))
y=3*RH+4; d.text((10,y),'referenties 3x (licht/donker) en 1x',fill=(0,0,0,255)); y+=16
for j,(n,p) in enumerate(refs):
    x=10+j*270
    sh.paste(op(p,L).resize((192,192),Image.NEAREST),(x,y)); sh.paste(op(p,L),(x+196,y)); sh.paste(op(p,D),(x+196,y+68))
    d.text((x,y+196),n,fill=(0,0,0,255))
sh.save('vel_opties.png')
