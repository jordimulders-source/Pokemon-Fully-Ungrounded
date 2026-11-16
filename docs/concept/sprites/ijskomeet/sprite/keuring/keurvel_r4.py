# Keurder r4: model (3x-verkleind, uitgelijnd) naast r3 op 8x, en r3 tussen Gen 3-soorten op 1x en 2x
from PIL import Image, ImageDraw
G='../../../../../../graphics/pokemon/'
def ld(p):
    im=Image.open(p).convert('RGBA'); return im.crop((0,0,64,64))
def wit(im):
    b=Image.new('RGBA',im.size,(255,255,255,255)); b.alpha_composite(im); return b.convert('RGB')
spr=Image.open('../r4.png').convert('RGBA')
mod=Image.open('model3x_r2.png').convert('RGB')
soorten=['lunatone','solrock','glalie','regice','metagross']
mons=[]
for s in soorten:
    im=Image.open(G+s+'/anim_front.png').convert('RGBA').crop((0,0,64,64))
    px=im.load(); bg=px[0,0]
    if bg[3]==255:
        for y in range(64):
            for x in range(64):
                if px[x,y]==bg: px[x,y]=(0,0,0,0)
    mons.append(im)
W=Image.new('RGB',(1100,1060),(255,255,255)); d=ImageDraw.Draw(W)
W.paste(mod.resize((512,512),0),(10,20)); d.text((10,4),'model (natief raster /3, uitgelijnd)',fill=0)
W.paste(wit(spr).resize((512,512),0),(560,20)); d.text((560,4),'r4 8x',fill=0)
allen=[spr]+mons; namen=["r4"]+soorten
x=10
for im,n in zip(allen,namen):
    W.paste(wit(im),(x,560)); d.text((x,630),n,fill=0); x+=80
x=10
for im,n in zip(allen,namen):
    W.paste(wit(im).resize((128,128),0),(x,660)); d.text((x,792),n,fill=0); x+=138
# donkere achtergrond (battle-achtig)
x=10
for im,n in zip(allen,namen):
    b=Image.new('RGBA',(128,128),(112,160,112,255)); b.alpha_composite(im.resize((128,128),0)); W.paste(b.convert('RGB'),(x,820)); x+=138
W.save('keurvel_r4.png')
