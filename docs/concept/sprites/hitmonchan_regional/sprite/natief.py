# Natief raster van gemini/r3.png terughalen. Pitch 10,24 (op 8x zoom gecontroleerd: geen halve cellen), fase 9,25.
# Per cel: mediaan van de binnenste 4x4 pixels. Slaat natief.png op (bijgesneden tot de figuur).
from PIL import Image; import numpy as np
D='docs/concept/sprites/hitmonchan_regional/'
a=np.asarray(Image.open(D+'gemini/r3.png').convert('RGB')).astype(int)
P=10.24; F=9.25; N=int((1024-F)//P)
out=np.zeros((N,N,3),int)
for j in range(N):
  for i in range(N):
    y0=int(round(F+j*P+3)); x0=int(round(F+i*P+3))
    out[j,i]=np.median(a[y0:y0+4,x0:x0+4].reshape(-1,3),0)
m=(out.min(2)<235); ys,xs=np.where(m)
y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
print('bbox cellen',x0,x1,y0,y1, 'maat',x1-x0,y1-y0)
Image.fromarray(out[y0:y1,x0:x1].astype('uint8')).save(D+'sprite/natief.png')
