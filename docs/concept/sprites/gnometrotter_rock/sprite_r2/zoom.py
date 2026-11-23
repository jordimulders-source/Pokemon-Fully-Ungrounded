# zoom.py sprite.png x0 y0 x1 y1 [uit.png] -> sprite-uitsnede | model op schaal, 12x met raster
import sys; sys.path.insert(0,'../sprite')
from PIL import Image, ImageDraw
from kijk import sprite, model_op_schaal
p=sys.argv[1]; x0,y0,x1,y1=map(int,sys.argv[2:6]); uit=sys.argv[6] if len(sys.argv)>6 else 'zoom.png'; z=12
s=sprite(p,(255,255,255)).crop((x0,y0,x1,y1)); m=model_op_schaal(n=64*z).crop((x0*z,y0*z,x1*z,y1*z))
w,h=(x1-x0)*z,(y1-y0)*z; W=Image.new('RGB',(2*w+10,h),'white'); W.paste(s.resize((w,h),Image.NEAREST),(0,0)); W.paste(m,(w+10,0))
d=ImageDraw.Draw(W)
for i in range(x1-x0+1):
    for off in (0,w+10): d.line([(off+i*z,0),(off+i*z,h)],fill=(200,200,255) if (x0+i)%5 else (255,120,120))
for j in range(y1-y0+1):
    for off in (0,w+10): d.line([(off,j*z),(off+w,j*z)],fill=(200,200,255) if (y0+j)%5 else (255,120,120))
W.save(uit)
