# python3 kijk.py out x0 y0 x1 y1 z npy1 [npy2 ...] -> sprites (zonder raster) naast elkaar + model
import sys,numpy as np; from PIL import Image
from view import rgba
out=sys.argv[1]; x0,y0,x1,y1,z=[int(v) for v in sys.argv[2:7]]; fs=sys.argv[7:]
S=968/62; m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
w,h=(x1-x0)*z,(y1-y0)*z; parts=[]
for f in fs:
    im=rgba(np.load(f)).crop((x0,y0,x1,y1)); b=Image.new('RGBA',im.size,(255,255,255,255)); parts.append(Image.alpha_composite(b,im).convert('RGB').resize((w,h),Image.NEAREST))
mb=(24+(x0-1)*S,1+(y0-4)*S,24+(x1-1)*S,1+(y1-4)*S); parts.append(mw.crop(tuple(int(round(v))+200 for v in mb)).resize((w,h),Image.LANCZOS))
c=Image.new('RGB',(len(parts)*(w+10),h),'white')
for k,p in enumerate(parts): c.paste(p,(k*(w+10),0))
c.save(out)
