# vel.py: r8 | r5-proef | model (8x); close-ups 16x naast het model (kop+kuif, wolk); 1x op licht/donker. python3 sprite_r8/vel.py
import sys; sys.path.insert(0,'gereedschap'); sys.path.insert(0,'sprite_r5')
from PIL import Image, ImageDraw; import basis as B
def plat(p,bg=(255,255,255)):
    im=Image.open(p).convert('RGBA'); b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
u0,v0=B.blok(0,0)
M=Image.new('RGB',(192,192),'white'); M.paste(Image.fromarray(B.a.astype('uint8')),(-u0,-v0))   # model, 3 natief per spritepixel
R8,R5='sprite_r8/altaria_r8.png','sprite_r5/proef_eindkeuring.png'
W=3*512+2*16; vel=Image.new('RGB',(W,512+40+352+40+200),'white'); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate(((plat(R8),'r8'),(plat(R5),'r5-proef'),(M,'model'))):
    vel.paste(im.resize((512,512),Image.NEAREST),(i*528,24)); d.text((i*528+4,6),t,fill=(0,0,0))
y=24+512+16
def close(box,x,y,Z=16):
    X0,Y0,X1,Y1=box
    s=plat(R8).crop(box).resize(((X1-X0)*Z,(Y1-Y0)*Z),Image.NEAREST)
    m=M.crop((3*X0,3*Y0,3*X1,3*Y1)).resize(s.size,Image.NEAREST)
    vel.paste(s,(x,y)); vel.paste(m,(x+s.width+6,y)); return x+2*s.width+12
d.text((4,y-14),'close-up 16x: kop+kuif (X20-54, Y4-26) r8 | model        wolk (X8-30, Y36-58) r8 | model',fill=(0,0,0))
x=close((20,4,42,26),0,y)
x=close((8,36,30,58),x+10,y)
y+=352+30
for i,bg in enumerate(((255,255,255),(232,224,200),(80,96,120),(24,24,32))):
    vel.paste(plat(R8,bg),(8+i*80,y))
    vel.paste(plat(R8,bg).resize((128,128),Image.NEAREST),(340+i*140,y))
vel.paste(M.resize((64,64),Image.BOX),(8,y+90)); d.text((80,y+110),'model 1x',fill=(0,0,0))
vel.paste(plat(R5).resize((64,64)),(8,y+ 90+70) if False else (180,y+90)); d.text((250,y+110),'r5-proef 1x',fill=(0,0,0))
vel.save('sprite_r8/vel.png')
