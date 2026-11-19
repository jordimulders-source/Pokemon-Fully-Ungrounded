# vel.png (r2): r2 8x | r1 8x | model verkleind (zelfde schaal) 8x | 1x op licht en donker | close-ups kop en poten 12x naast het model
import numpy as np; from PIL import Image,ImageDraw
from close import crop
def rgba(fn,box=None):
    im=Image.open(fn); im.save('/tmp/_t.png',transparency=0) if im.mode=='P' else None
    im=Image.open('/tmp/_t.png').convert('RGBA') if im.mode=='P' else im.convert('RGBA')
    return im.crop(box) if box else im
def on(im,c):
    b=Image.new('RGBA',im.size,c+(255,)); b.alpha_composite(im); return b.convert('RGB')
BG=(200,220,255)
S=rgba('../palpaca.png'); O=rgba('../../../ronde17/variant_kop/anim_front.png',(0,0,64,64))
oy,ox=np.load('plaats.npy'); Z=np.load('zones_nat.npy'); ys,xs=np.nonzero(Z!='.'); H,W=np.load('zone_t.npy').shape; s=(ys.max()+1-ys.min())/H
bx=(xs.min()+xs.max()+1)/2-W*s/2; by=ys.min()
N=Image.open('natief.png').convert('RGB')
# model op dezelfde schaal in een 64x64-vak op dezelfde plek
mx0=bx-ox*s; my0=by-oy*s
Nw=Image.new('RGB',(N.width+400,N.height+400),(255,255,255)); Nw.paste(N,(200,200)); N=Nw; mx0+=200; my0+=200
M=N.crop((int(round(mx0)),int(round(my0)),int(round(mx0+64*s)),int(round(my0+64*s)))).resize((512,512),Image.LANCZOS)
R1=rgba('../../r1/palpaca.png')
top=[on(S,BG).resize((512,512),0),on(R1,BG).resize((512,512),0),M]
labels=['r2 (8x)','r1 (8x)','model, zelfde schaal (8x)']
k1=crop(0,0,20,26,12); k2=crop(0,33,33,15,12)
Wd=3*512+40; Hd=512+30+150+30+max(k1.height,k2.height)+10
v=Image.new('RGB',(Wd,Hd),(255,255,255)); d=ImageDraw.Draw(v)
for i,(im,l) in enumerate(zip(top,labels)): v.paste(im,(i*(512+20),20)); d.text((i*532+4,4),l,fill=(0,0,0))
y=20+512+10; d.text((4,y),'r2 1x op licht en donker (+ 2x)',fill=(0,0,0)); y+=16
x=4
for c in [(255,255,255),(200,220,255),(40,40,48),(24,24,24)]:
    v.paste(on(S,c),(x,y)); x+=70
for c in [(255,255,255),(40,40,48)]:
    v.paste(on(S,c).resize((128,128),0),(x,y)); x+=136
x+=20
for c in [(255,255,255),(40,40,48)]:
    v.paste(on(O,c),(x,y)); x+=70
for c in [(255,255,255),(40,40,48)]:
    v.paste(on(R1,c),(x,y)); x+=70
d.text((x,y),'<- oude sprite ronde17 1x | r1 1x',fill=(0,0,0))
y+=150; d.text((4,y),'close-up 12x: kop (r2 | model) en poten (r2 | model)',fill=(0,0,0)); y+=16
v.paste(k1,(4,y)); v.paste(k2,(k1.width+30,y))
v.save('../vel.png'); print(v.size)
