# vel r4: (1) r4 | r3 | model op 8x; (2) r4 naast dodrio en fearow op 4x en 1x op licht/donker; (3) close-ups 12x kop, lijf, poten (r4 | model)
import numpy as np; from PIL import Image, ImageDraw
import modelover
R4='terreurvogel_bijl_r4.png'; R3='../sprite_bijl_r3/terreurvogel_bijl_r3.png'
def rgba(p):
    im=Image.open(p); a=np.array(im.convert('RGBA')); a[np.array(im)==0,3]=0; return Image.fromarray(a)
def gba(n):
    im=Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/%s/anim_front_gba.png'%n).crop((0,0,64,64))
    pal=[int(v) for l in open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/%s/normal_gba.pal'%n).read().split('\n')[3:19] for v in l.split()]
    im.putpalette(pal+[0]*(768-48)); a=np.array(im.convert('RGBA')); a[np.array(im)==0,3]=0; return Image.fromarray(a)
def op(im,s,bg=(255,255,255,255)):
    b=Image.new('RGBA',(64*s,64*s),bg); b.alpha_composite(im.resize((64*s,64*s),Image.NEAREST)); return b
vel=Image.new('RGBA',(1600,2100),(236,236,236,255)); d=ImageDraw.Draw(vel)
y=20
for i,(t,im) in enumerate([('r4 8x',op(rgba(R4),8)),('r3 8x',op(rgba(R3),8)),('model 8x',modelover.model_op(8).convert('RGBA'))]):
    x=10+i*522; vel.alpha_composite(im.crop((0,160,512,512)),(x,y)); d.text((x,y-14),t,fill=(0,0,0))
y=400
d.text((10,y-14),'4x: r4 | dodrio | fearow',fill=(0,0,0))
for i,im in enumerate([rgba(R4),gba('dodrio'),gba('fearow')]):
    vel.alpha_composite(op(im,4,(248,248,240,255)),(10+i*266,y))
y2=y+266
for j,(bg,nm) in enumerate([((248,248,240,255),'licht'),((40,44,52,255),'donker')]):
    d.text((10+j*260,y2),'1x %s: r4 | dodrio | fearow'%nm,fill=(0,0,0))
    for i,im in enumerate([rgba(R4),gba('dodrio'),gba('fearow')]):
        vel.alpha_composite(op(im,1,bg),(10+j*260+i*70,y2+14))
y=760
def close(b,z=12):
    x0,y0,x1,y1=b
    a=op(rgba(R4),z,(200,220,200,255)).crop((x0*z,y0*z,x1*z,y1*z)); m=modelover.model_op(z).convert('RGBA').crop((x0*z,y0*z,x1*z,y1*z))
    out=Image.new('RGBA',(a.width*2+8,a.height),(236,236,236,255)); out.paste(a,(0,0)); out.paste(m,(a.width+8,0)); return out
for t,b in [('kop 12x (r4 | model)',(0,22,30,44)),('lijf/vleugel/staart 12x',(24,28,64,51)),('poten 12x',(8,44,64,63))]:
    c=close(b); d.text((10,y-14),t,fill=(0,0,0)); vel.alpha_composite(c,(10,y)); y+=c.height+30
vel=vel.crop((0,0,1600,y)); vel.save('vel.png'); print(vel.size)
