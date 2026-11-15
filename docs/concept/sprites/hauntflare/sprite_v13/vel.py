# vel: v13 | v12 op 8x; close-ups kuif/staart/handen 12x naast Gen 3-vlammen (Typhlosion, Ponyta); 1x op licht en donker
from PIL import Image, ImageDraw; import numpy as np
D='docs/concept/sprites/hauntflare/'
def rgba(p,box=None,bg=(255,255,255)):
    im=Image.open(p); a=np.array(im); c=np.array(im.convert('RGBA')); c[a==0]=bg+(255,)
    o=Image.fromarray(c).convert('RGB'); return o.crop(box) if box else o
v13=D+'sprite_v13/hauntflare_v13.png'; v12=D+'sprite_v12/hauntflare_v12.png'
z=lambda im,k: im.resize((im.width*k,im.height*k),Image.NEAREST)
W=Image.new('RGB',(1060,1220),(230,230,230)); d=ImageDraw.Draw(W)
W.paste(z(rgba(v13),8),(10,20)); W.paste(z(rgba(v12),8),(538,20)); d.text((10,5),'v13',fill=0); d.text((538,5),'v12',fill=0)
y=550; x=10
for nm,box in [('kuif',(30,8,58,30)),('staart',(34,40,58,58)),('hand L',(8,47,29,63)),('hand R',(50,36,63,47))]:
    c=z(rgba(v13,box),12); W.paste(c,(x,y)); d.text((x,y-14),nm+' v13 12x',fill=0); x+=c.width+10
    if x>800: x=10; y+=290
y=1000
t=z(rgba('graphics/pokemon/typhlosion/anim_front.png',(16,0,48,26)),8); W.paste(t,(10,y)); d.text((10,y-14),'Typhlosion 8x',fill=0)
p=z(rgba('graphics/pokemon/charmeleon/anim_front.png',(48,8,64,30)),8); W.paste(p,(280,y)); d.text((280,y-14),'Charmeleon 8x',fill=0)
for i,bg in enumerate([(248,248,248),(40,40,48)]):
    W.paste(rgba(v13,bg=bg),(450+i*80,y)); W.paste(rgba(v12,bg=bg),(450+i*80,y+80))
d.text((450,y-14),'1x v13 (boven) / v12',fill=0)
W.save(D+'sprite_v13/vel.png')
