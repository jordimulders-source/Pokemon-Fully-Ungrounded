"""Vel kleurronde 2: pre-evo, kleur1-E en de nieuwe varianten op 4x en 1x, licht en donker,
plus Ekans, Sandaconda, Hippowdon; onderaan een 8x-uitsnede van de staart."""
import sys
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'
D=R+'docs/concept/sprites/salticonda/'
def ld(f):
    p=Image.open(f).crop((0,0,64,64)); P=p.load(); im=p.convert('RGBA'); Q=im.load()
    for x in range(64):
        for y in range(64):
            if P[x,y]==0: Q[x,y]=(0,0,0,0)
    return im
names=sys.argv[1:] or ['salticonda_A','salticonda_B']
new=[(n.replace('salticonda_','kop '),ld(D+'kleur2/%s.png'%n)) for n in names]
pre=('Silicobra-U',ld(D+'../silicobra_uyuni/af/silicobra_uyuni.png'))
E=('kleur1 E',ld(D+'kleur1/salticonda_E.png'))
refs=[(n.capitalize(),ld(R+'graphics/pokemon/%s/anim_front.png'%n)) for n in ['ekans','sandaconda','hippowdon']]
LIGHT=(236,232,222,255); DARK=(44,44,52,255)
big=[pre,E]+new
W=max(10+len(big)*266, 10+ (len(big)+3)*72+10); H=2*(30+256+20+64+20)+30+8*26+20
vel=Image.new('RGBA',(W,H),LIGHT); d=ImageDraw.Draw(vel)
half=30+256+20+64+20
d.rectangle([0,half,W,2*half],fill=DARK)
for y0,col in [(0,(30,30,30,255)),(half,(230,230,230,255))]:
    x=10
    for lab,im in big:
        d.text((x,y0+8),lab+'  4x',fill=col); vel.alpha_composite(im.resize((256,256),Image.NEAREST),(x,y0+26)); x+=266
    x=10
    for lab,im in big+refs:
        vel.alpha_composite(im,(x,y0+30+256+10)); d.text((x,y0+30+256+76),lab[:11],fill=col); x+=72
y0=2*half+10
d.text((10,y0),'staart 8x (uitsnede x44-63, y28-61)',fill=(30,30,30,255))
x=10
for lab,im in new:
    c=im.crop((44,34,64,61)).resize((160,216),Image.NEAREST)
    bg=Image.new('RGBA',c.size,(150,200,160,255)); bg.alpha_composite(c); vel.alpha_composite(bg,(x,y0+14)); x+=176
vel.save(D+'kleur2/vel.png'); print(vel.size)
