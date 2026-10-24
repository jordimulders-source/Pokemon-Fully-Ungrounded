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
sprites=[('variant sleep',Image.open(os.path.join(HERE,'kolibrie_variant_sleep.png')).convert('RGBA')),
         ('ronde 3',Image.open(os.path.join(HERE,'kolibrie.png')).convert('RGBA')),
         ('variant lint',Image.open(os.path.join(HERE,'kolibrie_variant_lint.png')).convert('RGBA'))]
sprites=[sprites[1],sprites[2],sprites[0]]
sprites+=[(n,load(n)) for n in ['venomoth','yanma','swellow','articuno','fearow','honchkrow']]
LIGHT,DARK=(232,232,224,255),(40,40,60,255)
n=len(sprites); W=Image.new('RGBA',(10+n*200,10+2*(192+20)+2*(64+20)+10),LIGHT)
d=ImageDraw.Draw(W)
y=10
for bg in (LIGHT,DARK):
    band=Image.new('RGBA',(W.width,192+20),bg); W.alpha_composite(band,(0,y))
    for i,(t,im) in enumerate(sprites):
        W.alpha_composite(im.resize((192,192),Image.NEAREST),(10+i*200,y))
        d.text((10+i*200,y+194),t+', 3x',fill='black' if bg==LIGHT else 'white')
    y+=212
for bg in (LIGHT,DARK):
    band=Image.new('RGBA',(W.width,84),bg); W.alpha_composite(band,(0,y))
    for i,(t,im) in enumerate(sprites):
        W.alpha_composite(im,(10+i*200,y+2)); W.alpha_composite(im,(10+i*72,y+2)) if False else None
    d.text((W.width-200,y+30),'1x',fill='black' if bg==LIGHT else 'white')
    y+=84
# compacte 1x-rij (zoals in het gevecht, dicht op elkaar)
W2=Image.new('RGBA',(W.width,W.height+2*76),LIGHT); W2.alpha_composite(W,(0,0))
for k,bg in enumerate((LIGHT,DARK)):
    band=Image.new('RGBA',(n*70+20,74),bg); W2.alpha_composite(band,(0,W.height+k*76))
    for i,(t,im) in enumerate(sprites): W2.alpha_composite(im,(10+i*70,W.height+k*76+5))
ImageDraw.Draw(W2).text((n*70+30,W.height+30),'1x compact: ronde 3 | variant lint | variant sleep | venomoth | yanma | swellow | articuno | fearow | honchkrow',fill='black')
W2.save(os.path.join(HERE,'vel.png'))
