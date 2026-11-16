import sys
from PIL import Image, ImageDraw; import numpy as np
X0,Y0,X1,Y1=[int(v) for v in sys.argv[1:5]]; out=sys.argv[5]; S=int(sys.argv[6]) if len(sys.argv)>6 else 16
nat=Image.open('sprite_r2/natief.png').convert('RGB')
sp=Image.open(sys.argv[7] if len(sys.argv)>7 else 'sprite_r2/pitahaya_r2.png').convert('RGBA')
base=Image.new('RGBA',(64,64),(255,255,255,255)); base.alpha_composite(sp)
A=base.crop((X0,Y0,X1,Y1)).resize(((X1-X0)*S,(Y1-Y0)*S),Image.NEAREST).convert('RGB')
# natief region: col=1+3*(x+1), row=3*(y+2)
c0=1+3*(X0+1); r0=3*(Y0+2)
B=nat.crop((c0,r0,c0+3*(X1-X0),r0+3*(Y1-Y0))).resize(A.size,Image.NEAREST)
W=Image.new('RGB',(A.width*2+10,A.height),(120,120,120)); W.paste(A,(0,0)); W.paste(B,(A.width+10,0))
d=ImageDraw.Draw(W)
for off in (0,A.width+10):
  for i in range(X1-X0+1): d.line([(off+i*S,0),(off+i*S,A.height)],fill=(0,0,0))
  for j in range(Y1-Y0+1): d.line([(off,j*S),(off+A.width,j*S)],fill=(0,0,0))
  for i in range(X0,X1):
    if i%2==0: d.text((off+(i-X0)*S+2,2),str(i),fill=(0,0,255))
  for j in range(Y0,Y1):
    if j%2==0: d.text((off+2,(j-Y0)*S+2),str(j),fill=(0,0,255))
W.save(out)
