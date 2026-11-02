# Vergelijkingsvel: nachtaap ronde 3 + fase 1 + echte sprites, 1x en 3x, licht en donker
import os
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'
D=R+'docs/concept/sprites/nachtaap_evo/'
def pal(p):
    L=open(p).read().split('\n')[3:19]
    return [tuple(map(int,l.split())) for l in L]
def load(png, palf=None):
    im=Image.open(png)
    if im.size[1]>64: im=im.crop((0,0,64,64))
    if palf and im.mode=='P':
        p=pal(palf); flat=[c for t in p for c in t]; im.putpalette(flat+[0]*(768-len(flat)))
        im.info['transparency']=0
    return im.convert('RGBA') if 'transparency' in im.info or im.mode=='RGBA' else im.convert('RGBA')
items=[('nachtaap r3',load(D+'kleur/ronde3/nachtaap.png',D+'kleur/ronde3/normal.pal')),
       ('nachtaap r4',load(D+'kleur/ronde4/nachtaap.png',D+'kleur/ronde4/normal.pal')),
       ('fase 1',load(D+'referenties/fase1_goedgekeurd.png'))]
for n in ['lairon','sableye','misdreavus','mismagius','aipom','ambipom','grumpig','zigzagoon','spinda','kecleon','natu','abra','mightyena','slakoth','espeon']:
    g=R+'graphics/pokemon/'+n+'/'
    items.append((n,load(g+'anim_front.png',g+'normal.pal')))
for name,im in items:
    a=im.split()[3]; print(name, sum(1 for v in a.getdata() if v>0),'px')
S=3; cell=64*S+8
cols=6; rows=(len(items)+cols-1)//cols
W=cols*cell; H=rows*(cell+64+30)*2
sheet=Image.new('RGBA',(W,H),(255,255,255,255)); d=ImageDraw.Draw(sheet)
y0=0
for bg in [(235,235,235,255),(36,36,44,255)]:
    for i,(name,im) in enumerate(items):
        cx=(i%cols)*cell; cy=y0+(i//cols)*(cell+64+30)
        blk=Image.new('RGBA',(cell,cell+64+30),bg)
        b=Image.new('RGBA',(64,64),bg); b.alpha_composite(im)
        blk.paste(b.resize((64*S,64*S),Image.NEAREST),(4,4))
        blk.paste(b,(4,64*S+10))
        sheet.paste(blk,(cx,cy))
        ImageDraw.Draw(sheet).text((cx+76,cy+64*S+30),name,fill=(255,0,0,255))
    y0+=rows*(cell+64+30)
sheet.save(D+'kleur/ronde3/keuring_vgl.png')
