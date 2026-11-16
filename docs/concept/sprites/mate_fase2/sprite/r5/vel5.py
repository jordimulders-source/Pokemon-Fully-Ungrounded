# r5/vel.png: A | B | r4 | model natief (8x); close-up achtersteven (sprite | model) 12x voor A, B en r4; 1x
from PIL import Image, ImageDraw
D='docs/concept/sprites/mate_fase2/sprite/'
def on(im,c):
    b=Image.new('RGBA',im.size,c+(255,)); b.alpha_composite(im.convert('RGBA')); return b.convert('RGB')
def up(im,s): return im.resize((im.width*s,im.height*s),Image.NEAREST)
sp={k:Image.open(D+p).convert('RGBA') for k,p in [('A','r5/mate2_A.png'),('B','r5/mate2_B.png'),('r4','r4/mate2.png')]}
nat=Image.open(D+'r1/natief.png').convert('RGB').crop((9,25,87,79))
V=Image.new('RGB',(2200,1250),(255,255,255)); d=ImageDraw.Draw(V)
x=10
for k in ('A','B','r4'):
    d.text((x,10),k+' 8x',fill=0); V.paste(up(on(sp[k],(235,240,235)),8),(x,28)); x+=530
d.text((x,10),'model natief 8x (ongeschrapt)',fill=0); V.paste(up(nat,6),(x,28))
# achtersteven: model natief x66-86, y40-79 ; sprites x48-64
mod=up(nat.crop((66-9,40-25,86-9,79-25)),12)
y=600; x=10
for k in ('A','B','r4'):
    a=up(on(sp[k],(235,240,235)).crop((46,15,64,64)),12)
    d.text((x,y-15),k+' achtersteven 12x',fill=0); V.paste(a,(x,y)); x+=a.width+10
d.text((x,y-15),'model achtersteven 12x',fill=0); V.paste(mod,(x,y)); x+=mod.width+20
for i,k in enumerate(('A','B','r4')):
    V.paste(on(sp[k],(255,255,255)),(x,y+i*80)); V.paste(on(sp[k],(40,40,48)),(x+70,y+i*80)); d.text((x+140,y+i*80+25),k,fill=0)
V.paste(nat,(x,y+250))
V.crop((0,0,2200,1200)).save(D+'r5/vel.png')
