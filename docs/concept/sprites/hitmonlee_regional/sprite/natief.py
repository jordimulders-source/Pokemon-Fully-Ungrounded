# Natief raster van gemini/r2.png terughalen. Pitch 5,12 (200x200 cellen; randsterkte-piek, fase 0;
# 10,24 scoort ook hoog maar op 8x zoom zijn de cellen 5 px: ringlijnen en lijntrapjes zijn 1 cel van 5,12).
# Per cel: mediaan van de binnenste 3x3 pixels.
from PIL import Image; import numpy as np
D='docs/concept/sprites/hitmonlee_regional/'
a=np.asarray(Image.open(D+'gemini/r2.png').convert('RGB')).astype(int)
P=5.12; N=200
out=np.zeros((N,N,3),int)
for j in range(N):
  for i in range(N):
    y0=int(round(j*P+1)); x0=int(round(i*P+1))
    out[j,i]=np.median(a[y0:y0+3,x0:x0+3].reshape(-1,3),0)
m=(out.min(2)<235); ys,xs=np.where(m)
y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
# even maken voor 2x-reductie
if (y1-y0)%2: y0-=1
if (x1-x0)%2: x0-=1
print('bbox',x0,x1,y0,y1)
Image.fromarray(out[y0:y1,x0:x1].astype('uint8')).save(D+'sprite/natief.png')
