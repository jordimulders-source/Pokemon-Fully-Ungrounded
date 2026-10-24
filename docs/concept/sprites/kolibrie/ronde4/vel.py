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
sprites=[('ronde 3 variant sleep',Image.open(os.path.join(HERE,'../ronde3/kolibrie_variant_sleep.png')).convert('RGBA')),
         ('ronde 4',Image.open(os.path.join(HERE,'kolibrie.png')).convert('RGBA'))]
sprites+=[(n,load(n)) for n in ['venomoth','yanma','swellow','articuno','fearow','honchkrow']]
LIGHT,DARK=(232,232,224,255),(40,40,60,255)
n=len(sprites); W=Image.new('RGBA',(10+n*200,10+2*212+2*76+10),LIGHT); d=ImageDraw.Draw(W)
y=10
for bg in (LIGHT,DARK):
    W.alpha_composite(Image.new('RGBA',(W.width,212),bg),(0,y))
    for i,(t,im) in enumerate(sprites):
        W.alpha_composite(im.resize((192,192),Image.NEAREST),(10+i*200,y))
        d.text((10+i*200,y+194),t+', 3x',fill='black' if bg==LIGHT else 'white')
    y+=212
for bg in (LIGHT,DARK):
    W.alpha_composite(Image.new('RGBA',(W.width,76),bg),(0,y))
    for i,(t,im) in enumerate(sprites): W.alpha_composite(im,(10+i*70,y+6))
    d.text((10+n*70+20,y+30),'1x: ronde 3 variant sleep | ronde 4 | venomoth | yanma | swellow | articuno | fearow | honchkrow',fill='black' if bg==LIGHT else 'white')
    y+=76
W.save(os.path.join(HERE,'vel.png'))
