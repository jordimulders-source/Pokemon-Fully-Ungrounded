# maakt ../vel.png: ronde 4 | ronde 5 op 4x en 1x (licht/donker), kop en handen op 8x
import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__))
def ld(p):
    im=Image.open(p); idx=im.load(); a=im.convert('RGBA'); px=a.load()
    for y in range(64):
        for x in range(64):
            if idx[x,y]==0: px[x,y]=(0,0,0,0)
    return a
r4=ld(os.path.join(H,'../../ronde5/nachtaap.png')); r5=ld(os.path.join(H,'../nachtaap.png'))
L=(236,236,230,255); DK=(40,40,48,255)
o=Image.new('RGBA',(1100,580),L); d=ImageDraw.Draw(o)
def put(im,x,y,bg,lab=None,s=1):
    im=im.resize((im.width*s,im.height*s),Image.NEAREST); b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); o.paste(b,(x,y))
    if lab: d.text((x,y+im.height+2),lab,fill=(30,30,30,255))
put(r4,0,0,L,'ronde 5, 4x',4); put(r5,266,0,L,'ronde 6, 4x',4); put(r5,532,0,DK,'ronde 6 op donker',4)
x=800
for n,r in (('r5',r4),('r6',r5)):
    put(r,x,0,L,n+' 1x'); put(r,x+76,0,DK,n+' donker'); x+=160
put(r5,800,90,L,'r6 3x',3)
put(r4.crop((12,22,50,40)),0,280,L,'rug ronde 5, 6x',6); put(r5.crop((12,22,50,40)),0,420,L,'rug ronde 6, 6x',6); put(r4.crop((0,34,28,44)),240,560,L,'oren r5, 6x',6) if False else None
put(r4.crop((2,54,43,63)),440,280,L,'handen/voeten ronde 4, 8x',8) if False else None
put(r4.crop((2,54,43,63)),440,280,L,'handen/voet ronde 5, 6x',6)
put(r5.crop((2,54,43,63)),440,370,L,'handen/voet ronde 6, 6x',6); put(r4.crop((2,35,28,44)),440,460,L,'kop+oren r5, 6x',6); put(r5.crop((2,35,28,44)),620,460,L,'kop+oren r6, 6x',6)
o.save(os.path.join(H,'../vel.png'))
