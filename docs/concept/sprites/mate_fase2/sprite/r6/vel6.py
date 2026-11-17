# r6/vel.png: zacht | sterk | r5 B | model (8x); close-up rechterrand 12x (zacht | sterk | r5B | model); 1x licht/donker
from PIL import Image, ImageDraw
D='docs/concept/sprites/mate_fase2/sprite/'
def on(im,c):
    b=Image.new('RGBA',im.size,c+(255,)); b.alpha_composite(im.convert('RGBA')); return b.convert('RGB')
def up(im,s): return im.resize((im.width*s,im.height*s),Image.NEAREST)
sp={k:Image.open(D+p).convert('RGBA') for k,p in [('r6 zacht','r6/mate2_zacht.png'),('r6 sterk','r6/mate2_sterk.png'),('r5 B','r5/mate2_B.png')]}
nat=Image.open(D+'r1/natief.png').convert('RGB').crop((9,25,87,79))
V=Image.new('RGB',(2200,1250),(255,255,255)); d=ImageDraw.Draw(V); x=10
for k in sp: d.text((x,10),k+' 8x',fill=0); V.paste(up(on(sp[k],(235,240,235)),8),(x,28)); x+=530
d.text((x,10),'model natief 6x (ongeschrapt)',fill=0); V.paste(up(nat,6),(x,28))
y=600; x=10
for k in sp:
    a=up(on(sp[k],(235,240,235)).crop((48,40,64,64)),12); d.text((x,y-15),k+' rechterrand 12x',fill=0); V.paste(a,(x,y)); x+=a.width+10
m=up(nat.crop((70-9,52-25,86-9,79-25)),12); d.text((x,y-15),'model achtersteven 12x',fill=0); V.paste(m,(x,y)); x+=m.width+20
for i,k in enumerate(sp):
    V.paste(on(sp[k],(255,255,255)),(x,y+i*80)); V.paste(on(sp[k],(40,40,48)),(x+70,y+i*80)); d.text((x+140,y+i*80+25),k,fill=0)
V.crop((0,0,2200,y+340)).save(D+'r6/vel.png')
