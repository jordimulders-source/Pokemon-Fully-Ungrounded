import os
from PIL import Image, ImageDraw
D=os.path.dirname(os.path.abspath(__file__))
L=lambda p: Image.open(os.path.join(D,p)).convert('RGBA').crop((0,0,64,64))
items=[('r12_creme',L('r12_creme.png')),('r12_wit',L('r12_wit.png')),('Capybarrel af',L('../../../capybarrel/af/capybarrel.png'))]
cw=524; V=Image.new('RGBA',(cw*3,520+400+110),(255,255,255,255)); d=ImageDraw.Draw(V)
for i,(n,im) in enumerate(items):
    V.alpha_composite(im.resize((512,512),Image.NEAREST),(i*cw,20)); d.text((i*cw+4,4),n,fill=(0,0,0))
box={'r12_creme':(13,9,44,38),'r12_wit':(13,9,44,38),'Capybarrel af':(5,18,36,47)}
for i,(n,im) in enumerate(items):
    c=im.crop(box[n]); V.alpha_composite(c.resize((c.width*12,c.height*12),Image.NEAREST),(i*cw,540))
y=540+31*12+10
for i,(n,im) in enumerate(items):
    for j,bg in enumerate([(255,255,255,255),(232,232,216,255),(40,40,48,255)]):
        b=Image.new('RGBA',(72,72),bg); b.alpha_composite(im,(4,4)); V.alpha_composite(b,(i*cw+j*80,y))
V.save(os.path.join(D,'vel.png'))
