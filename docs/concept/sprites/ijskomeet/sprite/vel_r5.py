# vel_r5: r5 | r4 | model (8x); naadmasker (uit model) naast model op 12x; 1x/2x licht/donker; naast regice
from PIL import Image, ImageDraw
import numpy as np
G='../../../../../graphics/pokemon/'
def rgba(p): return Image.open(p).convert('RGBA').crop((0,0,64,64))
def mon(s):
    im=rgba(G+s+'/anim_front.png'); px=im.load(); bg=px[0,0]
    if bg[3]==255:
        for y in range(64):
            for x in range(64):
                if px[x,y]==bg: px[x,y]=(0,0,0,0)
    return im
def op(im,c):
    b=Image.new('RGBA',im.size,c+(255,)); b.alpha_composite(im); return b.convert('RGB')
r5,r4=rgba('r5.png'),rgba('r4.png'); mod=Image.open('keuring/model3x_r2.png').convert('RGBA')
W=Image.new('RGB',(1840,1560),(255,255,255)); d=ImageDraw.Draw(W)
for i,(im,n) in enumerate([(r5,'r5'),(r4,'r4'),(mod,'model (natief /3)')]):
    W.paste(op(im,(255,255,255)).resize((512,512),0),(10+530*i,24)); d.text((10+530*i,6),n,fill=0)
# naadmasker naast model, 12x, lijf+kop-onderkant x0-36 y34-61
S=np.load('r5_seam_af.npy'); x0,y0,x1,y1=0,34,36,61; Z=12
mz=Image.open('model_12x.png').convert('RGB').crop((x0*Z,y0*Z,x1*Z,y1*Z))
mk=Image.new('RGB',mz.size,(255,255,255)); dm=ImageDraw.Draw(mk)
ov=mz.copy(); do=ImageDraw.Draw(ov)
for y in range(y0,y1):
    for x in range(x0,x1):
        if S[y,x]:
            dm.rectangle([(x-x0)*Z,(y-y0)*Z,(x-x0+1)*Z-1,(y-y0+1)*Z-1],fill=(20,20,60))
            do.rectangle([(x-x0)*Z+3,(y-y0)*Z+3,(x-x0+1)*Z-4,(y-y0+1)*Z-4],fill=(255,0,0))
sp=op(r5,(255,255,255)).crop((x0,y0,x1,y1)).resize(mz.size,0)
for i,(im,n) in enumerate([(mz,'model 12x'),(mk,'naadmasker (uit model, 1 px)'),(ov,'masker op model'),(sp,'r5 12x')]):
    W.paste(im,(10+(mz.size[0]+12)*i,580)); d.text((10+(mz.size[0]+12)*i,566),n,fill=0)
y=920; x=10
for im,n in [(r5,'r5'),(r4,'r4')]:
    for c in [(255,255,255),(40,40,48)]:
        W.paste(op(im,c),(x,y)); W.paste(op(im,c).resize((128,128),0),(x+70,y)); x+=210
    d.text((x-420,y+132),n+' (1x/2x licht, donker)',fill=0)
y=1090; x=10
for im,n in [(r5,'r5'),(mon('regice'),'regice'),(mon('lunatone'),'lunatone')]:
    W.paste(op(im,(255,255,255)).resize((128,128),0),(x,y)); W.paste(op(im,(104,160,112)).resize((128,128),0),(x,y+140)); d.text((x,y-14),n,fill=0); x+=150
W=W.crop((0,0,1840,1380)); W.save('vel_r5.png')
