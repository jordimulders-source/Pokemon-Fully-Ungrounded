# vel.png: (1) A 8x | model op dezelfde schaal 8x | kale reductie 8x
#          (2) kop 12x: A | model | Gen 3-Lombre-kop (gespiegeld, zodat hij dezelfde kant op kijkt)
#          (3) 1x: A, B, C, Gen 3-Lombre, gaucho-Lotad op wit en donker
#          (4) mondvarianten A | B | C op 8x (kop)
import numpy as np; from PIL import Image, ImageDraw
from gemeen import rgb
W=(255,255,255); D=(40,40,48)
def spr(p,z,bg=W): return Image.fromarray(rgb(np.array(Image.open(p)) if p.endswith('png') else np.load(p),bg)).resize((64*z,64*z),Image.NEAREST)
def gen3(p,z,bg=W,spiegel=False):
    im=Image.open(p).convert('RGBA').crop((0,0,64,64))
    if spiegel: im=im.transpose(Image.FLIP_LEFT_RIGHT)
    c=Image.new('RGBA',(64,64),bg+(255,)); c.alpha_composite(im); return c.convert('RGB').resize((64*z,64*z),Image.NEAREST)
LOM='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/lombre/anim_front_gba.png'
LOT='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/lotad_regional/af/lotad_gaucho.png'
def model_op_schaal(z):
    """Model (1024x1024) zo geschaald dat de figuur even groot is als in de sprite (54x74 natief -> 42x57), op 64x64-raster x z."""
    m=Image.open('../../r1/gemini_r1.png').convert('RGB'); meta=np.load('kaal_meta.npy'); oy,ox,Y0,X0=meta[:4]
    P=10.24; PH=9.25-P; sx=42/54; sy=57/74
    # figuur-linksboven in het model (volle resolutie) -> spritepositie (X0,Y0)
    fx=PH+ox*P; fy=PH+oy*P
    s=z*sx/P; t=z*sy/P
    big=m.resize((int(1024*s),int(1024*t)),Image.LANCZOS)
    c=Image.new('RGB',(64*z,64*z),W); c.paste(big,(int(X0*z-fx*s),int(Y0*z-fy*t))); return c
def label(im,t):
    c=Image.new('RGB',(im.width,im.height+16),(220,220,220)); c.paste(im,(0,16)); ImageDraw.Draw(c).text((4,2),t,fill=(0,0,0)); return c
def rij(ims,gap=8):
    w=sum(i.width for i in ims)+gap*(len(ims)-1); h=max(i.height for i in ims)
    c=Image.new('RGB',(w,h),(200,200,200)); x=0
    for i in ims: c.paste(i,(x,0)); x+=i.width+gap
    return c
r1=rij([label(spr('lombre_gaucho_A.png',8),'r1 variant A (8x)'),label(model_op_schaal(8),'model r1 (zelfde schaal)'),label(spr('kaal.png',8),'kale reductie (8x)')])
box=(12,18,42,38); z=12
kz=lambda im: im.crop(tuple(v*z for v in box))
r2=rij([label(kz(spr('lombre_gaucho_A.png',z)),'kop A (12x)'),label(kz(model_op_schaal(z)),'kop model (12x)'),
        label(gen3(LOM,z,spiegel=True).crop((19*z,14*z,49*z,34*z)),'Gen 3-Lombre gespiegeld (12x)')])
een=[]
for bg in (W,D):
    c=Image.new('RGB',(5*64,64),bg)
    for i,p in enumerate(['lombre_gaucho_A.png','lombre_gaucho_B.png','lombre_gaucho_C.png']):
        c.paste(Image.fromarray(rgb(np.array(Image.open(p)),bg)),(i*64,0))
    c.paste(gen3(LOM,1,bg),(192,0)); c.paste(Image.fromarray(rgb(np.array(Image.open(LOT)),bg)) if False else gen3(LOT,1,bg),(256,0))
    een.append(c)
r3=label(rij(een),'1x: A | B | C | Gen 3-Lombre | gaucho-Lotad, op wit en donker')
box2=(10,16,44,40); z=8
r4=rij([label(spr('lombre_gaucho_%s.png'%v,z).crop(tuple(q*z for q in box2)),'mond %s (8x)'%v) for v in 'ABC'])
rs=(r1,r2,r3,r4); H=sum(r.height for r in rs)+16*len(rs); Wd=max(r.width for r in rs)
v=Image.new('RGB',(Wd,H),(200,200,200)); y=0
for r in rs: v.paste(r,(0,y)); y+=r.height+16
v.save('vel.png'); print(v.size)
