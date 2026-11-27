# zoom.py x0 y0 x1 y1 out [Z]: natief (gekwantiseerd) uitsnede op Z-voud met coordinaten, naast het echte model
from PIL import Image, ImageDraw; import numpy as np, sys
D='docs/concept/sprites/hitmonchan_regional/'
x0,y0,x1,y1=map(int,sys.argv[1:5]); out=sys.argv[5]; Z=int(sys.argv[6]) if len(sys.argv)>6 else 24
nat=Image.open(D+'sprite/natief.png').convert('RGB')
m=Image.open(D+'gemini/r3.png').convert('RGB')
P=10.24;F=9.25;BX,BY=24,8
mc=m.crop((int(F+(x0+BX)*P),int(F+(y0+BY)*P),int(F+(x1+BX)*P),int(F+(y1+BY)*P))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
nc=nat.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
W=(x1-x0)*Z;H=(y1-y0)*Z
v=Image.new('RGB',(2*W+60,H+30),(255,255,255)); v.paste(nc,(30,30)); v.paste(mc,(W+60,30))
d=ImageDraw.Draw(v)
for i in range(x1-x0):
    d.text((30+i*Z+3,5),str(x0+i),fill=(200,0,0))
    d.line([(30+i*Z,30),(30+i*Z,30+H)],fill=(255,0,0))
for j in range(y1-y0):
    d.text((2,30+j*Z+3),str(y0+j),fill=(200,0,0))
    d.line([(30,30+j*Z),(30+W,30+j*Z)],fill=(255,0,0))
v.save(out)
