# Overlay: model op 8x met de spritepixels als contour (figuurgrens rood, zwarte spritepixels als blauwe puntjes, lichte randpixels geel)
import numpy as np, sys; from PIL import Image, ImageDraw
S=11.87; X0=138-0.5*S; Y0=107-1.2*S; z=8
o=np.load(sys.argv[1])
m=Image.open('../../referenties/model.png').convert('RGBA').crop((int(X0),int(Y0),int(X0+64*S),int(Y0+64*S))).resize((512,512),Image.LANCZOS)
d=ImageDraw.Draw(m)
fig=o>0
for j in range(64):
    for i in range(64):
        if not fig[j,i]: continue
        for (dj,di,ln) in [(-1,0,((i*z,j*z),(i*z+z,j*z))),(1,0,((i*z,j*z+z),(i*z+z,j*z+z))),(0,-1,((i*z,j*z),(i*z,j*z+z))),(0,1,((i*z+z,j*z),(i*z+z,j*z+z)))]:
            y,x=j+dj,i+di
            if not(0<=y<64 and 0<=x<64) or not fig[y,x]: d.line(ln,fill=(255,0,0,255),width=1)
        if o[j,i]==1: d.point((i*z+4,j*z+4),fill=(0,120,255,255))
        if o[j,i] in (5,6): d.rectangle((i*z+3,j*z+3,i*z+5,j*z+5),outline=(255,160,0,255))
m.save(sys.argv[2])
