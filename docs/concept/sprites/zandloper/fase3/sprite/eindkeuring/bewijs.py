# Bewijs: zelfde silhouet (alpha) en lijnpixels alleen gewisseld tussen lijntinten.
import numpy as np; from PIL import Image
LIJN={1,2,7,11}   # zwart, zand-, glas-, houtlijn
v=np.array(Image.open('../r11/biceps.png')); n=np.array(Image.open('zandloper_fase3.png'))
im=Image.open('zandloper_fase3.png')
assert ((v==0)==(n==0)).all(); print('alpha gelijk: ja')
lv=np.isin(v,list(LIJN)); ln=np.isin(n,list(LIJN))
print('lijnposities gelijk:', (lv==ln).all())
d=np.argwhere(v!=n); print('gewijzigde pixels:',len(d))
from collections import Counter
print(Counter((int(v[y,x]),int(n[y,x])) for y,x in d))
print('kleuren in gebruik:',len(np.unique(n)),'(incl. transparant), index 0 transparant:',im.info.get('transparency'))
