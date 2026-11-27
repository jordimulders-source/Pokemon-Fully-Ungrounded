# Vel r14: r14 | r13 op 8x, close-ups (kop, manen, hoorns) r14 vs r13 op 12x, 1x en 2x op licht en donker naast impala,
# skinguin, viscacha, plus palet. Gebruik: python3 vel14.py -> r14/vel.png
from PIL import Image, ImageDraw
SP='../../../'
r14=Image.open('r14/kudu_r14.png').convert('RGBA'); r13=Image.open('r13/kudu_r13.png').convert('RGBA')
imp=Image.open('../../impala/af/impala.png').convert('RGBA')
sk=Image.open(SP+'skinguin/af/skinguin.png').convert('RGBA').crop((0,0,64,64))
vi=Image.open(SP+'viscacha/af/viscacha.png').convert('RGBA').crop((0,0,64,64))
BG=(196,206,218,255); V=Image.new("RGBA",(1100,1800),BG); d=ImageDraw.Draw(V)
def plak(im,x,y,s,bg=None):
    if bg: V.paste(Image.new('RGBA',(im.width*s,im.height*s),bg),(x,y))
    V.alpha_composite(im.resize((im.width*s,im.height*s),Image.NEAREST),(x,y))
d.text((10,4),'r14 (eindkeuring)',fill=(0,0,0,255)); d.text((560,4),'r13',fill=(0,0,0,255))
plak(r14,10,18,8); plak(r13,560,18,8)
y=550
for naam,box in [('kop',(4,14,30,32)),('manen',(13,22,40,44)),('hoorns',(9,0,38,20))]:
    a=r14.crop(box); b=r13.crop(box); s=12 if naam!='manen' else 10
    d.text((10,y),naam+': r14 | r13',fill=(0,0,0,255)); plak(a,10,y+14,s); plak(b,30+a.width*s,y+14,s); y+=a.height*s+24
y+=4; d.text((10,y),'1x en 2x op licht en donker: r14, impala, skinguin, viscacha',fill=(0,0,0,255)); y+=14
for bg in [(248,248,248,255),(40,44,52,255)]:
    x=10
    for im in [r14,imp,sk,vi]: plak(im,x,y,1,bg); x+=70
    x=300
    for im in [r14,imp,sk,vi]: plak(im,x,y,2,bg); x+=134
    y+=134
pal=Image.open('r14/kudu_r14.png').getpalette()[:48]
for i in range(16):
    d.rectangle((10+i*40,y,48+i*40,y+30),fill=tuple(pal[i*3:i*3+3])); d.text((12+i*40,y+32),str(i),fill=(0,0,0,255))
V=V.crop((0,0,1100,y+50)); V.save('r14/vel.png'); print(V.size)
