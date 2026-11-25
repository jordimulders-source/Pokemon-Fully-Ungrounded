# Toont een sprite (png of npy-labels) op 16x met rasterlijnen en coordinaten; optioneel naast het model op dezelfde schaal.
import sys, numpy as np
from PIL import Image, ImageDraw
src=sys.argv[1]; out=sys.argv[2]; Z=16
im=Image.open(src).convert('RGBA'); W,H=im.size
big=Image.new('RGBA',(W*Z+30,H*Z+30),(255,255,255,255))
big.paste(im.resize((W*Z,H*Z),Image.NEAREST),(30,30),im.resize((W*Z,H*Z),Image.NEAREST))
d=ImageDraw.Draw(big)
for x in range(W+1): d.line([(30+x*Z,30),(30+x*Z,30+H*Z)],fill=(200,200,200,255) if x%5 else (255,0,0,255))
for y in range(H+1): d.line([(30,30+y*Z),(30+W*Z,30+y*Z)],fill=(200,200,200,255) if y%5 else (255,0,0,255))
for x in range(0,W,5): d.text((30+x*Z+2,10),str(x),fill=(0,0,0,255))
for y in range(0,H,5): d.text((2,30+y*Z+2),str(y),fill=(0,0,0,255))
if len(sys.argv)>3:
    m=Image.open(sys.argv[3]).convert('RGBA')
    a=np.asarray(m.convert('RGB')).astype(int); fg=a.min(2)<225; ys,xs=np.nonzero(fg)
    x0,y0,y1=xs.min(),ys.min(),ys.max()+1; p=(y1-y0)/H
    c=m.crop((x0,y0,x0+int(W*p),y0+int(H*p))).resize((W*Z,H*Z),Image.LANCZOS)
    b2=Image.new('RGBA',(big.width*2,big.height),(255,255,255,255)); b2.paste(big,(0,0)); b2.paste(c,(big.width+30,30))
    d=ImageDraw.Draw(b2)
    for x in range(0,W+1,5): d.line([(big.width+30+x*Z,30),(big.width+30+x*Z,30+H*Z)],fill=(255,0,0,255))
    for y in range(0,H+1,5): d.line([(big.width+30,30+y*Z),(big.width+30+W*Z,30+y*Z)],fill=(255,0,0,255))
    big=b2
big.save(out)
