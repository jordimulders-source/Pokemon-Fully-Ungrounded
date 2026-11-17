import sys,numpy as np
from PIL import Image; from tekstraster import *; from lijf import per_pixel; from ribben import ribkaart; from lijf4 import lijf
import subprocess
basis=sys.argv[1]; o0=lees(basis); pal=Image.open(basis).getpalette()
V=per_pixel(); U=np.zeros((64,64),bool); U[33:46,0:22]=True; U[43:49,28:37]=True
outs=[]
for i,(lm,lu,mr) in enumerate([(14,85,3),(20,85,4),(25,80,4),(30,85,5)]):
    o2,Z=lijf(o0.copy(),V,ribkaart(lm,lu)[0],U,minrib=mr); p='/tmp/claude-0/s/q%d.png'%i; schrijf(o2,pal,p); outs.append(p)
subprocess.run(['python3','klein.py','6','/tmp/claude-0/s/kq.png']+outs)
