# r4/vel.png: r4 8x | r3 8x | model natief 8x; close-ups 12x (sprite | geschrapt model); 1x licht/groen/donker + 2x
from PIL import Image, ImageDraw
D='docs/concept/sprites/mate_fase2/sprite/'
def on(im,c):
    b=Image.new('RGBA',im.size,c+(255,)); b.alpha_composite(im.convert('RGBA')); return b.convert('RGB')
def up(im,s): return im.resize((im.width*s,im.height*s),Image.NEAREST)
r4=Image.open(D+'r4/mate2.png').convert('RGBA'); r3=Image.open(D+'r3/mate2.png').convert('RGBA')
nat=Image.open(D+'r1/natief.png').convert('RGB').crop((9,25,87,79)); ges=Image.open(D+'r4/geschrapt.png').convert('RGB')
L=on(r4,(235,240,235)); oy=15
V=Image.new('RGB',(1720,1500),(255,255,255)); d=ImageDraw.Draw(V)
V.paste(up(L,8),(10,30)); d.text((10,12),'r4 8x (64x64)',fill=0)
V.paste(up(on(r3,(235,240,235)),8),(540,30)); d.text((540,12),'r3 8x (vorige)',fill=0)
V.paste(up(nat,8),(1070,30)); d.text((1070,12),'model natief 8x (ongeschrapt)',fill=0)
cl=[('punt, beide kano-ogen, neusgat',0,24,22,44,12),('gezicht ventje',33,2,52,19,12),('verre bombilla',21,1,36,22,12),('waterval',48,10,64,30,12),('nabije bombilla + zeefje',36,17,62,48,8)]
x=10; y=600
for n,x0,y0,x1,y1,s in cl:
    a=up(L.crop((x0,y0+oy,x1,y1+oy)),s); b=up(ges.crop((x0,y0,x1,y1)),s)
    if x+a.width*2+30>1720: x=10; y+=290
    d.text((x,y-15),n+' (sprite | model) %dx'%s,fill=0); V.paste(a,(x,y)); V.paste(b,(x+a.width+6,y)); x+=a.width*2+30
y2=y+270
for i,c in enumerate([(255,255,255),(200,230,200),(40,40,48)]): V.paste(on(r4,c),(10+i*80,y2))
V.paste(up(on(r4,(248,248,248)),2),(260,y2)); V.paste(on(r3,(255,255,255)),(410,y2)); V.paste(nat,(490,y2))
d.text((10,y2-15),'1x licht/groen/donker | 2x | r3 1x | model 1x',fill=0)
V.crop((0,0,1720,y2+140)).save(D+'r4/vel.png')
