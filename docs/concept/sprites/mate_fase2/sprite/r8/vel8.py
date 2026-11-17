# r8/vel.png: A | B | r7 (8x); rechterrand A | B | r7 (12x); hulpbeeld zonder bombilla A | B (12x); 1x licht/donker
from PIL import Image, ImageDraw
D='docs/concept/sprites/mate_fase2/sprite/'
def on(im,c):
    b=Image.new('RGBA',im.size,c+(255,)); b.alpha_composite(im.convert('RGBA')); return b.convert('RGB')
def up(im,s): return im.resize((im.width*s,im.height*s),Image.NEAREST)
sp={k:Image.open(D+p).convert('RGBA') for k,p in [('A','r8/mate2_A.png'),('B','r8/mate2_B.png'),('r7','r7/mate2.png')]}
V=Image.new('RGB',(1620,1300),(255,255,255)); d=ImageDraw.Draw(V); x=10
for k in sp: d.text((x,10),k+' 8x',fill=0); V.paste(up(on(sp[k],(235,240,235)),8),(x,28)); x+=530
y=600; x=10
for k in sp:
    a=up(on(sp[k],(235,240,235)).crop((46,38,64,60)),12); d.text((x,y-15),k+' rechterrand 12x',fill=0); V.paste(a,(x,y)); x+=a.width+10
for k in ('A','B'):
    h=up(Image.open(D+'r8/hulp_%s.png'%k).crop((44,38,64,62)),12); d.text((x,y-15),'hulp '+k+' zonder bombilla 12x',fill=0); V.paste(h,(x,y)); x+=h.width+10
y2=y+300
for i,k in enumerate(sp):
    V.paste(on(sp[k],(255,255,255)),(10+i*160,y2)); V.paste(on(sp[k],(40,40,48)),(80+i*160,y2)); d.text((10+i*160,y2+68),k,fill=0)
V.crop((0,0,1620,y2+90)).save(D+'r8/vel.png')
