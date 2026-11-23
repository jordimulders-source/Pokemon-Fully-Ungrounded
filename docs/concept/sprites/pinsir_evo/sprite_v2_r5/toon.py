import sys,numpy as np
from PIL import Image
DF=np.load('sprite_v2_r5/DF.npy');ML=np.load('sprite_v2_r5/ML.npy');RG=np.load('sprite_v2_r5/RG.npy')
f=sys.argv[1]
x0,x1,y0,y1=map(int,sys.argv[2:6])
r4=np.array(Image.open(f))
def cel(y,x):
  d=DF[y,x]
  if d<0: return '  .'
  if d>=.45: return ' ##'
  if d>=.2: return ' #%d'%int(d*10)
  v=int(ML[y,x]); return ('r%2d'%(v%100)) if RG[y,x]>45 else '%3d'%v
print('model (## lijn, #n deels lijn, getal = helderheid, r = rood)')
print('   '+''.join('%3d'%x for x in range(x0,x1)))
for y in range(y0,y1): print('%2d '%y+''.join(cel(y,x) for x in range(x0,x1)))
print(f)
print('   '+''.join('%3d'%x for x in range(x0,x1)))
for y in range(y0,y1): print('%2d '%y+''.join('%3s'%('.' if r4[y,x]==0 else r4[y,x]) for x in range(x0,x1)))
