# Keurvel r12 p2 (eindkeuring): sprite | model verkleind naar 64 (box), 8x; 1x op licht/donker.
import numpy as np; from PIL import Image, ImageDraw
D='../../'
s=Image.open(D+'sprite/r12/sprite_B_p2.png').convert('RGBA')
m=Image.open(D+'referenties/model_v14.png').convert('RGB')
m=m.crop((140,120,880,880)).resize((64,64),Image.BOX)
ma=np.array(m.convert('RGBA')); wit=(np.abs(ma[...,:3].astype(int)-255).sum(2)<40); ma[wit,3]=0
m64=Image.fromarray(ma); m64.save('model64.png')
Z=8; W=64*Z
vel=Image.new('RGB',(2*W+48+4*64+40,W+20),(200,200,200))
for i,im in enumerate([s,m64]):
    bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(im)
    big=bg.convert('RGB').resize((W,W),Image.NEAREST); d=ImageDraw.Draw(big)
    for k in range(0,W,8*Z): d.line((k,0,k,W),fill=(220,220,255)); d.line((0,k,W,k),fill=(220,220,255))
    vel.paste(big,(10+i*(W+20),10))
x0=2*W+50
for j,(im,c) in enumerate([(s,(255,255,255)),(m64,(255,255,255)),(s,(40,40,48)),(m64,(40,40,48))]):
    bg=Image.new('RGBA',(64,64),c+(255,)); bg.alpha_composite(im)
    vel.paste(bg.convert('RGB'),(x0+(j%2)*70,10+(j//2)*70))
vel.save('keurvel_r12.png')
