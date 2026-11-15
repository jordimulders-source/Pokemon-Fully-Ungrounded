"""vel.png: per rij gezicht 12x | hele sprite 6x | 1x. Rijen: v7, kandidaten, Haunter Gen 3."""
from PIL import Image, ImageDraw
import os
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'..','..','..','..','..')
def rgba(p):
    im=Image.open(p)
    if im.mode=='P':
        im=im.crop((0,0,64,64)); im.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/931d0048-d45a-55a4-a2ad-8ad05568e8ad/scratchpad/t.png',transparency=0)
        im=Image.open('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/931d0048-d45a-55a4-a2ad-8ad05568e8ad/scratchpad/t.png')
    return im.convert('RGBA')
rijen=[('v7',os.path.join(H,'..','sprite_v7','hauntflare_v7.png'),(14,22,40,42))]
for k in 'IJK': rijen.append((k,os.path.join(H,f'kandidaat_{k}.png'),(14,22,40,42)))
rijen.append(('Haunter G3',os.path.join(R,'graphics','pokemon','haunter','anim_front.png'),(8,28,38,48)))
BG=(200,200,210,255); rh=20*12
W=30*12+64*6+64+60; vel=Image.new('RGBA',(W,len(rijen)*(rh+24)),BG); d=ImageDraw.Draw(vel)
for i,(n,p,box) in enumerate(rijen):
    im=rgba(p); y=i*(rh+24)
    d.text((4,y+2),n,fill=(0,0,0,255)); y+=14
    f=im.crop(box); f=f.resize((f.width*12,f.height*12),Image.NEAREST)
    vel.paste(f,(0,y),f)
    g=im.resize((384,384),Image.NEAREST).crop((0,64,384,64+rh)); vel.paste(g,(30*12+20,y),g)
    vel.paste(im,(30*12+20+384+20,y+60),im)
vel.save(os.path.join(H,'vel.png'))
