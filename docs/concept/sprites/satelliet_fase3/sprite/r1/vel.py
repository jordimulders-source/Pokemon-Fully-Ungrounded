from PIL import Image, ImageDraw
import numpy as np
exec(open('bouw.py').read().split("# ---- 1.")[0])
TOP=(64-OH)//2+3
sp=Image.open('sprite.png'); pal=sp.getpalette(); A=np.array(sp)
def rgb(a,bgc):
    r=np.array(pal[:48]).reshape(16,3)[a].astype(np.uint8); r[a==0]=bgc; return Image.fromarray(r)
def grid(img,k,step=8,col=(210,210,210)):
    d=ImageDraw.Draw(img)
    for i in range(0,img.width+1,k*step): d.line([(i,0),(i,img.height)],fill=col)
    for i in range(0,img.height+1,k*step): d.line([(0,i),(img.width,i)],fill=col)
    return img
s8=rgb(A,(235,240,235)).resize((512,512),Image.NEAREST)
m=Image.open(kaal.M).convert('RGB').crop((X0,Y0,X1,Y1))
mh=int(round(m.height/s)); ms=m.resize((64,mh),Image.LANCZOS)
mc=Image.new('RGB',(64,64),(255,255,255)); mc.paste(ms,(0,TOP))
m8=mc.resize((512,512),Image.NEAREST)
# model op 8x met echte modelresolutie (scherp) ter vergelijking
mfull=Image.new('RGB',(512,512),(255,255,255)); mm=m.resize((512,int(m.height*512/m.width)),Image.NEAREST); mfull.paste(mm,(0,int(TOP*8)))
W_=512*3+40; Hh=512+40+300+40+140
vel=Image.new('RGB',(W_,Hh),(250,250,250)); d=ImageDraw.Draw(vel)
vel.paste(s8,(0,30)); vel.paste(m8,(512+20,30)); vel.paste(mfull,(1024+40,30))
d.text((4,8),'r1 sprite 8x (64x64)',fill=(0,0,0)); d.text((532,8),'model verkleind naar 64 breed (vlakgemiddelde) 8x',fill=(0,0,0)); d.text((1068,8),'model_gekozen.png op dezelfde maat (scherp)',fill=(0,0,0))
y0=30+512+20
# close-ups 16x: ogen en panelen, sprite boven model
def crop16(x0,y0_,w,h,img_sprite=True):
    if img_sprite: im=rgb(A,(235,240,235)).crop((x0,y0_+TOP,x0+w,y0_+TOP+h))
    else: im=m.crop((int(x0*s),int(y0_*s),int((x0+w)*s),int((y0_+h)*s))).resize((w,h),Image.LANCZOS)
    return im.resize((w*16,h*16),Image.NEAREST)
def crop16m(x0,y0_,w,h):
    im=m.crop((int(round(x0*s)),int(round(y0_*s)),int(round((x0+w)*s)),int(round((y0_+h)*s))))
    return im.resize((w*16,h*16),Image.NEAREST)
cx=0
for name,(x0,yy0,w,h) in {'voorste oog':(10,31,10,10),'oog links':(15,14,8,8),'oog rechts':(48,22,8,8),'paneel links (PD)':(0,23,16,9),'mast boven (PB)':(32,0,6,15)}.items():
    a1=crop16(x0,yy0,w,h); a2=crop16m(x0,yy0,w,h)
    if cx+a1.width>W_: break
    vel.paste(a1,(cx,y0+14)); vel.paste(a2,(cx,y0+14+a1.height+4)); d.text((cx+2,y0),name+' (sprite / model)',fill=(0,0,0))
    cx+=a1.width+12
y1=y0+14+2*16*15+20
for i,bgc in enumerate(((255,255,255),(240,236,226),(40,40,48),(10,10,14))):
    vel.paste(rgb(A,bgc),(cx+10+i*72,y0+20))
    vel.paste(rgb(A,bgc).resize((192,192),Image.NEAREST),(cx+10+i*200 if False else cx+10+ (i%2)*200, y0+100+(i//2)*200))
d.text((cx+10,y0+4),'1x en 3x op licht en donker',fill=(0,0,0))
vel.save('vel.png')
print(vel.size)
