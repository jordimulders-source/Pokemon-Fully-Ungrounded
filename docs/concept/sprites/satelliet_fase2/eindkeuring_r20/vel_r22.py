# vel_r22.png: r21 8x | r22 8x (gewijzigd rood omrand) | model op spriteraster 8x;
# close-ups 16x van de vier plekken (r21 | r22 | model); 1x r22/r21 op licht en donker.
from PIL import Image, ImageDraw
import numpy as np
BG=(200,230,200); s=12.703125
M=Image.open('../paneel_varianten/panelen_80b.png').convert('RGB')
def rgb(path,bg=BG):
    im=Image.open(path); pal=im.getpalette(); a=np.array(im)
    o=np.zeros((64,64,3),np.uint8)
    for i in range(16): o[a==i]=pal[3*i:3*i+3]
    o[a==0]=bg; return Image.fromarray(o),a
r21,a21=rgb('r21/sprite.png'); r22,a22=rgb('r22/sprite.png')
r22.resize((512,512),Image.NEAREST).save('r22/sprite_8x.png')
diff=list(zip(*np.where(a21!=a22)))
def mod(x0,y0,x1,y1,z): return M.crop((round(103+x0*s),round(143+(y0-7)*s),round(103+x1*s),round(143+(y1-7)*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def mark(img,x0,y0,z):
    d=ImageDraw.Draw(img)
    for y,x in diff:
        X,Y=(x-x0)*z,(y-y0)*z
        if 0<=X<img.size[0] and 0<=Y<img.size[1]: d.rectangle([X,Y,X+z-1,Y+z-1],outline=(255,0,0),width=2)
    return img
ZONES=[('P1 linkerrand groot paneel',26,32,42,50),('P2 lenslijnen lichtkant',10,24,26,41),('P3 lensrand links (13,31-32)',9,27,19,37),('P4 kaprand rij 27-28',23,22,39,31)]
z=16
hz=sum((y1-y0)*z+24 for _,_,y0,_,y1 in ZONES)
V=Image.new('RGB',(3*512+40,24+512+20+hz+120),'white'); d=ImageDraw.Draw(V)
V.paste(r21.resize((512,512),Image.NEAREST),(0,24)); d.text((4,6),'r21 8x',fill='black')
V.paste(mark(r22.resize((512,512),Image.NEAREST),0,0,8),(532,24)); d.text((536,6),'r22 8x (rood = gewijzigd)',fill='black')
V.paste(mod(0,0,64,64,8),(1064,24)); d.text((1068,6),'model op spriteraster',fill='black')
y=24+512+20
for nm,x0,y0,x1,y1 in ZONES:
    w,h=(x1-x0)*z,(y1-y0)*z
    d.text((4,y),nm+f'  (x{x0}-{x1-1}, y{y0}-{y1-1}): r21 | r22 | model, 16x',fill='black')
    V.paste(r21.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(0,y+18))
    V.paste(mark(r22.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),x0,y0,z),(w+20,y+18))
    V.paste(mod(x0,y0,x1,y1,z),(2*w+40,y+18))
    y+=h+24
x=0
for bg in [(248,248,248),(40,40,48)]:
    for p in ('r22/sprite.png','r21/sprite.png'):
        t,_=rgb(p,bg); V.paste(t,(x,y)); x+=70
d.text((0,y+68),'1x: r22 | r21 op licht, r22 | r21 op donker',fill='black')
V=V.crop((0,0,V.size[0],y+90)); V.save('vel_r22.png'); print(V.size)
