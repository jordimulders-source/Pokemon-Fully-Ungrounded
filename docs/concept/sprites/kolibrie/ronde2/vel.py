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
r2=Image.open(os.path.join(HERE,'kolibrie.png')).convert('RGBA')
r1=Image.open(os.path.join(HERE,'../ronde1/kolibrie.png')).convert('RGBA')
sil=Image.open(os.path.join(HERE,'../silhouet/silhouet_v6_groot_1x.png')).convert('RGBA')
refs=['venomoth','ho_oh','fearow','articuno','talonflame','ninjask']
W=Image.new('RGBA',(10+3*202+150, 10+192+20+64+30),(232,232,224,255))
d=ImageDraw.Draw(W)
for i,(im,t) in enumerate([(r1,'ronde 1, 3x'),(r2,'ronde 2, 3x'),(sil,'silhouet v6 groot, 3x')]):
    W.alpha_composite(im.resize((192,192),Image.NEAREST),(10+i*202,10)); d.text((10+i*202,205),t,fill='black')
x0=10+3*202
for i,bg in enumerate([(232,232,224,255),(120,160,120,255),(40,40,60,255),(248,248,248,255)]):
    b=Image.new('RGBA',(64,64),bg); b.alpha_composite(r2); W.alpha_composite(b,(x0+(i%2)*68,10+(i//2)*70))
d.text((x0,150),'ronde 2, 1x',fill='black')
y=225
W.alpha_composite(r1,(10,y)); W.alpha_composite(r2,(80,y))
for i,n in enumerate(refs):
    W.alpha_composite(load(n),(150+70*i,y))
d.text((10,y+66),'1x: ronde 1 | ronde 2 | '+' | '.join(refs),fill='black')
W.save(os.path.join(HERE,'vel.png'))
