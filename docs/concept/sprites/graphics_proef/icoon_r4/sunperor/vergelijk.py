"""vergelijk_8x.png: front | r3 | r4 f1 | r4 f2 | Xatu | Noctowl (in-game icon.png, GBA-palet), 8x op groen, met 1x-rij. Vanuit deze map."""
import numpy as np
from PIL import Image,ImageDraw
R='../../../../../../'
def ipal(k): L=open(R+f'graphics/pokemon/icon_palettes/pal{k}.pal').read().split('\n'); return [int(v) for l in L[3:19] for v in l.split()[:3]]
def rgba(im):
    a=np.array(im); r=im.convert('RGBA'); r.putalpha(Image.fromarray(((a>0)*255).astype('uint8'))); return r
def buur(n,k):
    a=np.array(Image.open(R+f'graphics/pokemon/{n}/icon.png'))[:32]; p=Image.fromarray(a,'P'); p.putpalette(ipal(k)); return rgba(p)
F=rgba(Image.open('../../../koningstiran/af/sapa_inca.png').crop((0,0,64,64)))
r3=rgba(Image.open('../../icoon_r3/sunperor/icon.png').crop((0,0,32,32)))
I=Image.open('icon.png'); f1=rgba(I.crop((0,0,32,32))); f2=rgba(I.crop((0,32,32,64)))
T=[('front (4x)',F),('r3',r3),('r4 f1',f1),('r4 f2',f2),('Xatu (pal0)',buur('xatu',0)),('Noctowl (pal2)',buur('noctowl',2))]
W=Image.new('RGB',(len(T)*266+10,330),(98,156,131)); d=ImageDraw.Draw(W)
for i,(t,im) in enumerate(T):
    b=im.resize((256,256),Image.NEAREST); W.paste(b,(10+i*266,24),b); d.text((10+i*266,6),t,fill=0)
x=10
for _,im in T[1:]: W.paste(im,(x,290),im); x+=36
d.text((x+4,300),'1x',fill=0); W.save('vergelijk_8x.png')
