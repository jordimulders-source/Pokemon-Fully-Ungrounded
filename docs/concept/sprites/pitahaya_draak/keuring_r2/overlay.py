import sys; sys.path.insert(0,'sprite_r1')
from PIL import Image, ImageDraw; import numpy as np
from groepen import laad
a,lum,g=laad('sprite_r2/natief.png')
sp=Image.open('sprite_r2/pitahaya_r2.png').convert('RGBA')
S=8; X0,Y0,X1,Y1=14,5,48,57
base=Image.new('RGBA',(64,64),(255,255,255,255)); base.alpha_composite(sp)
big=base.crop((X0,Y0,X1,Y1)).resize(((X1-X0)*S,(Y1-Y0)*S),Image.NEAREST)
# fade
big=Image.blend(big,Image.new('RGBA',big.size,(255,255,255,255)),0.35)
d=ImageDraw.Draw(big)
dark=(lum<85)&(g!=0)
H,W=g.shape
for r in range(H):
  for c in range(W):
    if dark[r,c]:
      x=((c-1)/3-1-X0)*S; y=(r/3-2-Y0)*S
      d.rectangle([x,y,x+S/3-1,y+S/3-1],fill=(0,120,255,255))
# grid
for i in range(X1-X0+1): d.line([(i*S,0),(i*S,big.height)],fill=(0,0,0,40))
for j in range(Y1-Y0+1): d.line([(0,j*S),(big.width,j*S)],fill=(0,0,0,40))
for i in range(X0,X1,5): d.text(((i-X0)*S+1,1),str(i),fill=(255,0,0,255))
for j in range(Y0,Y1,5): d.text((1,(j-Y0)*S+1),str(j),fill=(255,0,0,255))
big.save('keuring_r2/lijnoverlay.png')
