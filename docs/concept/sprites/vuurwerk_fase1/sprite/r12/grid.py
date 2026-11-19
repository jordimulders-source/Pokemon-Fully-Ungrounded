# Uitsnede model met spritegrid (F=2.4 ox=76.6 oy=14.6, sprite-offset rij 1, kol 17) naast sprite op zelfde schaal
import sys,numpy as np; from PIL import Image, ImageDraw
F,OX,OY=2.4,76.6,14.6; S=5.12
M=Image.open('../../referenties/model.png').convert('RGB')
r0,r1,c0,c1=map(int,sys.argv[1:5]); src=sys.argv[5]; out=sys.argv[6]; Z=int(sys.argv[7]) if len(sys.argv)>7 else 24
# r,c in 64x64-coordinaten
X=lambda c:((OX+F*(c-17))*S-0.42); Y=lambda r:((OY+F*(r-1))*S-0.42)
crop=M.crop((int(X(c0)),int(Y(r0)),int(X(c1)),int(Y(r1)))).resize(((c1-c0)*Z,(r1-r0)*Z),Image.LANCZOS)
d=ImageDraw.Draw(crop)
for c in range(c0,c1+1): d.line([((c-c0)*Z,0),((c-c0)*Z,(r1-r0)*Z)],fill=(0,160,255) if c%5 else (0,0,255))
for r in range(r0,r1+1): d.line([(0,(r-r0)*Z),((c1-c0)*Z,(r-r0)*Z)],fill=(0,160,255) if r%5 else (0,0,255))
sp=Image.open(src).convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(sp)
sc=bg.crop((c0,r0,c1,r1)).resize(((c1-c0)*Z,(r1-r0)*Z),Image.NEAREST).convert('RGB')
d2=ImageDraw.Draw(sc)
for c in range(c0,c1+1): d2.line([((c-c0)*Z,0),((c-c0)*Z,(r1-r0)*Z)],fill=(0,160,255) if c%5 else (0,0,255))
for r in range(r0,r1+1): d2.line([(0,(r-r0)*Z),((c1-c0)*Z,(r-r0)*Z)],fill=(0,160,255) if r%5 else (0,0,255))
W=Image.new('RGB',(crop.width*2+10,crop.height),'white'); W.paste(crop,(0,0)); W.paste(sc,(crop.width+10,0)); W.save(out)
