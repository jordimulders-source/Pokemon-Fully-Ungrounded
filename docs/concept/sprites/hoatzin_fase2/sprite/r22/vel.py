# vel.png: r22 | r21 | r17 | model op 8x, daarna 16x-uitsneden (kuif, vleugel, nek, poten): r22 | r21 | pixelblad | model
import numpy as np; from PIL import Image, ImageDraw
from raster import *
def wit(p):
    s=Image.open(p).convert('RGBA'); w=Image.new('RGB',(64,64),'white'); w.paste(s,(0,0),s); return w
blad=Image.fromarray(np.load('../r17/blad64.npy',allow_pickle=True).item()['rgb'].astype('uint8'))
rij=[]
top=[wit('hoatzin.png').resize((512,512),Image.NEAREST),wit('../r21/hoatzin.png').resize((512,512),Image.NEAREST),wit('../r17/hoatzin.png').resize((512,512),Image.NEAREST),model_img(8)]
r=Image.new('RGB',(4*522,532),'white'); d=ImageDraw.Draw(r)
for i,(p,t) in enumerate(zip(top,('r22','r21','r17','model'))): r.paste(p,(i*522,20)); d.text((i*522+4,4),t+' (8x)',fill=(0,0,0))
rij.append(r)
K=16
def paneel(im,x0,y0,x1,y1): return labels(grid(im.crop((x0,y0,x1,y1)).resize(((x1-x0)*K,(y1-y0)*K),Image.NEAREST),K,x0,y0),K,18,x0,y0,max(x1-x0,y1-y0))
for nm,(x0,y0,x1,y1) in (('kuif',(4,3,30,24)),('vleugel',(28,2,57,50)),('nek',(14,20,37,42)),('poten',(12,47,40,64))):
    ps=[paneel(wit('hoatzin.png'),x0,y0,x1,y1),paneel(wit('../r21/hoatzin.png'),x0,y0,x1,y1),paneel(blad,x0,y0,x1,y1),
        labels(grid(model_img(K,x0,y0,x1,y1),K,x0,y0),K,18,x0,y0,max(x1-x0,y1-y0))]
    w=sum(p.width for p in ps)+30; r=Image.new('RGB',(w,ps[0].height+20),'white'); d=ImageDraw.Draw(r); x=0
    for p,t in zip(ps,('r22','r21','pixelblad','model')): r.paste(p,(x,20)); d.text((x+20,4),nm+': '+t,fill=(0,0,0)); x+=p.width+10
    rij.append(r)
V=Image.new('RGB',(max(r.width for r in rij),sum(r.height+10 for r in rij)),'white'); y=0
for r in rij: V.paste(r,(0,y)); y+=r.height+10
V.save('vel.png'); print(V.size)
