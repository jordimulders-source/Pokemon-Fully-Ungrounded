# Vel r15: r15 | r14 op 8x, per gemarkeerde lijn een nummer (groen = veranderd, rood = recht gelaten), veranderde pixels
# omkaderd op r15; 1x en 2x op licht en donker. Gebruik: python3 vel15.py -> r15/vel.png
import numpy as np
from PIL import Image, ImageDraw
r15=Image.open('r15/kudu_r15.png').convert('RGBA'); r14=Image.open('r14/kudu_r14.png').convert('RGBA')
g0=np.load('r14/grid.npy'); g=np.load('r15/grid.npy')
BG=(196,206,218,255); S=8; V=Image.new('RGBA',(1100,860),BG); d=ImageDraw.Draw(V)
def plak(im,x,y,s,bg=None):
    if bg: V.paste(Image.new('RGBA',(im.width*s,im.height*s),bg),(x,y))
    V.alpha_composite(im.resize((im.width*s,im.height*s),Image.NEAREST),(x,y))
X1,X2,Y=10,560,22
d.text((X1,4),'r15 (kaders = veranderde pixels)',fill=(0,0,0,255)); d.text((X2,4),'r14',fill=(0,0,0,255))
plak(r15,X1,Y,S); plak(r14,X2,Y,S)
for y,x in np.argwhere(g0!=g): d.rectangle((X1+x*S,Y+y*S,X1+x*S+S-1,Y+y*S+S-1),outline=(0,200,255,255))
# nummer per lijn: (x,y) label-positie in spritepx, veranderd?
N={1:(31.5,8,1),2:(8,14.5,0),3:(30,15.5,1),4:(3.5,22.5,1),5:(10,30,1),6:(21.3,25.2,0),7:(15.8,35.6,1),8:(41,28.6,1),
   9:(34.4,46,1),10:(45.5,46,1),11:(55.5,44,1),12:(39,46.8,1),13:(56,52,1),14:(19.5,52,1),15:(34,55,1)}
for n,(x,y,v) in N.items():
    for X0 in (X1,X2):
        c=(0,150,0,255) if v else (200,0,0,255)
        px,py=X0+int(x*S),Y+int(y*S); d.rectangle((px-2,py-2,px+14,py+11),fill=(255,255,255,255),outline=c); d.text((px,py),str(n),fill=c)
d.text((X1,Y+64*S+4),'groen = lijn veranderd (knik naar het model), rood = recht gelaten (model is daar recht)',fill=(0,0,0,255))
y=Y+64*S+22
for bg in [(248,248,248,255),(40,44,52,255)]:
    x=10
    for im in [r15,r14]: plak(im,x,y,1,bg); x+=70
    x=160
    for im in [r15,r14]: plak(im,x,y,2,bg); x+=134
    y+=134
d.text((10,y),'1x en 2x: r15, r14 (licht en donker)',fill=(0,0,0,255))
V=V.crop((0,0,1100,y+20)); V.save('r15/vel.png'); print(V.size)
