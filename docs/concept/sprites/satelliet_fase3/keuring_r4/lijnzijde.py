# Keurder r4: zwart (1) met transparant alleen boven/links = lichtkant; navy (2) met transparant alleen onder/rechts = schaduwkant.
from PIL import Image; import numpy as np
a=np.array(Image.open('docs/concept/sprites/satelliet_fase3/sprite/r4/sprite.png'))
def t(x,y): return not(0<=x<64 and 0<=y<64) or a[y,x]==0
z=[];n=[]
for y in range(64):
  for x in range(64):
    v=a[y,x]
    if v not in(1,2): continue
    L=t(x-1,y) or t(x,y-1); S=t(x+1,y) or t(x,y+1)
    if v==1 and L and not S: z.append((x,y))
    if v==2 and S and not L: n.append((x,y))
print('zwart alleen aan lichtkant:',len(z),z)
print('navy alleen aan schaduwkant:',len(n),n)
