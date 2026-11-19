# Lijnkaart: model (1024) uitsnede op spriteraster, met de zwarte spritepixels als rood kadertje erover.
# python3 overlay.py f.npy x0 y0 x1 y1 s out
import sys; import numpy as np; from PIL import Image, ImageDraw
f=sys.argv[1]; x0,y0,x1,y1,s=map(int,sys.argv[2:7]); out=sys.argv[7]
o=np.load(f); OY,OX=1,4; S=15.36
im=Image.open('../../gemini/r9_prompt_v6.png').convert('RGB')
c=im.crop((int(OX*5.12+x0*S),int(OY*5.12+y0*S),int(OX*5.12+x1*S),int(OY*5.12+y1*S))).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST)
d=ImageDraw.Draw(c)
for x in range(x0,x1):
    for y in range(y0,y1):
        X,Y=(x-x0)*s,(y-y0)*s
        d.rectangle([X,Y,X+s-1,Y+s-1],outline=(225,225,240))
        if o[y,x]==1: d.rectangle([X+2,Y+2,X+s-3,Y+s-3],outline=(255,0,0),width=2)
for x in range(x0,x1,2): d.text(((x-x0)*s+2,0),str(x%100),fill=(0,0,255))
for y in range(y0,y1,2): d.text((0,(y-y0)*s+2),str(y),fill=(0,0,255))
c.save(out)
