# maakt ../vel.png: ronde 10 | ronde 11 op 4x en 1x (licht/donker), rug op 6x met de rode projectie-omlijning
import os, numpy as np
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(H,'../../../')
def ld(p):
    im=Image.open(p); idx=im.load(); a=im.convert('RGBA'); px=a.load()
    for y in range(64):
        for x in range(64):
            if idx[x,y]==0: px[x,y]=(0,0,0,0)
    return a
vb=ld(os.path.join(H,'../../ronde10/nachtaap.png')); r9=ld(os.path.join(H,'../nachtaap.png'))
K=np.load(os.path.join(D,'silhouet/wiggen_64.npy'))
L=(236,236,230,255); DK=(40,40,48,255)
o=Image.new('RGBA',(1000,560),L); d=ImageDraw.Draw(o)
def put(im,x,y,bg,lab=None,s=1):
    im=im.resize((im.width*s,im.height*s),Image.NEAREST); b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); o.paste(b,(x,y))
    if lab: d.text((x,y+im.height+2),lab,fill=(30,30,30,255))
    return b
put(vb,0,0,L,'ronde 10, 4x',4); put(r9,266,0,L,'ronde 11, 4x',4); put(r9,532,0,DK,'ronde 11 op donker',4)
put(vb,800,0,L,'r10'); put(r9,880,0,L,'r11'); put(vb,800,90,DK); put(r9,880,90,DK)
X0,Y0,X1,Y1,S=12,22,52,50,6
for i,(n,im) in enumerate((('ronde 10',vb),('ronde 11',r9))):
    ox=i*260; put(im.crop((X0,Y0,X1,Y1)),ox,280,L,'rug '+n+', 6x, rood = 3D-projectie',S)
    for y in range(Y0,Y1):
        for x in range(X0,X1):
            if not K[y,x]: continue
            px,py=ox+(x-X0)*S,280+(y-Y0)*S
            if not K[y-1,x]: d.line([(px,py),(px+S-1,py)],fill=(230,0,0,255))
            if not K[y+1,x]: d.line([(px,py+S-1),(px+S-1,py+S-1)],fill=(230,0,0,255))
            if not K[y,x-1]: d.line([(px,py),(px,py+S-1)],fill=(230,0,0,255))
            if not K[y,x+1]: d.line([(px+S-1,py),(px+S-1,py+S-1)],fill=(230,0,0,255))
put(r9,540,280,L,'ronde 11, 3x',3)
o.save(os.path.join(H,'../vel.png'))
