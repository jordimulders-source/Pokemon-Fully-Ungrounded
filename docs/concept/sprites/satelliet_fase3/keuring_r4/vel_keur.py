# Keurder r4: sprite / kaal / model op dezelfde maat, 8x met raster.
from PIL import Image, ImageDraw
import numpy as np
B='docs/concept/sprites/satelliet_fase3/'
s=Image.open(B+'sprite/r4/sprite.png').convert('RGBA')
k=Image.open(B+'sprite/r4/kaal.png').convert('RGBA')
m=Image.open(B+'model/model_gekozen.png').convert('RGBA')
a=np.array(m); al=a[:,:,3]>0
ys,xs=np.where(al)
mc=m.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
w=64; h=round(mc.height*64/mc.width)
mm=Image.new('RGBA',(64,64)); sa=np.array(s)[:,:,3]>0; sy=np.where(sa)[0].min()
mm.paste(mc.resize((w,h),Image.LANCZOS),(0,sy))
def big(im,f=8,grid=True):
    bg=Image.new('RGBA',im.size,(232,238,232,255)); bg.alpha_composite(im)
    b=bg.resize((im.width*f,im.height*f),Image.NEAREST)
    if grid:
        d=ImageDraw.Draw(b)
        for i in range(0,im.width*f,f*8): d.line([(i,0),(i,b.height)],fill=(255,0,0,90))
        for i in range(0,im.height*f,f*8): d.line([(0,i),(b.width,i)],fill=(255,0,0,90))
    return b
sa_=np.array(s); ka=np.array(k)
dif=sa_.copy(); msk=(sa_!=ka).any(2); dif[msk]=[255,0,0,255]
D=Image.fromarray(dif)
crop=(0,10,64,58)
tiles=[big(x.crop(crop)) for x in (s,k,mm,D)]
W=sum(t.width for t in tiles)+30; H=tiles[0].height
out=Image.new('RGBA',(W,H),(250,250,250,255)); x=0
for t in tiles: out.paste(t,(x,0)); x+=t.width+10
out.save(B+'keuring_r4/vergelijk_8x.png')
one=Image.new('RGBA',(64*3+20,64),(232,238,232,255))
for i,t in enumerate((s,k,mm)): one.alpha_composite(t,(i*74,0))
one.resize((one.width*3,one.height*3),Image.NEAREST).save(B+'keuring_r4/vergelijk_1x_3x.png')
one.save(B+'keuring_r4/vergelijk_1x.png')
