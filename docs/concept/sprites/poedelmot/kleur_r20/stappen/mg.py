import sys; sys.path.insert(0,'/home/user/pokemon-fully-ungrounded/docs/concept/sprites/poedelmot/kleur_r17/stappen')
from tl import *
X0,Y0,X1,Y1,z=map(int,sys.argv[1:6]); im=model(X0,Y0,X1,Y1,z); d=ImageDraw.Draw(im)
for i in range(X1-X0+1):
    d.line([(i*z,0),(i*z,im.height)],fill=(255,0,0) if (X0+i)%5==0 else (120,120,255)); d.text((i*z+2,2),str(X0+i),fill=(255,0,0))
for j in range(Y1-Y0+1):
    d.line([(0,j*z),(im.width,j*z)],fill=(255,0,0) if (Y0+j)%5==0 else (120,120,255)); d.text((2,j*z+2),str(Y0+j),fill=(255,0,0))
im.save(sys.argv[6])
