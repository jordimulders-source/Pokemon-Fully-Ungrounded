# Vergelijkingsvel: r4 (huidig) / selout A / selout B naast 5 echte Gen 3-sprites, op 1x (3 achtergronden) en 4x.
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/'; D=R+'docs/concept/sprites/steenmozaiek/sprite/r4/'
def rgba(p,crop=True):
    im=Image.open(p)
    if crop: im=im.crop((0,0,64,64))
    im=im.convert('RGBA'); px=im.load()
    t=Image.open(p).getpalette()[:3]
    for y in range(64):
        for x in range(64):
            if Image.open(p).crop((0,0,64,64)).getpixel((x,y))==0: px[x,y]=(0,0,0,0)
    return im
def rg(p):
    src=Image.open(p).crop((0,0,64,64)); im=src.convert('RGBA'); a=im.load(); s=src.load()
    for y in range(64):
        for x in range(64):
            if s[x,y]==0: a[x,y]=(0,0,0,0)
    return im
eigen=[rg(D+'steenjaguar_r4.png'),rg(D+'eindkeuring/selout_voorstel.png'),rg(D+'eindkeuring/selout_voorstel_b.png')]
echt=[rg(R+'graphics/pokemon/%s/anim_front.png'%s) for s in('raikou','absol','persian','entei','manectric')]
alle=eigen+echt
bgs=[(255,255,255),(48,48,64),(112,184,104)]
S=4
vel=Image.new('RGB',(len(alle)*64*S, 64*S+3*70),(255,255,255))
for i,sp in enumerate(alle):
    vel.paste(sp.resize((64*S,64*S),Image.NEAREST),(i*64*S,0),sp.resize((64*S,64*S),Image.NEAREST))
    for j,bg in enumerate(bgs):
        t=Image.new('RGB',(64*S,70),bg); t.paste(sp,(8,3),sp); t.paste(sp.resize((128,128),Image.NEAREST).crop((0,0,128,64)) if False else sp,(8,3),sp)
        vel.paste(t,(i*64*S,64*S+j*70))
vel.save(D+'eindkeuring/vel_buitenlijn.png')
# los: huidig vs A op 8x
v2=Image.new('RGB',(64*8*2+16,64*8),(255,255,255))
for i,sp in enumerate(eigen[:2]):
    v2.paste(sp.resize((512,512),Image.NEAREST),(i*(512+16),0),sp.resize((512,512),Image.NEAREST))
v2.save(D+'eindkeuring/huidig_vs_selout_8x.png')
