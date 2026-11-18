# snelle vergelijking: python3 kijk.py npy x0 y0 x1 y1 out z  -> sprite | r2 | model (zelfde registratie)
import sys,numpy as np; from PIL import Image
from view import rgba
g=np.load(sys.argv[1]); x0,y0,x1,y1=[int(v) for v in sys.argv[2:6]]; out=sys.argv[6]; z=int(sys.argv[7])
S=968/62; m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
W,H=(x1-x0)*z,(y1-y0)*z
def sp(G):
    im=rgba(G).crop((x0,y0,x1,y1)); b=Image.new('RGBA',im.size,(255,255,255,255)); return Image.alpha_composite(b,im).convert('RGB').resize((W,H),Image.NEAREST)
B=mw.crop(tuple(int(round(v))+200 for v in (24+(x0-1)*S,1+(y0-4)*S,24+(x1-1)*S,1+(y1-4)*S))).resize((W,H),Image.LANCZOS)
c=Image.new('RGB',(3*W+20,H),'white'); c.paste(sp(g),(0,0)); c.paste(sp(np.load('r2.npy')),(W+10,0)); c.paste(B,(2*W+20,0)); c.save(out)
