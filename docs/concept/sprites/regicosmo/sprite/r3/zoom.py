# Hulpmiddel: uitsnede van de sprite (12x) naast dezelfde uitsnede van het natieve model.  python3 zoom.py npy x0 y0 x1 y1 uit.png
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from PIL import Image; import pal, kaal as kl, gemeen as g
f,x0,y0,x1,y1,uit=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
k=np.load(f); Z=16
sp=pal.rgb(k).crop((x0,y0,x1,y1)); sp=sp.resize((sp.width*Z,sp.height*Z),0)
n=Image.open(os.path.join(g.D,'natief.png')).convert('RGB')
nx0=kl.X0+(x0-kl.OX)/kl.s; ny0=kl.Y0+(y0-kl.OY)/kl.s; nx1=kl.X0+(x1-kl.OX)/kl.s; ny1=kl.Y0+(y1-kl.OY)/kl.s
m=n.resize((n.width*8,n.height*8),0).crop((int(nx0*8),int(ny0*8),int(nx1*8),int(ny1*8))).resize(sp.size,0)
W=Image.new('RGB',(sp.width*2+10,sp.height),'white'); W.paste(sp,(0,0)); W.paste(m,(sp.width+10,0)); W.save(uit)
