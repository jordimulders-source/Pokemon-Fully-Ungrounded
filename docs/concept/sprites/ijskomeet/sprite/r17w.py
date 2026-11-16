# r17 = r15 + linker buitenlijn lichter (Jordi: beter) + kopbovenkant als lijn; ontkorrelen alleen losse 1-px in paars en gas (ijsfacetten blijven)
import numpy as np; from PIL import Image
from collections import Counter
o=np.load('r15w/o4.npy').copy(); pal=Image.open('r15.png').getpalette(); vap=np.load('r15w/vap.npy')
K,W,L,M,D,S,N,G,g=1,2,3,4,5,6,13,11,15
top=[(7,27),(8,27),(9,27),(10,26),(11,25),(12,24),(13,24),(14,23),(15,23),(16,24),(17,25)]
for x,y in top: o[y,x]=N
fg=o>0
for y in range(64):
  for x in range(64):
    if o[y,x]==K and x<=14 and any(0<=y+dy<64 and 0<=x+dx<64 and not fg[y+dy,x+dx] for dy,dx in((0,-1),(-1,0),(-1,-1),(1,-1))):
      o[y,x]=S if y<46 else N
PUR={7,8,9,10}; GAS={W,L,G,g}; n=0
for y in range(1,63):
  for x in range(1,63):
    c=o[y,x]
    if vap[y,x] and c in GAS: grp=GAS
    elif c in PUR: grp=PUR
    else: continue
    nb=[o[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1))]
    if c in nb: continue
    same=[k for k in nb if k in grp]
    if len(same)>=3:
      o[y,x]=Counter(same).most_common(1)[0][0]; n+=1
print('losse pixels',n)
im=Image.fromarray(o.astype(np.uint8)).convert('P'); im.putpalette(pal); im.save('r17.png',transparency=0)
a=im.convert('RGB').resize((512,512),Image.NEAREST); a.save('r17_8x.png')
b=Image.open('r15.png').convert('RGB').resize((512,512),Image.NEAREST); m=Image.open('vel_r9.png').crop((1060,0,1590,520))
v=Image.new('RGB',(1600,530),'white'); v.paste(a,(0,8)); v.paste(b,(530,8)); v.paste(m,(1060,0)); v.save('voor_jordi_r17.png')
