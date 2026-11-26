from PIL import Image, ImageDraw
import numpy as np
exec(open('bouw2.py').read().split('# ---- tekenen')[0])
TOP=(64-OH)//2+3
def ld(p):
    sp=Image.open(p); pal=sp.getpalette(); return np.array(sp),pal
A2,P2=ld('sprite.png'); A1,P1=ld('../r1/sprite.png')
def rgb(A,pal,bgc):
    r=np.array(pal[:48]).reshape(16,3)[A].astype(np.uint8); r[A==0]=bgc; return Image.fromarray(r)
m=Image.open(kaal.M).convert('RGB').crop((X0,Y0,X1,Y1))
mfull=Image.new('RGB',(512,512),(255,255,255)); mm=m.resize((512,int(m.height*512/m.width)),Image.NEAREST); mfull.paste(mm,(0,TOP*8))
vel=Image.new('RGB',(1576,1060),(250,250,250)); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate(((rgb(A2,P2,(235,240,235)).resize((512,512),Image.NEAREST),'r2 8x'),(rgb(A1,P1,(235,240,235)).resize((512,512),Image.NEAREST),'r1 8x'),(mfull,'model_gekozen.png scherp, zelfde maat'))):
    vel.paste(im,(i*532,30)); d.text((i*532+4,8),t,fill=(0,0,0))
y0=30+512+20
def c16(A,pal,x0,yy,w,h): return rgb(A,pal,(235,240,235)).crop((x0,yy+TOP,x0+w,yy+TOP+h)).resize((w*14,h*14),Image.NEAREST)
def c16m(x0,yy,w,h): return m.crop((int(round(x0*s)),int(round(yy*s)),int(round((x0+w)*s)),int(round((yy+h)*s)))).resize((w*14,h*14),Image.NEAREST)
cx=0
for name,(x0,yy,w,h) in {'voorste bol + oog':(9,28,14,14),'paneel PD':(0,22,18,10),'mast PB':(32,0,6,15),'paneel PE':(22,30,20,12)}.items():
    a1=c16(A2,P2,x0,yy,w,h); a2=c16m(x0,yy,w,h)
    vel.paste(a1,(cx,y0+14)); vel.paste(a2,(cx,y0+14+a1.height+4)); d.text((cx+2,y0),name+' (r2 / model)',fill=(0,0,0)); cx+=a1.width+12
for i,bgc in enumerate(((255,255,255),(240,236,226),(40,40,48),(10,10,14))):
    vel.paste(rgb(A2,P2,bgc),(1300+(i%2)*80,y0+20+(i//2)*80))
d.text((1300,y0+4),'r2 1x licht/donker',fill=(0,0,0))
vel.save('vel.png'); print(vel.size)
