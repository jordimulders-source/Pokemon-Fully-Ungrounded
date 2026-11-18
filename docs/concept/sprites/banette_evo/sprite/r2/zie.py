# Werkvel: sprite (rooster+coord) | model (zelfde rooster): python3 zie.py npy x0 y0 x1 y1 out [z]
import sys,numpy as np; from PIL import Image, ImageDraw
from view import rgba
g=np.load(sys.argv[1]); x0,y0,x1,y1=[int(v) for v in sys.argv[2:6]]; out=sys.argv[6]; z=int(sys.argv[7]) if len(sys.argv)>7 else 24
S=968/62; m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
W,H=(x1-x0)*z,(y1-y0)*z
mb=(24+(x0-1)*S,1+(y0-4)*S,24+(x1-1)*S,1+(y1-4)*S)
B=mw.crop(tuple(int(round(v))+200 for v in mb)).resize((W,H),Image.LANCZOS)
sp=rgba(g).crop((x0,y0,x1,y1)); bg=Image.new('RGBA',sp.size,(255,255,255,255)); A=Image.alpha_composite(bg,sp).convert('RGB').resize((W,H),Image.NEAREST)
c=Image.new('RGB',(2*W+60,H+20),'white'); c.paste(A,(30,20)); c.paste(B,(W+60,20)); d=ImageDraw.Draw(c)
for ox in (30,W+60):
  for i in range(x1-x0+1):
    d.line([(ox+i*z,20),(ox+i*z,20+H)],fill=(0,200,255))
    if i<x1-x0: d.text((ox+i*z+2,4+(i%2)*8),str(x0+i),fill=(0,0,0))
  for j in range(y1-y0+1):
    d.line([(ox,20+j*z),(ox+W,20+j*z)],fill=(0,200,255))
    if j<y1-y0: d.text((ox-28,20+j*z+z//3),str(y0+j),fill=(0,0,0))
c.save(out)
