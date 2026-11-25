import os
from PIL import Image, ImageDraw
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(D,'../../../../../..')
L=lambda p: Image.open(p).convert('RGBA').crop((0,0,64,64))
items=[('r10 (met hooglicht)',L(os.path.join(D,'r10_met_hooglicht.png'))),('r10 zonder hooglicht',L(os.path.join(D,'r10_zonder_hooglicht.png'))),('r9',L(os.path.join(D,'../r9/capykart.png'))),
 ('Porygon (Gen 3)',L(os.path.join(R,'graphics/pokemon/porygon/anim_front_gba.png'))),('Capybarrel af',L(os.path.join(D,'../../../capybarrel/af/capybarrel.png')))]
S=8; cw=64*S+12; V=Image.new('RGBA',(cw*len(items),64*S+130),(255,255,255,255)); d=ImageDraw.Draw(V)
for i,(n,im) in enumerate(items):
    V.alpha_composite(im.resize((64*S,64*S),Image.NEAREST),(i*cw,20)); d.text((i*cw+4,4),n,fill=(0,0,0))
    for j,bg in enumerate([(255,255,255,255),(40,40,48,255),(96,120,168,255)]):
        b=Image.new('RGBA',(72,72),bg); b.alpha_composite(im,(4,4)); V.alpha_composite(b,(i*cw+j*80,64*S+40))
V.save(os.path.join(D,'vel.png'))
