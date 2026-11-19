# zone: sprite (links, 24x) | model natief (rechts, 8x natief = 24 per spritepixel), met spritegrid en coordinaten
import sys,numpy as np; from PIL import Image, ImageDraw
from reduce2 import PAL
a=np.load(sys.argv[1]); c0,c1,r0,r1=map(int,sys.argv[3:7]); src=sys.argv[7] if len(sys.argv)>7 else 'natief.png'
OX,OY=76,14; Z=int(sys.argv[8]) if len(sys.argv)>8 else 24
def rgbidx(idx):
    out=PAL[idx].astype('uint8').copy(); out[idx==0]=255; return out
A=Image.fromarray(rgbidx(a[r0:r1,c0:c1])).resize(((c1-c0)*Z,(r1-r0)*Z),Image.NEAREST)
if src=='model':
    M=Image.open('../../referenties/model.png').convert('RGB'); f=lambda v,o: (o+3*v)*5.12-0.42
    B=M.crop((round(f(c0,OX)),round(f(r0,OY)),round(f(c1,OX)),round(f(r1,OY)))).resize(((c1-c0)*Z,(r1-r0)*Z),Image.LANCZOS)
else:
    n=np.asarray(Image.open(src).convert('RGB'))[OY+3*r0:OY+3*r1, OX+3*c0:OX+3*c1]
    B=Image.fromarray(n).resize(((c1-c0)*Z,(r1-r0)*Z),Image.NEAREST)
for im in (A,B):
    d=ImageDraw.Draw(im)
    for x in range(c1-c0+1): d.line([(x*Z,0),(x*Z,im.height)],fill=(150,150,150))
    for y in range(r1-r0+1): d.line([(0,y*Z),(im.width,y*Z)],fill=(150,150,150))
    for x in range(c0,c1): d.text(((x-c0)*Z+2,1),str(x),fill=(0,0,255))
    for y in range(r0,r1): d.text((1,(y-r0)*Z+12),str(y),fill=(0,140,0))
S=Image.new('RGB',(A.width*2+10,A.height),'white'); S.paste(A,(0,0)); S.paste(B,(A.width+10,0)); S.save(sys.argv[2])
