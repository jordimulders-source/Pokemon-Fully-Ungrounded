# Wangoog (zonder glans, op het cremestuk rond native x40-44,y35-39) weghalen: donkere pixels -> mediaan van de cremeburen. Alleen weghalen, niets tekenen.
from PIL import Image; import numpy as np
a=np.asarray(Image.open('natief.png').convert('RGB')).copy(); A=a.astype(int)
lum=0.299*A[...,0]+0.587*A[...,1]+0.114*A[...,2]
oog=[(41,35),(42,35),(40,36),(41,36),(42,36),(43,36),(40,37),(41,37),(42,37),(43,37),(41,38),(42,38),(43,38)]  # alleen de oogvlek, niet de voeg of het zwarte stuk
reg=(slice(33,42),slice(38,47)); sub=A[reg]; L=lum[reg]
cream=sub[L>170]; c=np.median(cream,axis=0).astype('uint8'); print('creme',c, len(cream))
for x,y in oog: a[y,x]=c
Image.fromarray(a).save('natief_zonder_wangoog.png')
Image.fromarray(a).crop((5,20,60,70)).resize((660,600),Image.NEAREST).save('kop_zonder_wangoog_12x.png')
