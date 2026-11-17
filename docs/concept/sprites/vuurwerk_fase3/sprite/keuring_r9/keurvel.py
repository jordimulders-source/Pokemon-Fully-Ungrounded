# Keurvel r9: sprite_a | model verkleind naar 64 (box), 8x; 1x op licht/donker.
import sys, numpy as np; from PIL import Image, ImageDraw
D='../../'
s=Image.open(D+'sprite/r9/sprite_a.png').convert('RGBA')
m=Image.open(D+'referenties/model_v14.png').convert('RGB')
m=m.crop((140,120,880,880)).resize((64,64),Image.BOX)   # dier 708x739 -> ~61 px
ma=np.array(m.convert('RGBA')); wit=(np.abs(ma[...,:3].astype(int)-255).sum(2)<40); ma[wit,3]=0
m64=Image.fromarray(ma); m64.save('model64.png')
Z=8; W=64*Z
vel=Image.new('RGB',(2*W+48+4*64+40,W+20),(200,200,200))
for i,im in enumerate([s,m64]):
    bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(im)
    vel.paste(bg.convert('RGB').resize((W,W),Image.NEAREST),(10+i*(W+20),10))
x0=2*W+50
for j,(im,c) in enumerate([(s,(255,255,255)),(m64,(255,255,255)),(s,(40,40,48)),(m64,(40,40,48))]):
    bg=Image.new('RGBA',(64,64),c+(255,)); bg.alpha_composite(im)
    vel.paste(bg.convert('RGB'),(x0+(j%2)*70,10+(j//2)*70))
d=ImageDraw.Draw(vel)
# markeringen (sprite-coordinaten) uit het rapport
MARK={1:(0,28,26,56),2:(20,3,43,44),3:(2,4,30,27),4:(8,20,11,23),5:(25,8,40,17)}
for n,(a,b,c,e) in MARK.items():
    d.rectangle((10+a*Z,10+b*Z,10+c*Z,10+e*Z),outline=(0,160,255),width=3); d.text((14+a*Z,12+b*Z),str(n),fill=(0,0,255))
vel.save('keurvel_r9.png')
