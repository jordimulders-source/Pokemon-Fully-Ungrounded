# rooster.py x0 y0 x1 y1 out [sprite.png]: natief model met het spriteraster erover (spritecoordinaten), 10 px per natieve cel;
# met sprite.png: de sprite op dezelfde schaal ernaast.
import sys; sys.path.insert(0,'sprite_r5'); from gemeen2 import *
from PIL import Image, ImageDraw; import numpy as np
x0,y0,x1,y1=map(int,sys.argv[1:5]); out=sys.argv[5]; z=10
N=Image.open(NATIEF).convert('RGB')
ua=(x0-X0)/S+U0; va=(y0-Y0)/S+V0; ub=(x1-X0)/S+U0; vb=(y1-Y0)/S+V0
c=N.crop((int(ua),int(va),int(np.ceil(ub)),int(np.ceil(vb)))); ox,oy=int(ua),int(va)
im=c.resize((c.width*z,c.height*z),Image.NEAREST); d=ImageDraw.Draw(im)
for X in range(x0,x1+1):
    px=((X-X0)/S+U0-ox)*z; d.line([(px,0),(px,im.height)],fill=(0,140,255))
    if X<x1: d.text((px+3,2),str(X),fill=(0,0,200))
for Y in range(y0,y1+1):
    py=((Y-Y0)/S+V0-oy)*z; d.line([(0,py),(im.width,py)],fill=(0,140,255))
    if Y<y1: d.text((2,py+3),str(Y),fill=(0,0,200))
if len(sys.argv)>6:
    o=np.array(Image.open(sys.argv[6])); s=rgb(o,(255,255,255)).crop((x0,y0,x1,y1))
    zz=z/S; s=s.resize((int((x1-x0)*zz),int((y1-y0)*zz)),Image.NEAREST)
    t=Image.new('RGB',(im.width+s.width+20,max(im.height,s.height)),'white'); t.paste(im,(0,0)); t.paste(s,(im.width+20,0)); im=t
im.save(out)
