# Onderlaag ontkorrelen: ijsvulling (a,b,c,e) mode-filter 3x3, clusters <4 nemen buurtint. Lijnen/rood/blauw blijven.
import numpy as np
R=[list(l.rstrip('\n')) for l in open('maker/onderlaag.txt')]
ICE='abce'
def lum(ch): return {'a':0,'b':1,'c':2,'e':3}[ch]
for it in range(2):
  N=[r[:] for r in R]
  for y in range(1,63):
    for x in range(1,63):
      if R[y][x] in ICE+'dw':
        nb=[R[y+dy][x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if R[y+dy][x+dx] in ICE]
        if nb:
          v,n=np.unique(nb,return_counts=True)
          if n.max()>=4: N[y][x]=v[n.argmax()]
          elif R[y][x] in 'dw': N[y][x]=R[y][x]
  R=N
open('maker/glad.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
for i,l in enumerate(R[17:60]): print('%2d %s'%(i+17,''.join(l)))
