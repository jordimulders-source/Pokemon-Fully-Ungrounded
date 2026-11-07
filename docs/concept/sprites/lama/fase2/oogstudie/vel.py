# Bouwt oogstudie.png: hele sprite op 2x + oog-uitsnede op 10x met raster.
# Alleen uitsneden en een vel; er wordt niets getekend aan de sprites zelf.
# Draaien vanuit de repo-root: python3 docs/concept/sprites/lama/fase2/oogstudie/vel.py
from PIL import Image, ImageDraw
D='docs/concept/sprites/lama/fase2/oogstudie/'
L='docs/concept/sprites/lama/fase2/'
VOORBEELDEN=[  # naam, uitsnede (x0,y0,x1,y1), korte typering
 ('camerupt',(13,35,24,44),'1 zwaar lid, wit onder'),
 ('farfetchd',(21,20,31,29),'2 plat zwart lid'),
 ('numel',(20,22,30,32),'3 bruin oog, streepglans'),
 ('slowpoke',(20,27,31,38),'4 leeg: mini-pupil'),
 ('lapras',(14,10,24,19),'5 lange hals, bruin'),
 ('tropius',(6,6,16,15),'6 lange hals, blad-lid'),
 ('girafarig',(15,10,25,19),'7 viervoeter, lid-hoek'),
 ('rapidash',(8,13,18,22),'8 paard, bruine lidlijn'),
]
LAMA=[(L+'kleur/ronde3/lama.png',(14,10,24,19),'lama ronde3 (nu)'),
      (L+'silhouet/variant_jonger2/proef_lama.png',(13,11,23,20),'lama jonger2 (nu)')]
def mon(n):
    im=Image.open(f'graphics/pokemon/{n}/anim_front.png')
    pal=[]
    for l in open(f'graphics/pokemon/{n}/normal.pal').read().split('\n')[3:19]:
        pal+=[int(x) for x in l.split()]
    im=im.convert('P'); im.putpalette(pal)
    return im.crop((0,0,64,64)).convert('RGB')
def zoom(im,box,s=10):
    x0,y0,x1,y1=box
    z=im.crop(box).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST); d=ImageDraw.Draw(z)
    for i in range(x1-x0+1): d.line([(i*s,0),(i*s,z.height)],fill=(110,110,110))
    for j in range(y1-y0+1): d.line([(0,j*s),(z.width,j*s)],fill=(110,110,110))
    return z
def kader(im,box,s=2):
    im=im.resize((128,128),Image.NEAREST); d=ImageDraw.Draw(im)
    x0,y0,x1,y1=box; d.rectangle([x0*s-1,y0*s-1,x1*s,y1*s],outline=(255,0,0))
    return im
CW=140; RH=128+14+120+20
W=CW*5+10; H=RH*2+150
vel=Image.new('RGB',(W,H),(250,250,245)); d=ImageDraw.Draw(vel)
items=[(mon(n),b,t) for n,b,t in VOORBEELDEN]+[(Image.open(p).convert('RGB'),b,t) for p,b,t in LAMA]
for i,(im,b,t) in enumerate(items):
    r,c=divmod(i,5); x=5+c*CW; y=5+r*RH
    d.text((x,y),t,fill=(0,0,0))
    vel.paste(kader(im,b),(x,y+12))
    vel.paste(zoom(im,b),(x,y+12+132))
# Rij 3: de twee recepten uit OOGSTUDIE.md als raster (lamapalet uit kleur/ronde3), op 10x, 3x en 1x.
LP={'1':(0x2a,0x16,0x1a),'2':(0x6c,0x3a,0x20),'3':(0xa8,0x68,0x3a),'4':(0xd6,0x9a,0x52),
    '5':(0xef,0xc2,0x7a),'6':(0xf8,0xe2,0xa8),'a':(0x4a,0x3c,0x40),'f':(0xfa,0xf6,0xec)}
RECEPT={'A zwaar lid':['5555551','5444415','5111115','52a1124','56aa245','5533455'],
        'B leeg bruin':['5555515','5111112','5221124','5422235','5533355','5555555']}
for k,(t,rows) in enumerate(RECEPT.items()):
    im=Image.new('RGB',(7,6))
    for y,r in enumerate(rows):
        for x,ch in enumerate(r): im.putpixel((x,y),LP[ch])
    x=5+k*(CW*2+20); y=5+2*RH
    d.text((x,y),'recept '+t+' (10x, 3x, 1x)',fill=(0,0,0))
    vel.paste(zoom(im,(0,0,7,6)),(x,y+14))
    vel.paste(im.resize((21,18),Image.NEAREST),(x+80,y+14))
    vel.paste(im,(x+110,y+14))
d.text((5,H-14),'rood kader = uitsnede; uitsnede op 10x met pixelraster. Lama kijkt naar links.',fill=(0,0,0))
vel.save(D+'oogstudie.png')
