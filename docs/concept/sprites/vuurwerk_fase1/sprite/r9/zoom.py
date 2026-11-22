# zone: sprite (links) | model (rechts) op dezelfde schaal, met spritegrid en coordinaten. src: model | natief.png | natief_q.png
import sys,numpy as np; from PIL import Image, ImageDraw
from reduce2 import PAL
F,OX,OY=2.4,76.6,14.6
a=np.load(sys.argv[1]); c0,c1,r0,r1=map(int,sys.argv[3:7]); src=sys.argv[7] if len(sys.argv)>7 else 'model'; Z=int(sys.argv[8]) if len(sys.argv)>8 else 24
def rgbidx(idx):
    out=PAL[idx].astype('uint8').copy(); out[idx==0]=255; return out
A=Image.fromarray(rgbidx(a[r0:r1,c0:c1])).resize(((c1-c0)*Z,(r1-r0)*Z),Image.NEAREST)
fx=lambda v:(OX+F*v)*5.12-0.42; fy=lambda v:(OY+F*v)*5.12-0.42
if src=='model':
    M=Image.open('../../referenties/model.png').convert('RGB')
    B=M.crop((round(fx(c0)),round(fy(r0)),round(fx(c1)),round(fy(r1)))).resize(A.size,Image.LANCZOS)
    if len(sys.argv)>9:
        x=np.asarray(B).astype(float); B=Image.fromarray(np.clip((x-150)*2.5,0,255).astype('uint8'))
else:
    N=Image.open(src).convert('RGB'); B=N.crop((OX+F*c0,OY+F*r0,OX+F*c1,OY+F*r1)) if False else N.transform(A.size,Image.EXTENT,(OX+F*c0,OY+F*r0,OX+F*c1,OY+F*r1),Image.NEAREST)
for im in (A,B):
    d=ImageDraw.Draw(im)
    for x in range(c1-c0+1): d.line([(x*Z,0),(x*Z,im.height)],fill=(150,150,150))
    for y in range(r1-r0+1): d.line([(0,y*Z),(im.width,y*Z)],fill=(150,150,150))
    for x in range(c0,c1): d.text(((x-c0)*Z+2,1),str(x),fill=(0,0,255))
    for y in range(r0,r1): d.text((1,(y-r0)*Z+12),str(y),fill=(0,140,0))
S=Image.new('RGB',(A.width*2+10,A.height),'white'); S.paste(A,(0,0)); S.paste(B,(A.width+10,0)); S.save(sys.argv[2])
