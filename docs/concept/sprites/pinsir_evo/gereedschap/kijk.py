# kijk.py SPRITE.png UIT.png x0 y0 x1 y1 [z]: zone van de sprite naast het model met spriteraster (grote close-up met coördinaten)
import sys; sys.path.insert(0,'gereedschap')
from PIL import Image, ImageDraw; import numpy as np
from vel import rgbp, model_crop
x0,y0,x1,y1=map(int,sys.argv[3:7]); z=int(sys.argv[7]) if len(sys.argv)>7 else 20
A=rgbp(sys.argv[1]).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); B=model_crop(x0,y0,x1,y1,z)
W=A.width; H=A.height; v=Image.new('RGB',(2*W+40,H+30),'white'); v.paste(A,(30,20)); v.paste(B,(W+40,20))
g=np.asarray(v).copy()
for off in (30,W+40):
    for x in range(0,W+1,z): g[20:20+H,min(off+x,g.shape[1]-1)]=(g[20:20+H,min(off+x,g.shape[1]-1)]*0.6+np.array((60,140,255))*0.4).astype('uint8')
    for y in range(0,H+1,z): g[min(20+y,g.shape[0]-1),off:off+W]=(g[min(20+y,g.shape[0]-1),off:off+W]*0.6+np.array((60,140,255))*0.4).astype('uint8')
v=Image.fromarray(g); d=ImageDraw.Draw(v)
for i,x in enumerate(range(x0,x1)): d.text((30+i*z+2,4),str(x%100),fill=(0,0,0)); d.text((W+40+i*z+2,4),str(x%100),fill=(0,0,0))
for j,y in enumerate(range(y0,y1)): d.text((2,20+j*z+2),str(y),fill=(0,0,0))
v.save(sys.argv[2]); print(sys.argv[2],v.size)
