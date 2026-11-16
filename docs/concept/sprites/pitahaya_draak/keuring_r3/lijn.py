from PIL import Image; import numpy as np
S=np.array(Image.open('sprite_r3/pitahaya_r3.png')); d=np.load('keuring_r2/model_per_px.npz')
mzw,mlum,mg=d['mzw'],d['mlum'],d['mg']
H=S>0
def rand(x,y):
    return any(not H[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1)))
print('interne zwarte px (niet aan transparant grenzend): x,y mzw/9 mlum groep buren')
for y in range(64):
  for x in range(64):
    if S[y,x]==1 and not rand(x,y):
      nb=[S[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1))]
      nz=sum(v==1 for v in nb)
      print((x,y),mzw[y,x],round(mlum[y,x]),mg[y,x],'zwarte4buren',nz, 'FACE' if 18<=x<=34 and 22<=y<=34 else '')
