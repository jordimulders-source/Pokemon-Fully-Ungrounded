# zoom.py sprite.png x0 y0 x1 y1 [schaal] -> zoom.png: uitsnede van sprite en model (op schaal) naast elkaar, met raster en coordinaten
import sys; from PIL import Image, ImageDraw
from kijk import sprite, model_op_schaal
p=sys.argv[1]; x0,y0,x1,y1=map(int,sys.argv[2:6]); k=int(sys.argv[6]) if len(sys.argv)>6 else 12
ims=[sprite(p).crop((x0,y0,x1,y1)),model_op_schaal().crop((x0,y0,x1,y1))]
w,h=(x1-x0)*k,(y1-y0)*k
W=Image.new('RGB',(2*w+30,h+20),'white'); d=ImageDraw.Draw(W)
for i,im in enumerate(ims):
    W.paste(im.resize((w,h),Image.NEAREST),(i*(w+30)+20,20))
    for X in range(x0,x1+1):
        xx=i*(w+30)+20+(X-x0)*k; d.line([(xx,20),(xx,20+h)],fill=(200,200,200))
        if X%2==0 and X<x1: d.text((xx+1,2),str(X),fill=(0,0,0))
    for Y in range(y0,y1+1):
        yy=20+(Y-y0)*k; d.line([(i*(w+30)+20,yy),(i*(w+30)+20+w,yy)],fill=(200,200,200))
        if i==0 and Y<y1: d.text((0,yy+2),str(Y),fill=(0,0,0))
W.save('zoom.png')
