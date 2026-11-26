# Echte pitch van gemini/r9.png is 5,12 px (randsterkte-piek 15493 tegen gemiddeld 4935; 10,24 is elke tweede lijn).
# Haalt het 200x200-raster terug: mediaan van het midden van elke cel.
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../gemini/r9.png').convert('RGB')).astype(int)
p,ph=5.12,4.1
cs=np.arange(ph+p/2-p,1024,p); cs=cs[cs>=1]
W=len(cs); out=np.zeros((W,W,3),'uint8')
for j,y in enumerate(cs):
  for i,x in enumerate(cs):
    b=a[max(0,int(y-1)):int(y+2),max(0,int(x-1)):int(x+2)].reshape(-1,3)
    out[j,i]=np.median(b,0)
Image.fromarray(out).save('r9_natief200.png'); print(W)
