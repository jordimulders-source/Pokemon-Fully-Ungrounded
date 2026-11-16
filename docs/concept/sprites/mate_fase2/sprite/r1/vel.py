# vel.png: sprite 8x | model (natief, zelfde schaal) 8x; close-ups 12x sprite vs geschrapt model; 1x licht/donker
import sys; from PIL import Image, ImageDraw; import numpy as np
D='docs/concept/sprites/mate_fase2/sprite/'; R=sys.argv[1] if len(sys.argv)>1 else 'r1'
def rgba(p):
    im=Image.open(p); 
    if im.mode=='P': im=im.convert('RGBA')
    return im
sp=rgba(D+R+'/mate2.png'); 
nat=Image.open(D+'r1/natief.png').convert('RGB').crop((5,16,95,80))   # model natief rond het dier
ges=Image.open(D+'r1/geschrapt.png').convert('RGB')
H=ges.height; oy=64-H-1; ox=(64-ges.width)//2
def on(im,c):
    b=Image.new('RGBA',im.size,c+(255,)); b.alpha_composite(im.convert('RGBA')); return b.convert('RGB')
def up(im,s): return im.resize((im.width*s,im.height*s),Image.NEAREST)
spl=on(sp,(235,240,235))
V=Image.new('RGB',(1500,1700),(255,255,255)); d=ImageDraw.Draw(V)
V.paste(up(spl,8),(10,30)); d.text((10,10),R+' sprite 8x (64x64)',fill=0)
V.paste(up(nat,8),(540,30)); d.text((540,10),'model natief raster 8x (zelfde schaal, ongeschrapt)',fill=0)
# close-ups: (naam, x0,y0,x1,y1 in geschrapt-coordinaten)
cl=[('gezicht ventje',30,2,50,18),('ogen kano',0,22,16,38),('verre bombilla',19,1,34,21),('nabije bombilla',33,16,61,44)]
x=10; y=560
for n,x0,y0,x1,y1 in cl:
    s=12 if (x1-x0)<20 else 8
    a=up(spl.crop((x0+ox,y0+oy,x1+ox,y1+oy)),s); b=up(ges.crop((x0,y0,x1,y1)),s)
    if x+a.width*2+30>1500: x=10; y+=330
    d.text((x,y-15),n+' (sprite | model) %dx'%s,fill=0)
    V.paste(a,(x,y)); V.paste(b,(x+a.width+6,y)); x+=a.width*2+30
y2=y+300
for i,c in enumerate([(255,255,255),(200,230,200),(40,40,48)]):
    V.paste(on(sp,c),(10+i*80,y2)); 
V.paste(on(sp,(248,248,248)).resize((128,128),Image.NEAREST),(260,y2)); V.paste(nat,(400,y2))
d.text((10,y2-15),'1x licht/groen/donker, 2x, model natief 1x',fill=0)
V.crop((0,0,1500,y2+150)).save(D+R+'/vel.png')
