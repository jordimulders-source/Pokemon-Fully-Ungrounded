# vel r2: r2 8x | r1 8x | model (natief) verkleind op dezelfde maat 8x ; 1x/2x r2 op licht en donker, r1 en model 1x/2x
import sys; from PIL import Image, ImageDraw; import numpy as np
H=lambda c:[int(c[i:i+2],16) for i in (1,3,5)]
PAL=['#1e170e','#433425','#5f4b3a','#765a43','#9f7e65','#b39b87','#36332b','#4e4a44','#7b7975','#a39b93','#d8c8b0']
P=np.array([H(c) for c in PAL],np.uint8)
def rgba(f):
    o=np.load(f); r=np.zeros((64,64,4),np.uint8); r[o>0,:3]=P[o[o>0]-1]; r[o>0,3]=255; return Image.fromarray(r,'RGBA')
sp=rgba('sprite.npy'); r1=rgba('../sprite_r3/sprite.npy')
sp.save('sprite.png'); w=Image.new('RGB',(64,64),'white'); w.paste(sp,(0,0),sp); w.resize((512,512),Image.NEAREST).save('sprite_8x.png')
X,Y,ww,hh=[int(t) for t in open('plaats.txt').read().split()]
m=Image.open('natief.png').convert('RGB'); a=np.asarray(m); fg=a.min(2)<225; ys,xs=np.where(fg)
ref=Image.new('RGB',(64,64),'white'); ref.paste(m.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)).resize((ww,hh),Image.LANCZOS),(X,Y))
def on(s,bg): b=Image.new('RGBA',(64,64),bg); return Image.alpha_composite(b,s).convert('RGB')
C=(0,120,512,512)  # alleen het deel met de sprite (rij 15-64)
V=Image.new('RGB',(3*512+4*16,392+16+40+150),(236,236,236)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate(((on(sp,(255,255,255,255)),'r4'),(on(r1,(255,255,255,255)),'r3'),(ref,'model op dezelfde maat'))):
    V.paste(im.resize((512,512),Image.NEAREST).crop(C),(16+i*528,24)); d.text((16+i*528,8),t+' 8x',fill=(0,0,0))
y=24+392+30; x=16
for s,t in ((sp,'r4'),(r1,'r3')):
    for bg in ((255,255,255),(40,44,60)):
        V.paste(on(s,bg+(255,)),(x,y)); V.paste(on(s,bg+(255,)).resize((128,128),Image.NEAREST),(x+72,y)); x+=216
    d.text((x-430,y-16),t+' 1x/2x licht, donker',fill=(0,0,0))
V.paste(ref,(x,y)); V.paste(ref.resize((128,128),Image.NEAREST),(x+72,y)); d.text((x,y-16),'model 1x/2x',fill=(0,0,0))
V.save('vel.png')
