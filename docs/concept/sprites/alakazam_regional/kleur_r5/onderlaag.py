# onderlaag: model per spritepixel (mediaan) -> materiaal + tint. Alleen als basis; daarna handwerk in raster_A.txt
import numpy as np
d=np.load("meet5.npz"); med,sil,fo=d["med"],d["sil"],d["fo"]
L=med.mean(2); red=med[...,0]>med[...,2]+40
pad=np.pad(sil,1)
edge=sil&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
def plate(x,y): return 11<=x<=25 and 17<=y<=28 and not (x>=24 and y<=19)
out=[]
for y in range(64):
  r=''
  for x in range(64):
    if not sil[y,x]: r+='.'; continue
    l=L[y,x]
    if edge[y,x]: r+="o"; continue
    if red[y,x]: r+= 't' if l>120 else 'r' if l>70 else 's'
    elif fo[y,x]>=0.3: r+="o"
    elif plate(x,y) and l<150:
        r+= 'p' if l>=128 else 'n' if l>=108 else 'm' if l>=60 else 'k'
    elif l<56: r+='k'
    elif l<80: r+='m'
    elif l>=232: r+='w'
    elif l>=190: r+='a'
    elif l>=152: r+='b'
    elif l>=115: r+='c'
    else: r+='d'
  out.append(r)
open('onderlaag.txt','w').write('\n'.join(out)+'\n')
