"""Vel kleurronde 3b: pre-evo, kleur1-E, kleur3 en kleur3b op 4x en 1x (licht en donker);
koppen op 8x (pre-evo, Sandaconda, kleur3, kleur3b) en de kuif van kleur3b op 8x."""
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'
D=R+'docs/concept/sprites/salticonda/'
L=lambda p: Image.open(p).convert('RGBA')
ims=[L(D+'../silicobra_uyuni/af/silicobra_uyuni.png'),L(D+'kleur1/salticonda_E.png'),L(D+'kleur3/salticonda.png'),L(D+'kleur3b/salticonda.png')]
names=['Silicobra-Uyuni (af)','kleur1-E','kleur3','kleur3b']
sand=L(R+'graphics/pokemon/sandaconda/anim_front.png').crop((0,0,64,64))
bgc=sand.getpixel((0,0)); sand.putdata([(0,0,0,0) if p==bgc else p for p in list(sand.getdata())])
LIGHT,DARK=(236,238,240,255),(44,48,56,255)
W=4*266+10
parts=[]
for bg in (LIGHT,DARK):
    P=Image.new('RGBA',(W,346),bg); d=ImageDraw.Draw(P)
    for i,im in enumerate(ims):
        P.alpha_composite(im.resize((256,256),Image.NEAREST),(5+i*266,4)); P.alpha_composite(im,(5+i*266+96,276))
        d.text((5+i*266,262),names[i],fill=(128,128,128,255))
    parts.append(P)
crops=[(ims[0],(10,12,48,44),'pre-evo'),(sand,(0,10,30,42),'Sandaconda'),(ims[2],(2,0,48,27),'kleur3'),(ims[3],(2,0,48,27),'kleur3b')]
row=Image.new('RGBA',(sum((b[2]-b[0])*8+10 for _,b,_ in crops),32*8+16),LIGHT); x=0
for im,b,t in crops:
    row.alpha_composite(im.crop(b).resize(((b[2]-b[0])*8,(b[3]-b[1])*8),Image.NEAREST),(x,14)); ImageDraw.Draw(row).text((x,1),t+' kop 8x',fill=(90,90,90,255)); x+=(b[2]-b[0])*8+10
row=row.resize((W,int(row.height*W/row.width)),Image.NEAREST)
k=ims[3].crop((14,0,47,21)).resize((33*8,21*8),Image.NEAREST)
kr=Image.new('RGBA',(W,21*8+20),LIGHT); kr.alpha_composite(k,(5,16)); ImageDraw.Draw(kr).text((5,2),'kleur3b kuif 8x',fill=(90,90,90,255))
k3=ims[2].crop((14,0,47,21)).resize((33*8,21*8),Image.NEAREST); kr.alpha_composite(k3,(5+33*8+20,16)); ImageDraw.Draw(kr).text((5+33*8+20,2),'kleur3 kuif 8x',fill=(90,90,90,255))
H=sum(p.height for p in parts)+row.height+kr.height
V=Image.new('RGBA',(W,H),LIGHT); y=0
for p in parts+[row,kr]: V.alpha_composite(p,(0,y)); y+=p.height
V.save(D+'kleur3b/vel.png')
