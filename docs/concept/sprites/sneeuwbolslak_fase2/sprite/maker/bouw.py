# python3 maker/bouw.py : leeg raster + bol_r1 (x21) + deel_r1 -> raster_r1.txt ; meldt segmenten buiten silhouet
import numpy as np
SIL=np.load('sil56_rond.npy'); R=[['.']*64 for _ in range(64)]
segs=[]
for l in open('maker/bol_r1.txt'):
  y,t=l.split(); segs.append((int(y),21,t))
for l in open('maker/deel_r1.txt'):
  y,x,t=l.rstrip('\n').split(' ',2); segs.append((int(y),int(x),t))
for y,x0,t in segs:
  for i,ch in enumerate(t):
    x=x0+i
    if ch=='.': continue
    if not SIL[y,x]: print('buiten silhouet',x,y,ch)
    R[y][x]=ch
for y in range(64):
  for x in range(64):
    if SIL[y,x] and R[y][x]=='.': print('gat',x,y)
open('maker/raster_r1.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
