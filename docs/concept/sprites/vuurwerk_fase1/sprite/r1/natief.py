# Natief raster van het Gemini-model terughalen: pitch 5.12 (200x200), celgrenzen op -0.42 + k*5.12 (randsterkte gemeten)
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../../referenties/model.png').convert('RGB')).astype(int)
P=5.12; C0=-0.42
out=np.zeros((200,200,3),'uint8')
for j in range(200):
  for i in range(200):
    cy=C0+j*P+P/2; cx=C0+i*P+P/2
    y0,y1=int(round(cy-1.5)),int(round(cy+1.5)); x0,x1=int(round(cx-1.5)),int(round(cx+1.5))
    y0,x0=max(0,y0),max(0,x0)
    out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('natief.png')
g=out.min(2); yy,xx=np.where(g<225); print('bbox',xx.min(),xx.max(),yy.min(),yy.max())
