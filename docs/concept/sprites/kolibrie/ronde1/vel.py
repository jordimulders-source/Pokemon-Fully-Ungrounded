import os
from PIL import Image, ImageDraw
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,'../../../../..'))
def load(n):
    im=Image.open(os.path.join(ROOT,'graphics/pokemon',n,'anim_front.png'))
    p=[tuple(map(int,l.split())) for l in open(os.path.join(ROOT,'graphics/pokemon',n,'normal.pal')).read().split('\n')[3:19]]
    im=im.convert('P') if im.mode!='P' else im.copy()
    im.putpalette([c for t in p for c in t]+[0]*(768-48))
    r=im.convert('RGBA'); a=im.load(); q=r.load()
    for y in range(64):
        for x in range(64):
            if a[x,y]==0: q[x,y]=(0,0,0,0)
    return r.crop((0,0,64,64))
spr=Image.open(os.path.join(HERE,'kolibrie.png')).convert('RGBA')
sil=Image.open(os.path.join(HERE,'../silhouet/silhouet_v6_1x.png')).convert('RGBA')
refs=['venomoth','ho_oh','fearow','articuno','talonflame','ninjask']
W=Image.new('RGBA',(10+192+10+192+10+64*4+10, 10+192+20+64+30),(232,232,224,255))
d=ImageDraw.Draw(W)
W.alpha_composite(spr.resize((192,192),Image.NEAREST),(10,10)); d.text((10,205),'kolibrie ronde 1, 3x',fill='black')
W.alpha_composite(sil.resize((192,192),Image.NEAREST),(212,10)); d.text((212,205),'silhouet v6, 3x',fill='black')
x0=414
for i,bg in enumerate([(232,232,224,255),(120,160,120,255),(40,40,60,255),(248,248,248,255)]):
    b=Image.new('RGBA',(64,64),bg); b.alpha_composite(spr); W.alpha_composite(b,(x0+(i%2)*66,10+(i//2)*70))
d.text((x0,150),'1x op 4 achtergronden',fill='black')
y=225
W.alpha_composite(spr,(10,y))
for i,n in enumerate(refs):
    W.alpha_composite(load(n),(10+70*(i+1),y))
d.text((10,y+66),'1x: kolibrie | '+' | '.join(refs),fill='black')
W.save(os.path.join(HERE,'vel.png'))
