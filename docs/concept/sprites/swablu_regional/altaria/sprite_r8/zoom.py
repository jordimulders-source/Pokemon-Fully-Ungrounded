# zoom.py: close-up sprite (16x) naast het natieve model op dezelfde schaal. python3 sprite_r8/zoom.py sprite.png X0 Y0 X1 Y1 uit.png
import sys; sys.path.insert(0,'gereedschap'); sys.path.insert(0,'sprite_r5')
from PIL import Image; import basis as B, numpy as np
p,X0,Y0,X1,Y1,uit=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
Z=16
im=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',(64,64),'white'); bg.alpha_composite(im)
s=bg.crop((X0,Y0,X1,Y1)).resize(((X1-X0)*Z,(Y1-Y0)*Z),Image.NEAREST)
u0,v0=B.blok(X0,Y0); u1,v1=B.blok(X1,Y1)
m=Image.fromarray(B.a.astype('uint8')).crop((u0,v0,u1,v1)).resize(s.size,Image.NEAREST)
out=Image.new('RGB',(s.width*2+8,s.height),'white'); out.paste(s.convert('RGB'),(0,0)); out.paste(m,(s.width+8,0))
from PIL import ImageDraw; d=ImageDraw.Draw(out)
for X in range(X0,X1):
    if X%5==0: d.text(((X-X0)*Z+2,2),str(X),fill=(255,0,0))
for Y in range(Y0,Y1):
    if Y%5==0: d.text((2,(Y-Y0)*Z+2),str(Y),fill=(255,0,0))
out.save(uit)
