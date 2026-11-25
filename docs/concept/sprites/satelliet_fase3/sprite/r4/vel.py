# vel r4: r4 | r3 | model (8x); close-ups per paneel (r3 boven, model onder); 1x op licht/donker
from PIL import Image, ImageDraw
import numpy as np, kaal
OH=43; TOP=(64-OH)//2+3; s=3.515625
def ld(p):
    sp=Image.open(p); return np.array(sp),sp.getpalette()
def rgb(A,pal,bgc):
    r=np.array(pal[:48]).reshape(16,3)[A].astype(np.uint8); r[A==0]=bgc; return Image.fromarray(r)
A3,P3=ld('sprite.png'); A2,P2=ld('../r3/sprite.png')
m=Image.open(kaal.M).convert('RGB')
mm=m.crop((3,3,3+225,3+int(round(OH*s)))).resize((512,int(round(OH*s))*512//225),Image.NEAREST)
mfull=Image.new('RGB',(512,512),(255,255,255)); mfull.paste(mm,(0,TOP*8))
vel=Image.new('RGB',(1576,1100),(250,250,250)); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate(((rgb(A3,P3,(235,240,235)).resize((512,512),Image.NEAREST),'r4 8x'),(rgb(A2,P2,(235,240,235)).resize((512,512),Image.NEAREST),'r3 8x'),(mfull,'model_gekozen.png scherp, zelfde maat'))):
    vel.paste(im,(i*532,30)); d.text((i*532+4,8),t,fill=(0,0,0))
y0=562; Z=12
def c3(x0,yy,w,h): return rgb(A3,P3,(235,240,235)).crop((x0,yy+TOP,x0+w,yy+TOP+h)).resize((w*Z,h*Z),Image.NEAREST)
def cm(x0,yy,w,h): return m.crop((round(3+x0*s),round(3+yy*s),round(3+(x0+w)*s),round(3+(yy+h)*s))).resize((w*Z,h*Z),Image.NEAREST)
cx=0; rij=0
for name,(x0,yy,w,h) in {'PA':(19,5,20,9),'PC':(45,15,19,8),'PD':(0,23,18,9),'PE':(22,30,20,12),'PB':(32,0,6,14),'PF':(32,28,6,14)}.items():
    a1=c3(x0,yy,w,h); a2=cm(x0,yy,w,h)
    if cx+a1.width>1300: cx=0; rij+=1
    yb=y0+rij*250
    vel.paste(a1,(cx,yb+14)); vel.paste(a2,(cx,yb+14+a1.height+4)); d.text((cx+2,yb),name+' (r4 / model)',fill=(0,0,0)); cx+=a1.width+12
for i,bgc in enumerate(((255,255,255),(240,236,226),(40,40,48),(10,10,14))):
    vel.paste(rgb(A3,P3,bgc),(1340+(i%2)*80,y0+20+(i//2)*80))
d.text((1340,y0+4),'r4 1x licht/donker',fill=(0,0,0))
vel.save('vel.png'); print(vel.size)
