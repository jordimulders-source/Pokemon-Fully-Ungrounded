# zone view: python3 zv.py npy x0 y0 x1 y1 out [z]  -> sprite 12x | model with grid
import sys,numpy as np; from PIL import Image,ImageDraw
from view import rgba
g=np.load(sys.argv[1]); x0,y0,x1,y1=[int(v) for v in sys.argv[2:6]]; out=sys.argv[6]; z=int(sys.argv[7]) if len(sys.argv)>7 else 12
S=968/62; m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
w,h=(x1-x0)*z,(y1-y0)*z
im=rgba(g).crop((x0,y0,x1,y1)); b=Image.new('RGBA',im.size,(255,255,255,255)); A=Image.alpha_composite(b,im).convert('RGB').resize((w,h),Image.NEAREST)
mb=(24+(x0-1)*S,1+(y0-4)*S,24+(x1-1)*S,1+(y1-4)*S); B=mw.crop(tuple(int(round(v))+200 for v in mb)).resize((w,h),Image.LANCZOS)
c=Image.new('RGB',(2*w+50,h+30),'white'); c.paste(A,(30,20)); c.paste(B,(w+50,20)); d=ImageDraw.Draw(c)
for X in range(x0,x1+1):
    for off in (30,w+50):
        px=off+(X-x0)*z; d.line([(px,20),(px,20+h)],fill=(150,200,255) if X%5 else (255,0,255))
    d.text((30+(X-x0)*z+2,4),str(X%100),fill=(0,0,0))
for Y in range(y0,y1+1):
    for off in (30,w+50):
        py=20+(Y-y0)*z; d.line([(off,py),(off+w,py)],fill=(150,200,255) if Y%5 else (255,0,255))
    d.text((2,20+(Y-y0)*z+2),str(Y),fill=(0,0,0))
c.save(out)
