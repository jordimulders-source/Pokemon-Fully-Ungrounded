import numpy as np; from pal import *
g=lees('rufflet_r1.txt'); g=np.pad(g,((0,0),(0,0)),constant_values='.')
for r in open('fixes_r2.txt'):
  r=r.split('#')[0].strip()
  if not r: continue
  y,x,s=r.split(); y,x=int(y),int(x)
  for i,c in enumerate(s):
    if c!='_': g[y,x+i]=c
schrijf('rufflet_r2.txt',g)
r1=lees('rufflet_r1.txt'); print('px gewijzigd t.o.v. r1:',int((g!=r1).sum()),'silhouet:',int(((g!='.')!=(r1!='.')).sum()), [(int(y),int(x)) for y,x in zip(*np.where((g!='.')!=(r1!='.')))])
