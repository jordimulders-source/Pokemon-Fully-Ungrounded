"""vergelijk_8x.png: front | onderlaag | icoon f1 | f2 | viscacha-icoon | 2 echte buren (in-game icon.png), alles 8x op groen.
python3 maak_vergelijk.py <soort> <front.png> <onderlaag.png> <buur1> <buur2>   (vanuit de repo-root)"""
import sys,os,re,numpy as np
from PIL import Image,ImageDraw
soort,front,onder,b1,b2=sys.argv[1:6]
D=f'docs/concept/sprites/graphics_proef/icoon_r3/{soort}/'
def ipal(k):
    L=open(f'graphics/pokemon/icon_palettes/pal{k}.pal').read().split('\n'); return [int(v) for l in L[3:19] for v in l.split()[:3]]
IPI={}
for fn in os.listdir('src/data/pokemon/species_info'):
    for mm in re.finditer(r'\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \},',open('src/data/pokemon/species_info/'+fn).read(),re.S):
        v=re.search(r'iconPalIndex = (?:P_GBA_STYLE_SPECIES_ICONS \? \d : )?(\d)',mm.group(2))
        if v: IPI[mm.group(1).lower()]=int(v.group(1))
def rgba(im):
    a=np.array(im); r=im.convert('RGBA'); r.putalpha(Image.fromarray(((a>0)*255).astype('uint8'))); return r
def buur(n):
    im=Image.open(f'graphics/pokemon/{n}/icon.png').crop((0,0,32,32)); im=im.convert('P') if im.mode!='P' else im
    a=np.array(im); p=Image.fromarray(a,'P'); p.putpalette(ipal(IPI.get(n,0))); return rgba(p)
F=rgba(Image.open(front).crop((0,0,64,64)))
I=Image.open(D+'icon.png'); f1=rgba(I.crop((0,0,32,32))); f2=rgba(I.crop((0,32,32,64)))
O=rgba(Image.open(D+onder)); V=rgba(Image.open('docs/concept/sprites/viscacha/icoon/af/icon.png').crop((0,0,32,32)))
tegels=[('front (4x)',F.resize((256,256),Image.NEAREST)),('onderlaag',O.resize((256,256),Image.NEAREST)),('icoon f1',f1.resize((256,256),Image.NEAREST)),
        ('icoon f2',f2.resize((256,256),Image.NEAREST)),('viscacha-icoon',V.resize((256,256),Image.NEAREST)),(b1,buur(b1).resize((256,256),Image.NEAREST)),(b2,buur(b2).resize((256,256),Image.NEAREST))]
W=Image.new('RGB',(len(tegels)*266+10,330),(98,156,131)); d=ImageDraw.Draw(W)
for i,(t,im) in enumerate(tegels):
    W.paste(im,(10+i*266,24),im); d.text((10+i*266,6),t,fill=0)
x=10
for im in [f1,f2,V,buur(b1),buur(b2)]:
    W.paste(im,(x,290),im); x+=36
d.text((x+4,300),'1x',fill=0)
W.save(D+'vergelijk_8x.png'); print('ok',D+'vergelijk_8x.png')
