# vel.png: (1) kop 12x: r3 A | r4 A | r4 B | r4 C | model | Gen 3-referentiekoppen (gespiegeld)  (achtergrond lichtgrijs, zodat wit leest)
#          (2) r4 A/B/C geheel op 8x ; (3) 1x r3 A / r4 A/B/C / Lombre op wit en donker
import numpy as np; from PIL import Image, ImageDraw
from gemeen import rgb
G=(200,204,212); W=(255,255,255); D=(40,40,48)
LOM='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/lombre/anim_front_gba.png'
F=['../r3/lombre_gaucho_r3_A.png']+['lombre_gaucho_r4_%s.png'%v for v in 'ABC']; NM=['r3 A','r4 A','r4 B','r4 C']
def spr(p,z,bg): return Image.fromarray(rgb(np.array(Image.open(p)),bg)).resize((64*z,64*z),Image.NEAREST)
def gen3(z,bg,sp=True):
    im=Image.open(LOM).convert('RGBA').crop((0,0,64,64))
    if sp: im=im.transpose(Image.FLIP_LEFT_RIGHT)
    c=Image.new('RGBA',(64,64),bg+(255,)); c.alpha_composite(im); return c.convert('RGB').resize((64*z,64*z),Image.NEAREST)
def model(z,box):
    # model op dezelfde schaal als de sprite (zie r1/vel.py model_op_schaal), uitsnede box
    m=Image.open('../../r1/gemini_r1.png').convert('RGB'); meta=np.load('kaal_meta.npy'); oy,ox,Y0,X0=meta[:4]
    P=10.24; PH=9.25-P; s=z*(42/54)/P; t=z*(57/74)/P
    big=m.resize((int(1024*s),int(1024*t)),Image.LANCZOS); c=Image.new('RGB',(64*z,64*z),W)
    c.paste(big,(int(X0*z-(PH+ox*P)*s),int(Y0*z-(PH+oy*P)*t))); return c.crop(tuple(v*z for v in box))
def art(w,h,z):
    a=Image.open('../../referenties/lombre_artwork.png').convert('RGBA').crop((170,180,600,520)).transpose(Image.FLIP_LEFT_RIGHT)
    c=Image.new('RGBA',a.size,G+(255,)); c.alpha_composite(a); c=c.convert('RGB')
    s=min(w*z/c.width,h*z/c.height); return c.resize((int(c.width*s),int(c.height*s)),Image.LANCZOS)
def label(im,t):
    c=Image.new('RGB',(im.width,im.height+16),(220,220,220)); c.paste(im,(0,16)); ImageDraw.Draw(c).text((4,2),t,fill=(0,0,0)); return c
def rij(ims,gap=8):
    w=sum(i.width for i in ims)+gap*(len(ims)-1); h=max(i.height for i in ims)
    c=Image.new('RGB',(w,h),(170,170,170)); x=0
    for i in ims: c.paste(i,(x,0)); x+=i.width+gap
    return c
z=12; box=(16,20,40,37)
r1=rij([label(spr(p,z,G).crop(tuple(v*z for v in box)),n+' (12x)') for p,n in zip(F,NM)]+[label(model(z,box),'model (12x)'),
        label(art(box[2]-box[0],box[3]-box[1],z),'Lombre-artwork, kop gespiegeld')])
def refkop(n,b,z=12):
    im=Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/%s/anim_front_gba.png'%n).convert('RGBA').crop((0,0,64,64))
    c=Image.new('RGBA',(64,64),G+(255,)); c.alpha_composite(im); return label(c.convert('RGB').crop(b).resize(((b[2]-b[0])*z,(b[3]-b[1])*z),Image.NEAREST),n+' Gen 3 (12x)')
r1b=rij([refkop('nuzleaf',(16,8,44,26)),refkop('ludicolo',(12,12,40,28)),refkop('lotad',(10,26,44,44))])
r2=rij([label(spr(p,8,W).crop((8*8,2*8,56*8,64*8)),n+' (8x)') for p,n in zip(F[1:],NM[1:])])
een=[]
for bg in (W,D):
    c=Image.new('RGB',(5*64,64),bg)
    for i,p in enumerate(F): c.paste(Image.fromarray(rgb(np.array(Image.open(p)),bg)),(i*64,0))
    c.paste(gen3(1,bg,False),(256,0)); een.append(c)
r3=label(rij([e.resize((e.width*2,e.height*2),Image.NEAREST) for e in een]),'1x (hier 2x getoond): r3 A | r4 A | r4 B | r4 C | Gen 3-Lombre, op wit en donker')
r3b=label(rij(een),'echte 1x')
rs=(r1,r1b,r2,r3,r3b); H=sum(r.height for r in rs)+16*len(rs); Wd=max(r.width for r in rs)
v=Image.new('RGB',(Wd,H),(170,170,170)); y=0
for r in rs: v.paste(r,(0,y)); y+=r.height+16
v.save('vel.png'); print(v.size)
