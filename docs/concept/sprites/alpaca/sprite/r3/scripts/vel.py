# Vel r3: r3 8x | r2 8x | Mareep, Skitty 8x | 1x en 2x op licht/donker (A, B, r2) | close-up kop 12x: model op spriteraster, A, B, r2.
from PIL import Image, ImageDraw
import subprocess
G='../../../../../../../graphics/pokemon/'
def rgba(p):
    return Image.open(p).convert('RGBA')
def ref(n):
    im=Image.open(G+n+'/anim_front.png').crop((0,0,64,64))
    p=open(G+n+'/normal.pal').read().split('\n')[3:19]
    im.putpalette([int(c) for l in p for c in l.split()]); im=im.convert('RGBA')
    d=list(im.getdata()); bg=d[0]; im.putdata([(0,0,0,0) if q==bg else q for q in d]); return im
A=rgba('../palpaca.png'); B=rgba('../palpaca_B.png'); R2=rgba('../../r2/palpaca.png')
subprocess.run(['python3','modelkop.py','15','35','14','35','modelkop_12x.png'],check=True)
MK=Image.open('modelkop_12x.png').convert('RGBA')
W=Image.new('RGBA',(4*512+50,512+40+260+40+21*12+40),(255,255,255,255)); d=ImageDraw.Draw(W)
for i,(im,t) in enumerate([(A,'r3 (A)'),(R2,'r2'),(ref('mareep'),'Mareep'),(ref('skitty'),'Skitty')]):
    z=im.resize((512,512),Image.NEAREST); W.paste(z,(i*(512+16),20),z); d.text((i*528+4,4),t,fill=(0,0,0))
y=572
for j,bg in enumerate([(248,248,248,255),(40,40,48,255)]):
    x0=j*1060; d.rectangle([x0,y,x0+1040,y+250],fill=bg)
    for k,im in enumerate([A,B,R2]):
        W.paste(im,(x0+10+k*80,y+10),im); z=im.resize((128,128),Image.NEAREST); W.paste(z,(x0+260+k*140,y+10),z)
d.text((4,y-14),'1x en 2x op licht en donker: A, B, r2',fill=(0,0,0))
y=572+290
cr=(15,14,35,35)
for k,(im,t) in enumerate([(MK,'model op spriteraster'),(A,'A'),(B,'B (verre oog)'),(R2,'r2')]):
    z=im if im is MK else im.crop(cr).resize((240,252),Image.NEAREST)
    W.paste(z,(k*270,y),z); d.text((k*270,y-14),t+' 12x, x15-34 y14-34',fill=(0,0,0))
W.save('../vel.png'); print('vel', W.size)
