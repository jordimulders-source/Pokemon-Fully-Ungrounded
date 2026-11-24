# Elke modelpixel -> dichtstbijzijnde paletkleur (vast palet, gemeten op het model). Uitvoer klassen.npy (1024x1024, 0=bg)
from PIL import Image; import numpy as np
from scipy import ndimage as nd
PAL=[(255,0,255),(24,18,34),(240,238,234),(212,200,222),(186,170,204),(144,120,164),
     (196,146,204),(138,90,156),(92,58,116),(48,32,80),(76,66,130),(176,160,204),
     (134,194,192),(86,170,166),(60,106,134),(100,92,160)]
PAL_UIT=np.array(PAL); PAL_UIT[4]=(192,176,208)   # r4: weergavetint 4 = modelkleur #c0b0d0 (lijftint.py); klassering houdt de oude waarde
np.save('pal.npy',PAL_UIT)
a=np.asarray(Image.open('../model.png').convert('RGB')).astype(float)
w=(a.min(2)>=245)&((a.max(2)-a.min(2))<15)
lab,n=nd.label(w); keep={lab[0,0]}; sz=nd.sum(w,lab,range(1,n+1)); ob=nd.find_objects(lab)
for i in range(n):
    s=ob[i]
    if sz[i]>2000 and s[1].start>=584 and s[1].stop<=680: keep.add(i+1)
bg=np.isin(lab,list(keep))
bg|=(a.min(2)>=225)&((a.max(2)-a.min(2))<20)&nd.binary_dilation(bg,iterations=3)
P=np.array(PAL[1:],float)
d=((a[...,None,:]-P[None,None])**2).sum(-1)
d[...,11-1]=1e9          # 11 = rasterkleur groot paneel: alleen via zone (klassen2.py), anders pakt het lijflavendel hem
Z=np.array(Image.open('zones.png'))
d[Z==0,15-1]=1e9         # 15 = paneelraster/donkerblauw-lila: alleen binnen de panelen
k=d.argmin(-1)+1; k[bg]=0
np.save('klassen.npy',k.astype(np.uint8))
pal=[v for c in PAL for v in c]
im=Image.fromarray(k.astype('uint8'),'P'); im.putpalette(pal+[0]*(768-len(pal))); im.convert('RGB').save('klassen.png')
print(np.bincount(k.ravel(),minlength=16))
