# onderlaag: Gemini-gemiddelde per spritepixel -> dichtstbijzijnde Gemini-referentiekleur -> oude paletindex
import numpy as np
from PIL import Image
m=np.load('stappen/sil.npy'); g=np.load('stappen/gids.npy')
ref=[((154,137,119),'7'),((124,108,95),'6'),((86,76,65),'8'),((55,55,55),'2'),((30,25,22),'1'),
     ((190,140,92),'5'),((160,113,71),'4'),((120,80,52),'3'),((178,153,131),'B'),((140,118,100),'b'),
     ((70,62,58),'F'),((193,143,142),'e'),((138,87,93),'f'),((225,215,180),'c'),((160,150,120),'d'),((110,40,30),'a')]
R=np.array([r for r,_ in ref],float)
out=[]
for y in range(64):
  row=''
  for x in range(64):
    if not m[y,x]: row+='.'; continue
    d=((R-g[y,x])**2).sum(1); row+=ref[d.argmin()][1]
  out.append(row)
open('stappen/onderlaag.txt','w').write('\n'.join(out)+'\n')
print('\n'.join(out))
