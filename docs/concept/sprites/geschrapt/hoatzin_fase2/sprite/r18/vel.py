# poot_vel.png: per gebied r18 | r17 | pixelblad (r17) | model, 16x met raster en coördinaten
import numpy as np; from PIL import Image, ImageDraw
from raster import *
K=16
def paneel(im,x0,y0,x1,y1):
    return labels(grid(im.crop((x0,y0,x1,y1)).resize(((x1-x0)*K,(y1-y0)*K),Image.NEAREST),K,x0,y0),K,18,x0,y0,max(x1-x0,y1-y0))
def wit(p):
    s=Image.open(p).convert('RGBA'); w=Image.new('RGB',(64,64),'white'); w.paste(s,(0,0),s); return w
B=np.load('../r17/blad64.npy',allow_pickle=True).item(); blad=Image.fromarray(B['rgb'].astype('uint8'))
rijen=[]
for nm,(x0,y0,x1,y1) in (('linkerpoot',(12,47,32,63+1)),('nek / vleugelvoorrand',(14,20,37,42))):
    ps=[paneel(wit('hoatzin.png'),x0,y0,x1,y1),paneel(wit('../r17/hoatzin.png'),x0,y0,x1,y1),paneel(blad,x0,y0,x1,y1),
        labels(grid(model_img(K,x0,y0,x1,y1),K,x0,y0),K,18,x0,y0,max(x1-x0,y1-y0))]
    w=sum(p.width for p in ps)+30; h=ps[0].height+20; r=Image.new('RGB',(w,h),'white'); d=ImageDraw.Draw(r); x=0
    for p,t in zip(ps,('r18','r17','pixelblad','model')):
        r.paste(p,(x,20)); d.text((x+20,4),nm+': '+t,fill=(0,0,0)); x+=p.width+10
    rijen.append(r)
V=Image.new('RGB',(max(r.width for r in rijen),sum(r.height for r in rijen)+10),'white'); y=0
for r in rijen: V.paste(r,(0,y)); y+=r.height+10
V.save('poot_vel.png'); print(V.size)
