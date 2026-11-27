# zoom.py a.png b.png x0 y0 x1 y1 z out : a | b | model (zelfde vak), met coordinaten
import sys; sys.path.insert(0,'sprite/r1'); import meet
from PIL import Image, ImageDraw
a,b=sys.argv[1:3]; x0,y0,x1,y1,z=map(int,sys.argv[3:8]); out=sys.argv[8]
w,h=(x1-x0)*z,(y1-y0)*z
o=Image.new('RGB',(3*w+40,h+14),'white'); d=ImageDraw.Draw(o)
for i,p in enumerate([a,b]): o.paste(meet.rgba(p).crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(i*(w+20),14))
o.paste(meet.model_crop(x0,y0,x1,y1,z),(2*(w+20),14))
for k in range(3):
    for i in range(x1-x0):
        if (x0+i)%5==0: d.text((k*(w+20)+i*z+1,0),str(x0+i),fill='red')
    for j in range(y1-y0):
        if (y0+j)%5==0: d.text((k*(w+20)+1,14+j*z+1),str(y0+j),fill='red')
o.save(out)
