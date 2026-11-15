import sys; sys.path.insert(0,'r6w'); sys.path.insert(0,'.')
import numpy as np
import numpy as np, p6, gio
from PIL import Image
MAP=dict(zip('KWLMDSijnvwcCrg','KWLMDSabcdGeCrg'))
r5g=gio.from_txt('r5.txt')
R=np.full((64,64),-1)
for j in range(64):
  for i in range(64):
    if r5g[j,i]>=0: R[j,i]=p6.CH.index(MAP[gio.CH[r5g[j,i]]])
CH=p6.CH; I={c:k for k,c in enumerate(CH)}
def isin(o,s): return np.isin(o,[I[c] for c in s])
def flood(o,seeds,ok):
    reg=np.zeros((64,64),bool); st=list(seeds)
    for s in st: reg[s]=True
    while st:
        a,b=st.pop()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            y,x=a+dy,b+dx
            if 0<=y<64 and 0<=x<64 and not reg[y,x] and ok[y,x]: reg[y,x]=True; st.append((y,x))
    return reg
def show(o,mark=None,y0=0,y1=64,x0=0,x1=64):
    for j in range(y0,y1):
        print('%2d '%j+''.join(('#' if (mark is not None and mark[j,i]) else ('.' if o[j,i]<0 else CH[o[j,i]])) for i in range(x0,x1)))
