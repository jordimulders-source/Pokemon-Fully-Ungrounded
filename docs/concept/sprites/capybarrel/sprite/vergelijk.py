# vergelijk.py sprite.png x0 y0 w h uit.png : model (met spritecelraster) | sprite, zelfde schaal (24x), coördinaten = spritepixels
import sys, numpy as np
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/'
sp=Image.open(sys.argv[1]).convert('RGBA'); x0,y0,w,h=map(int,sys.argv[2:6])
# sprite-figuur zit in kaal.png-coördinaten (46 breed, 34 hoog); r1-png's zijn 64x64 met offset
OX,OY=(0,0) if sp.size==(46,34) else (int(sys.argv[7]),int(sys.argv[8]))
S=int(sys.argv[9]) if len(sys.argv)>9 else 24; p=738/46; mx0=143; my1=799; H=34
m=Image.open(R+'referenties/model_r3.png').convert('RGB')
box=(mx0+x0*p, my1-(H-y0)*p, mx0+(x0+w)*p, my1-(H-y0-h)*p)
mc=m.crop(tuple(int(round(v)) for v in box)).resize((w*S,h*S),Image.LANCZOS)
d=ImageDraw.Draw(mc)
for k in range(w+1): d.line([(k*S,0),(k*S,h*S)],fill=(0,200,255))
for k in range(h+1): d.line([(0,k*S),(w*S,k*S)],fill=(0,200,255))
bg=Image.new('RGBA',sp.size,(235,235,235,255)); bg.alpha_composite(sp)
sc=bg.convert('RGB').crop((x0+OX,y0+OY,x0+OX+w,y0+OY+h)).resize((w*S,h*S),Image.NEAREST)
d2=ImageDraw.Draw(sc)
for k in range(w+1): d2.line([(k*S,0),(k*S,h*S)],fill=(180,180,180))
for k in range(h+1): d2.line([(0,k*S),(w*S,k*S)],fill=(180,180,180))
W=Image.new('RGB',(2*w*S+60,h*S+30),(255,255,255)); dw=ImageDraw.Draw(W)
W.paste(mc,(30,30)); W.paste(sc,(w*S+60,30))
for k in range(w): dw.text((30+k*S+6,14),str(x0+k),fill=(0,0,200)); dw.text((w*S+60+k*S+6,14),str(x0+k),fill=(0,0,200))
for k in range(h): dw.text((4,30+k*S+6),str(y0+k),fill=(0,0,200))
W.save(sys.argv[6])
