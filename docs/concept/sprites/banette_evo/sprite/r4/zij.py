# python3 zij.py cur.npy x0 y0 x1 y1 out.png [z]: sprite (raster) | model, zelfde registratie
import sys,numpy as np; from PIL import Image,ImageDraw
from view import rgba
g=np.load(sys.argv[1]); x0,y0,x1,y1=[int(v) for v in sys.argv[2:6]]; out=sys.argv[6]; z=int(sys.argv[7]) if len(sys.argv)>7 else 16
S=968/62; m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
w,h=(x1-x0)*z,(y1-y0)*z
A=Image.alpha_composite(Image.new('RGBA',(64,64),(255,255,255,255)),rgba(g)).convert('RGB').crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST)
mb=(24+(x0-1)*S,1+(y0-4)*S,24+(x1-1)*S,1+(y1-4)*S)
B=mw.crop(tuple(int(round(v))+200 for v in mb)).resize((w,h),Image.LANCZOS)
c=Image.new('RGB',(2*w+30,h+20),'white'); c.paste(A,(20,20)); c.paste(B,(w+30,20)); d=ImageDraw.Draw(c)
for X in range(x0,x1+1):
    d.line([(20+(X-x0)*z,20),(20+(X-x0)*z,20+h)],fill=(200,200,255) if X%5 else (255,0,255)); d.line([(w+30+(X-x0)*z,20),(w+30+(X-x0)*z,20+h)],fill=(0,200,255) if X%5==0 else None) if X%5==0 else None
    if X%5==0: d.text((20+(X-x0)*z+1,2),str(X),fill=(0,0,0))
for Y in range(y0,y1+1):
    d.line([(20,20+(Y-y0)*z),(20+w,20+(Y-y0)*z)],fill=(255,0,255) if Y%5==0 else (200,200,255))
    if Y%5==0: d.text((0,20+(Y-y0)*z),str(Y),fill=(0,0,0)); d.line([(w+30,20+(Y-y0)*z),(2*w+30,20+(Y-y0)*z)],fill=(0,200,255))
c.save(out)
