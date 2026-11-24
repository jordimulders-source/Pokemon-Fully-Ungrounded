import os
from PIL import Image, ImageDraw
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(D,'../../../../../..')
def L(p): return Image.open(p).convert('RGBA').crop((0,0,64,64))
items=[('r8',L(os.path.join(D,'capykart.png'))),('r7',L(os.path.join(D,'../../eindkeuring/capykart_r7.png')))]
for n in ['sudowoodo','porygon','linoone']:
    items.append((n+' (Gen 3)',L(os.path.join(R,f'graphics/pokemon/{n}/anim_front_gba.png'))))
S=6; cw=64*S+12
W=Image.new('RGBA',(cw*len(items),64*S+30+150),(255,255,255,255)); d=ImageDraw.Draw(W)
for i,(n,im) in enumerate(items):
    W.alpha_composite(im.resize((64*S,64*S),Image.NEAREST),(i*cw,20)); d.text((i*cw+4,4),n,fill=(0,0,0))
y=64*S+40
for j,bg in enumerate([(255,255,255,255),(232,232,216,255),(40,40,48,255),(96,120,168,255)]):
    for k,(n,im) in enumerate(items[:2]):
        b=Image.new('RGBA',(80,80),bg); b.alpha_composite(im,(8,8))
        W.alpha_composite(b.resize((80*1,80*1)),(j*200+k*90,y))
        b2=Image.new('RGBA',(80,80),bg); b2.alpha_composite(im,(8,8))
d.text((4,y+85),'1x op licht/donker: per achtergrond links r8, rechts r7',fill=(0,0,0))
W.save(os.path.join(D,'vel.png'))
