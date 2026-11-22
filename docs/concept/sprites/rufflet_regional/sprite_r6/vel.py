from PIL import Image, ImageDraw
names=['rufflet_r5V3','rufflet_r6']; S=12
def kop(n):
    im=Image.open(n+'.png').convert('RGBA'); t=Image.new('RGB',(64,64),(255,255,255)); t.paste(im,(0,0),im)
    return t.crop((14,12,40,36)).resize((26*S,24*S),Image.NEAREST)
R=Image.open('../referenties/rufflet_anim_front.png').convert('RGB').crop((14,6,40,30)).resize((26*S,24*S),Image.NEAREST)
V=Image.new('RGB',(2*528+3*330+40,30+512+330),(255,255,255)); d=ImageDraw.Draw(V)
for i,n in enumerate(names): V.paste(Image.open(n+'_8x.png'),(16+i*528,30)); d.text((16+i*528,10),n+' 8x',fill=(0,0,0))
x=16+2*528
for l,im in [('r5V3 kop 12x',kop(names[0])),('r6 kop 12x',kop(names[1])),('Rufflet kop 12x',R)]: V.paste(im,(x,30)); d.text((x,10),l,fill=(0,0,0)); x+=330
for i,n in enumerate(names):
    s=Image.open(n+'.png').convert('RGBA')
    for j,bg in enumerate([(232,232,232),(40,44,56)]):
        t=Image.new('RGB',(64,64),bg); t.paste(s,(0,0),s); V.paste(t,(16+2*528+i*160+j*72,360))
V.save('vel.png')
