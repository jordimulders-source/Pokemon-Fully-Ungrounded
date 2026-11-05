# maakt ../vel.png: ronde 12 | ronde 13 op 4x en 1x (licht/donker), achterwig en voorpoten op 8x
import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__))
def ld(p):
    im=Image.open(p); idx=im.load(); a=im.convert('RGBA'); px=a.load()
    for y in range(64):
        for x in range(64):
            if idx[x,y]==0: px[x,y]=(0,0,0,0)
    return a
r12=ld(os.path.join(H,'../../ronde12/nachtaap.png')); r13=ld(os.path.join(H,'../nachtaap.png'))
L=(236,236,230,255); DK=(40,40,48,255)
o=Image.new('RGBA',(1100,600),L); d=ImageDraw.Draw(o)
def put(im,x,y,bg,lab=None,s=1):
    im=im.resize((im.width*s,im.height*s),Image.NEAREST); b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); o.paste(b,(x,y))
    if lab: d.text((x,y+im.height+2),lab,fill=(30,30,30,255))
put(r12,0,0,L,'ronde 12, 4x',4); put(r13,266,0,L,'ronde 13, 4x',4); put(r13,532,0,DK,'ronde 13 op donker',4)
put(r12,800,0,L,'r12 1x'); put(r13,880,0,L,'r13 1x'); put(r12,800,90,DK); put(r13,880,90,DK)
put(r12.crop((34,26,52,42)),0,290,L,'achterwig ronde 12, 8x',8); put(r13.crop((34,26,52,42)),160,290,L,'achterwig ronde 13, 8x',8)
put(r12.crop((2,50,32,63)),330,290,L,'voorpoten ronde 12, 8x',8); put(r13.crop((2,50,32,63)),330,420,L,'voorpoten ronde 13, 8x',8)
o.save(os.path.join(H,'../vel.png'))
