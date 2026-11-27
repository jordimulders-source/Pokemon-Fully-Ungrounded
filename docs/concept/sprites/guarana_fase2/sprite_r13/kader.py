# kader.py SPRITE: rechte stukken donker (lijnrood/zwart) >= 3 px, horizontaal of verticaal, die oogwit raken, per oogvak
import sys; sys.path.insert(0,'sprite_r9'); sys.path.insert(0,'sprite_r13'); import numpy as np; from PIL import Image; from hulp import *
from bouw13 import OGEN
o=np.array(Image.open(sys.argv[1])).astype(int)
def raakt_wit(x,y): return any(ok(y+dy,x+dx) and o[y+dy,x+dx] in (10,11) for dy,dx in N8)
for n,(x0,y0),T in OGEN:
    uit=[]
    for y in range(y0-1,y0+len(T)+1):
        run=[]
        for x in range(x0-1,x0+len(T[0])+2):
            if ok(y,x) and o[y,x] in (1,2) and raakt_wit(x,y): run.append(x)
            else:
                if len(run)>=3: uit.append(('rij',y,run[0],run[-1]))
                run=[]
    for x in range(x0-1,x0+len(T[0])+1):
        run=[]
        for y in range(y0-1,y0+len(T)+2):
            if ok(y,x) and o[y,x] in (1,2) and raakt_wit(x,y): run.append(y)
            else:
                if len(run)>=3: uit.append(('kol',x,run[0],run[-1]))
                run=[]
    print(n,uit)
