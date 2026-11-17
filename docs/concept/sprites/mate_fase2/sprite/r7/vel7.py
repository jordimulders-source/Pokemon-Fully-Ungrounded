# r7/vel.png: r7 | r6 zacht | model (8x); hulpbeeld zonder bombilla 12x (uitsnede achterkant); rechterrand r7|r6 12x; 1x
from PIL import Image, ImageDraw
D='docs/concept/sprites/mate_fase2/sprite/'
def on(im,c):
    b=Image.new('RGBA',im.size,c+(255,)); b.alpha_composite(im.convert('RGBA')); return b.convert('RGB')
def up(im,s): return im.resize((im.width*s,im.height*s),Image.NEAREST)
r7=Image.open(D+'r7/mate2.png').convert('RGBA'); r6=Image.open(D+'r6/mate2_zacht.png').convert('RGBA')
nat=Image.open(D+'r1/natief.png').convert('RGB').crop((9,25,87,79)); hulp=Image.open(D+'r7/hulp_zonder_bombilla.png')
V=Image.new('RGB',(1700,1300),(255,255,255)); d=ImageDraw.Draw(V)
d.text((10,10),'r7 8x',fill=0); V.paste(up(on(r7,(235,240,235)),8),(10,28))
d.text((540,10),'r6 zacht 8x',fill=0); V.paste(up(on(r6,(235,240,235)),8),(540,28))
d.text((1070,10),'model natief 6x',fill=0); V.paste(up(nat,6),(1070,28))
y=600
h=up(hulp.crop((40,40,62,64)),12); d.text((10,y-15),'hulp r7: bombilla+zeefje weg (roze), sluitlijn achter zeefje (rood) 12x',fill=0); V.paste(h,(10,y))
a=up(on(r7,(235,240,235)).crop((44,42,62,62)),12); b=up(on(r6,(235,240,235)).crop((44,42,62,62)),12)
d.text((290,y-15),'rechterrand r7 | r6 zacht 12x',fill=0); V.paste(a,(290,y)); V.paste(b,(290+a.width+8,y))
x=290+2*a.width+30
for i,(k,im) in enumerate((('r7',r7),('r6',r6))):
    V.paste(on(im,(255,255,255)),(x,y+i*80)); V.paste(on(im,(40,40,48)),(x+70,y+i*80)); d.text((x+140,y+i*80+25),k,fill=0)
V.crop((0,0,1700,y+300)).save(D+'r7/vel.png')
