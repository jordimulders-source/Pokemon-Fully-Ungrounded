# python3 cmp.py npy out x0 y0 x1 y1 z : sprite z x | model z x (geen grid) + hele sprite 1x/2x naast model 1x/2x
import sys,numpy as np; from PIL import Image
from view import rgba
g=np.load(sys.argv[1]); out=sys.argv[2]; x0,y0,x1,y1,z=[int(v) for v in sys.argv[3:8]]
S=968/62; m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
def mb(x0,y0,x1,y1,w,h,f=Image.LANCZOS):
    b=(24+(x0-1)*S,1+(y0-4)*S,24+(x1-1)*S,1+(y1-4)*S); return mw.crop(tuple(int(round(v))+200 for v in b)).resize((w,h),f)
def sp(x0,y0,x1,y1,z):
    im=rgba(g).crop((x0,y0,x1,y1)); b=Image.new('RGBA',im.size,(255,255,255,255)); return Image.alpha_composite(b,im).convert('RGB').resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
w,h=(x1-x0)*z,(y1-y0)*z
c=Image.new('RGB',(2*w+20+300,max(h,140)),'white'); c.paste(sp(x0,y0,x1,y1,z),(0,0)); c.paste(mb(x0,y0,x1,y1,w,h),(w+10,0))
c.paste(sp(0,0,64,64,1),(2*w+20,0)); c.paste(mb(0,0,64,64,64,64,Image.BOX),(2*w+90,0))
c.paste(sp(0,0,64,64,2),(2*w+20,70)) if 2*w+20+128<=c.width else None
c.save(out)
