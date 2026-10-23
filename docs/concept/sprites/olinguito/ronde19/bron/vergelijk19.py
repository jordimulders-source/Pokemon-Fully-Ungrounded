"""Maakt ../studie.png (7 referenties + ronde 18/19, 3x, met kopkader en maten) en ../compare.png
(ronde 18 | ronde 19 | Poochyena | Cyndaquil, 1x en 3x, plus koppen op 6x)."""
from PIL import Image, ImageDraw
G='/home/user/projectgrounded/graphics/pokemon/%s/anim_front.png'
def laad(p, f=0):
    a=Image.open(p); px=a.load(); rgb=a.convert('RGB')
    o=Image.new('RGB',(64,64),(255,255,255))
    for y in range(64):
        for x in range(64):
            if px[x,y+64*f]: o.putpixel((x,y),rgb.getpixel((x,y+64*f)))
    return o
def opp(im): return sum(1 for y in range(64) for x in range(64) if im.getpixel((x,y))!=(255,255,255))
# kopkaders (met de hand bepaald, frame 1): x0,y0,x1,y1 -- kop = alles binnen het kader
KOP={'poochyena':(10,13,33,35),'cyndaquil':(14,21,31,41),'r18':(9,19,39,39),'r19':(13,21,37,38)}
NOT={'poochyena':'1 oog; neus x10, oog x17-20 (7 px achter de neus), oor erboven',
     'cyndaquil':'1 oog (spleet) x23-28; snuit spits, 9 px voor het oog',
     'typhlosion':'1 oog; snuit wijst schuin weg, verre oog achter de snuit',
     'dragonair':'1 oog; kop klein t.o.v. lijf',
     'kabutops':'1 oog in beeld, kop half van opzij',
     'rhyhorn':'1 oog; lange snuit + hoorn',
     'rhydon':'1 oog; snuit 3/4, verre oog weg'}
items=[(n,laad(G%n)) for n in NOT]+[('r18',laad('../../ronde18/anim_front.png')),('r19',laad('../anim_front.png'))]
W=Image.new('RGB',(5*200,2*250),(255,255,255)); d=ImageDraw.Draw(W)
for i,(n,im) in enumerate(items):
    X,Y=(i%5)*200,(i//5)*250
    W.paste(im.resize((192,192),Image.NEAREST),(X,Y))
    t='%s  %d px'%(n,opp(im))
    if n in KOP:
        x0,y0,x1,y1=KOP[n]; d.rectangle((X+x0*3,Y+y0*3,X+x1*3+2,Y+y1*3+2),outline=(220,0,0))
        k=sum(1 for y in range(y0,y1+1) for x in range(x0,x1+1) if im.getpixel((x,y))!=(255,255,255))
        t+='  kop %d (%d%%)'%(k,round(100*k/opp(im)))
    d.text((X+2,Y+196),t,fill=(0,0,0))
    if n in NOT: d.text((X+2,Y+210),NOT[n][:34],fill=(80,80,80)); d.text((X+2,Y+222),NOT[n][34:],fill=(80,80,80))
W.save('../studie.png')
# compare
r18=[laad('../../ronde18/anim_front.png',f) for f in (0,1)]; r19=[laad('../anim_front.png',f) for f in (0,1)]
ims=[r18[0],r19[0],laad(G%'poochyena'),laad(G%'cyndaquil')]
C=Image.new('RGB',(4*196+4*68+10,192+30+150),(255,255,255)); d=ImageDraw.Draw(C)
x=0
for im,n in zip(ims,['ronde 18','ronde 19','Poochyena','Cyndaquil']):
    C.paste(im,(x,60)); d.text((x,130),n,fill=(0,0,0)); x+=68
x+=10
for im in ims: C.paste(im.resize((192,192),Image.NEAREST),(x,0)); x+=196
x=0
for im,b in [(r18[0],(6,16,42,41)),(r19[0],(6,16,42,41)),(r19[1],(6,15,42,40)),(ims[2],(6,10,42,35))]:
    c=im.crop(b).resize(((b[2]-b[0])*4,(b[3]-b[1])*4),Image.NEAREST); C.paste(c,(x,212)); x+=c.width+8
d.text((4,198),'koppen 4x: ronde 18 | ronde 19 frame 1 | ronde 19 frame 2 | Poochyena',fill=(0,0,0))
C.save('../compare.png')
