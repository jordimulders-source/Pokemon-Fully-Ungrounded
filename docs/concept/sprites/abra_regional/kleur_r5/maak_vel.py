# maak_vel.py (vanuit kleur_r5/): vel.png (r5 8x | r4 8x | model zelfde schaal | 1x/2x licht/donker/groen)
# en closeup.png (per onderdeel r4 | r5 | model op 12x; oog ook variant B)
from PIL import Image, ImageDraw
S='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/e768f5de-0252-58bb-8bc9-76aca5f6423c/scratchpad/'
def rgba(p):
    im=Image.open(p); im.save(S+'_v.png',transparency=0); return Image.open(S+'_v.png').convert('RGBA')
def op(img,kl):
    b=Image.new('RGBA',img.size,kl); b.alpha_composite(img); return b.convert('RGB')
r5=rgba('abra_r5.png'); r4=rgba('../kleur_r4/abra_r4.png'); rB=rgba('abra_r5_oogB.png')
nat=Image.open('../kleur_r1/natief.png').convert('RGB')
mod=Image.new('RGB',(128,128),'white'); mod.paste(nat,(1,14))
W=(255,255,255,255)
klein=Image.new('RGB',(512,512),(200,200,200))
for k,kl in enumerate([(248,248,248,255),(40,40,48,255),(144,200,144,255)]):
    klein.paste(op(r5,kl),(16+k*80,16)); klein.paste(op(r5,kl).resize((128,128),Image.NEAREST),(16+k*164,120))
v=Image.new('RGB',(4*532,560),'white'); d=ImageDraw.Draw(v)
for k,(x,t) in enumerate(((op(r5,W).resize((512,512),Image.NEAREST),'r5 8x (oog A)'),(op(r4,W).resize((512,512),Image.NEAREST),'r4 8x'),
                          (mod.resize((512,512),Image.NEAREST),'model (natief raster), zelfde schaal'),(klein,'r5 1x en 2x op licht/donker/groen'))):
    v.paste(x,(k*532,40)); d.text((k*532+8,12),t,fill=(0,0,0))
v.save('vel.png')
Z=12
def crop(img,box,model=False):
    x0,y0,x1,y1=box
    if model: return mod.crop((2*x0,2*y0,2*x1,2*y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
    return op(img,W).crop(box).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
DELEN=[('linkeroog: r4 | A (in r5) | B | model',(18,26,30,34),[r4,r5,rB,None]),
       ('rechteroor: r4 | r5 | model',(26,13,38,24),[r4,r5,None]),
       ('kop: r4 | r5 | model',(16,15,46,38),[r4,r5,None]),
       ('linkerarm: r4 | r5 | model',(17,36,32,52),[r4,r5,None]),
       ('staart rechts: r4 | r5 | model',(38,43,57,63),[r4,r5,None])]
rijen=[]
for t,box,imgs in DELEN:
    ps=[crop(i,box,i is None) for i in imgs]
    w=sum(p.width for p in ps)+10*(len(ps)-1); h=ps[0].height+22
    r=Image.new('RGB',(w,h),'white'); dd=ImageDraw.Draw(r); dd.text((4,4),t,fill=(0,0,0)); x=0
    for p in ps:
        r.paste(p,(x,22)); x+=p.width+10
    rijen.append(r)
c=Image.new('RGB',(max(r.width for r in rijen),sum(r.height+12 for r in rijen)),'white'); y=0
for r in rijen: c.paste(r,(0,y)); y+=r.height+12
c.save('closeup.png'); print('ok',c.size)
