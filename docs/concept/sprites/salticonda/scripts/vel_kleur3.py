"""Vel kleurronde 3: pre-evo, kleur1-E en kleur3 op 4x en 1x (licht en donker), koppen op 8x (pre-evo, Sandaconda, nieuw)."""
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'
D=R+'docs/concept/sprites/salticonda/'
ims=[Image.open(D+'../silicobra_uyuni/af/silicobra_uyuni.png').convert('RGBA'),
     Image.open(D+'kleur1/salticonda_E.png').convert('RGBA'),
     Image.open(D+'kleur3/salticonda.png').convert('RGBA')]
names=['Silicobra-Uyuni (af)','Salticonda kleur1-E','Salticonda kleur3']
sand=Image.open(R+'graphics/pokemon/sandaconda/anim_front.png').convert('RGBA').crop((0,0,64,64))
bgc=sand.getpixel((0,0)); sand.putdata([(0,0,0,0) if p==bgc else p for p in sand.getdata()])
LIGHT,DARK=(236,238,240,255),(44,48,56,255)
W=3*276+20; H=2*(256+10+70)+20+260+30
V=Image.new('RGBA',(W,H),(255,255,255,255)); d=ImageDraw.Draw(V)
y=0
for bg in (LIGHT,DARK):
    V.paste(bg,(0,y,W,y+256+80))
    for i,im in enumerate(ims):
        V.alpha_composite(im.resize((256,256),Image.NEAREST),(10+i*276,y+4))
        V.alpha_composite(im,(10+i*276+96,y+264))
        d.text((10+i*276,y+262),names[i],fill=(128,128,128,255))
    y+=256+80
y+=10
crops=[(ims[0],(10,12,48,44),'pre-evo kop 8x'),(sand,(0,10,30,42),'Sandaconda kop 8x'),(ims[2],(2,0,48,27),'Salticonda kleur3 kop 8x')]
x=0
V2=Image.new('RGBA',(sum((c[1][2]-c[1][0])*8+10 for c in crops),max((c[1][3]-c[1][1])*8 for c in crops)+16),LIGHT)
for im,b,t in crops:
    V2.alpha_composite(im.crop(b).resize(((b[2]-b[0])*8,(b[3]-b[1])*8),Image.NEAREST),(x,14)); ImageDraw.Draw(V2).text((x,1),t,fill=(90,90,90,255)); x+=(b[2]-b[0])*8+10
s=W/V2.width
if s<1: V2=V2.resize((W,int(V2.height*s)),Image.NEAREST)
V=V.crop((0,0,W,y+V2.height+4)); V.paste(LIGHT,(0,y,W,y+V2.height+4)); V.alpha_composite(V2,(0,y))
V.save(D+'kleur3/vel.png')
