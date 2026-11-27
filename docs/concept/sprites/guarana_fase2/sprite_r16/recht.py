# recht.py SPRITE: rechte stukken >= 3 px op de buitenrand van de trossen (randpixels rood/zwart/wit die aan achtergrond grenzen,
# in dezelfde rij met de achtergrond aan dezelfde kant), per tros
import sys; sys.path.insert(0,'sprite_r9'); sys.path.insert(0,'sprite_r16'); import numpy as np; from PIL import Image; from hulp import *
import bouw16 as B
o=np.array(Image.open(sys.argv[1])).astype(int)
tros=np.zeros((64,64),bool)
for n,(sp,sr,dx,dy) in B.INSTEL.items():
    for f in B.tros(n,sp,sr,dx,dy):
        for (x,y) in f['F']:
            if ok(y,x): tros[y,x]=True
def buiten(y,x): return not ok(y,x) or not tros[y,x]
uit=[]
for dy,dx,naam in ((-1,0,'boven'),(1,0,'onder'),(0,-1,'links'),(0,1,'rechts')):
    for k in range(64):
        run=[]
        for t in range(65):
            y,x=(k,t) if dy else (t,k)
            if t<64 and tros[y,x] and buiten(y+dy,x+dx): run.append(t)
            else:
                if len(run)>=4: uit.append((naam,k,run[0],run[-1],len(run)))
                run=[]
print(len(uit),'rechte stukken >=4:'); [print(' ',u) for u in uit]
# binnenlijnen (regel 8): horizontale rijen lijnrood/zwart >= 5 binnen een tros (geen oogwit erboven of eronder)
uit=[]
for y in range(64):
    run=[]
    for x in range(65):
        if x<64 and tros[y,x] and o[y,x] in (1,2): run.append(x)
        else:
            if len(run)>=5: uit.append((y,run[0],run[-1]))
            run=[]
print('horizontale lijnen >=5 in de trossen:',uit)
