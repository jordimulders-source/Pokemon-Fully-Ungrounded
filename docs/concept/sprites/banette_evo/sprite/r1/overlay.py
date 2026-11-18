# Model (raster, NEAREST) met de spritepixels half-transparant erover: python3 overlay.py cur.npy x0 y0 x1 y1 out [z]
import sys,numpy as np; from PIL import Image, ImageDraw
from pal import PAL
g=np.load(sys.argv[1]); x0,y0,x1,y1=[int(v) for v in sys.argv[2:6]]; out=sys.argv[6]; z=int(sys.argv[7]) if len(sys.argv)>7 else 24
S=968/62; m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
mb=(24+(x0-1)*S,1+(y0-4)*S,24+(x1-1)*S,1+(y1-4)*S); W,H=(x1-x0)*z,(y1-y0)*z
B=mw.crop(tuple(int(round(v))+200 for v in mb)).resize((W,H),Image.NEAREST).convert('RGBA')
O=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(O)
for j in range(y0,y1):
    for i in range(x0,x1):
        v=g[j,i]
        if v: 
            c=PAL[v]; d.rectangle([(i-x0)*z+z//4,(j-y0)*z+z//4,(i-x0)*z+3*z//4,(j-y0)*z+3*z//4],fill=c+(255,))
for i in range(x1-x0+1): d.line([(i*z,0),(i*z,H)],fill=(0,200,255,120))
for j in range(y1-y0+1): d.line([(0,j*z),(W,j*z)],fill=(0,200,255,120))
Image.alpha_composite(B,O).convert('RGB').save(out)
