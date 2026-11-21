import numpy as np; from PIL import Image, ImageDraw
names=['../sprite_r4/rufflet_r4A','rufflet_r5V1','rufflet_r5V2','rufflet_r5V3']; lab=['r4A','V1','V2','V3']
big=[Image.open(n+'_8x.png') for n in names]
def kop(n,S=12):
    im=Image.open(n+'.png').convert('RGBA'); t=Image.new('RGB',(64,64),(255,255,255)); t.paste(im,(0,0),im)
    return t.crop((14,12,40,36)).resize((26*S,24*S),Image.NEAREST)
R=Image.open('../referenties/rufflet_anim_front.png').convert('RGB').crop((14,6,40,30)).resize((26*12,24*12),Image.NEAREST)
V=Image.new('RGB',(4*528+16,30+512+30+300+30+90),(255,255,255)); d=ImageDraw.Draw(V)
for i,(b,l) in enumerate(zip(big,lab)): V.paste(b,(16+i*528,30)); d.text((16+i*528,10),l+' 8x',fill=(0,0,0))
y=30+512+30
for i,(n,l) in enumerate(zip(names,lab)): V.paste(kop(n),(16+i*340,y)); d.text((16+i*340,y-14),l+' kop 12x',fill=(0,0,0))
V.paste(R,(16+4*340,y)); d.text((16+4*340,y-14),'Rufflet kop 12x',fill=(0,0,0))
y+=300+20
for i,n in enumerate(names):
    s=Image.open(n+'.png').convert('RGBA')
    for j,bg in enumerate([(232,232,232),(40,44,56)]):
        t=Image.new('RGB',(64,64),bg); t.paste(s,(0,0),s); V.paste(t,(16+i*160+j*72,y))
V.save('vel.png'); print(V.size)
