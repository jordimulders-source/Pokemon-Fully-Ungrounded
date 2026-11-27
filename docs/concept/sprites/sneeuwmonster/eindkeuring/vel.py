# Vel eindkeuring: voor | na | model op 8x, kop- en voeten-close-up op 12x, 1x op wit/creme/donker/zwart; plus sneeuwmonster_8x.png
# Gebruik: cd sneeuwmonster && python3 eindkeuring/vel.py
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import X0,Y0,U0,V0,S,MODEL
U='eindkeuring/'
def laad(p):
    im=Image.open(p); o=np.asarray(im).astype(int); q=im.getpalette(); return o,[tuple(q[3*i:3*i+3]) for i in range(16)]
def rgb(op,bg=(255,255,255)):
    o,P=op; img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=P[k]
    return Image.fromarray(img)
voor=laad('sprite_r10/sneeuwmonster_r10.png'); na=laad(U+'sneeuwmonster_ek.png')
MI=Image.open(MODEL).convert('RGB'); f=lambda u,ph:ph+0.5+10.24*u
def mcrop(x0,y0,x1,y1,z):
    u0=(x0-X0)/S+U0; u1=(x1-X0)/S+U0; v0=(y0-Y0)/S+V0; v1=(y1-Y0)/S+V0
    return MI.crop((int(f(u0,9.05)),int(f(v0,9.25)),int(f(u1,9.05)),int(f(v1,9.25)))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def grid(im,z,x0,y0):
    d=ImageDraw.Draw(im)
    for i in range(im.width//z+1): d.line([(i*z,0),(i*z,im.height)],fill=(255,120,120) if (x0+i)%5==0 else (215,215,215))
    for j in range(im.height//z+1): d.line([(0,j*z),(im.width,j*z)],fill=(255,120,120) if (y0+j)%5==0 else (215,215,215))
    return im
def paneel(K,z,raster):
    x0,y0,x1,y1=K; out=[]
    for im in (rgb(voor).crop(K),rgb(na).crop(K)):
        b=im.resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); out.append(grid(b,z,x0,y0) if raster else b)
    m=mcrop(*K,z); out.append(grid(m,z,x0,y0) if raster else m); return out
B=(14,8,50,56); KOP=(18,9,44,33); VOET=(17,44,46,54)
rijen=[('voor (r10) | na (eindkeuring) | model, 8x',paneel(B,8,False)),('kop 12x',paneel(KOP,12,True)),('voeten 12x',paneel(VOET,12,True))]
W=max(sum(p.width for p in r)+20 for _,r in rijen)
H=sum(r[0].height+20 for _,r in rijen)+170
V=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(V); y=0
for t,r in rijen:
    d.text((4,y+3),t,fill=(200,0,0)); x=0
    for p in r: V.paste(p,(x,y+16)); x+=p.width+10
    y+=r[0].height+20
d.text((4,y+3),'1x: voor (boven) en na (onder) op wit, creme, donker, zwart; rechts 2x',fill=(200,0,0)); y+=16
for i,op in enumerate((voor,na)):
    x=0
    for bg in ((255,255,255),(248,240,216),(56,64,80),(0,0,0)): V.paste(rgb(op,bg),(x,y+i*68)); x+=70
    for j,bg in enumerate(((255,255,255),(56,64,80))): V.paste(rgb(op,bg).resize((128,128),Image.NEAREST),(300+i*280+j*135,y))
V.save(U+'vel.png'); print(U+'vel.png',V.size)
rgb(na).resize((512,512),Image.NEAREST).save(U+'sneeuwmonster_8x.png')
