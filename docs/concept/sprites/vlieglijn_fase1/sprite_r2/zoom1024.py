# 1024-model met spriteraster (S=1.6 natief) voor cellen i0..i1, j0..j1. python3 zoom1024.py i0 i1 j0 j1 UIT.png
from PIL import Image, ImageDraw; import sys
i0,i1,j0,j1=map(int,sys.argv[1:5]); F=3
S=1.6*10.24; X0=17*10.24; Y0=20*10.24
im=Image.open('../model/model.png').convert('RGB')
bx0=int(X0+i0*S); by0=int(Y0+j0*S); bx1=int(X0+i1*S); by1=int(Y0+j1*S)
c=im.crop((bx0,by0,bx1,by1)).resize(((bx1-bx0)*F,(by1-by0)*F),Image.NEAREST); d=ImageDraw.Draw(c)
for i in range(i0,i1+1):
  x=(X0+i*S-bx0)*F; d.line([(x,0),(x,c.size[1])],fill=(255,0,0))
for j in range(j0,j1+1):
  y=(Y0+j*S-by0)*F; d.line([(0,y),(c.size[0],y)],fill=(255,0,0))
for i in range(i0,i1):
  for j in range(j0,j1): d.text(((X0+i*S-bx0)*F+2,(Y0+j*S-by0)*F+2),'%d,%d'%(i,j),fill=(255,0,200))
c.save(sys.argv[5])
