# Keurder r4: sprite (16x, met coordinaten) naast hetzelfde stuk model; plus 1x-vergelijking met model verkleind.
import sys; sys.path.insert(0,'docs/concept/sprites/satelliet_fase3/sprite/r4')
from common import load
from PIL import Image, ImageDraw
import numpy as np
B='docs/concept/sprites/satelliet_fase3/'
a,bg=load(); ys,xs=np.where(~bg); X0,Y0=xs.min(),ys.min(); sc=(xs.max()+1-X0)/64
mi=np.dstack([a,np.where(bg,0,255)]).astype(np.uint8); m=Image.fromarray(mi,'RGBA')
s=Image.open(B+'sprite/r4/sprite.png').convert('RGBA'); TOP=13
def on(im):
    b=Image.new('RGBA',im.size,(232,238,232,255)); b.alpha_composite(im); return b
M=on(m); S=on(s)
def sb(x0,y0,x1,y1):
    c=S.crop((x0,y0,x1,y1)).resize(((x1-x0)*16,(y1-y0)*16),Image.NEAREST); d=ImageDraw.Draw(c)
    for i in range(x1-x0): d.text((i*16+2,2),str((x0+i)%100),fill=(255,0,0))
    for j in range(y1-y0): d.text((2,j*16+4),str(y0+j),fill=(0,0,255))
    return c
def mb(x0,y0,x1,y1,size):
    return M.crop((round(X0+x0*sc),round(Y0+(y0-TOP)*sc),round(X0+x1*sc),round(Y0+(y1-TOP)*sc))).resize(size,Image.NEAREST)
for n,box in [('hub',(28,24,48,38)),('voorarm',(8,32,40,56)),('links',(14,24,30,36)),('rechts',(40,16,60,42))]:
    p=sb(*box); q=mb(*box,p.size)
    o=Image.new('RGBA',(p.width*2+10,p.height),'white'); o.paste(p,(0,0)); o.paste(q,(p.width+10,0)); o.save(B+f'keuring_r4/zoom_{n}.png')
mm=M.crop((X0,Y0,xs.max()+1,ys.max()+1)); mm=mm.resize((64,round(mm.height/sc)),Image.LANCZOS)
one=Image.new('RGBA',(138,64),(232,238,232,255)); one.paste(S,(0,0)); one.paste(mm,(74,TOP))
one.save(B+'keuring_r4/vergelijk_1x.png'); one.resize((one.width*4,one.height*4),Image.NEAREST).save(B+'keuring_r4/vergelijk_1x_4x.png')
