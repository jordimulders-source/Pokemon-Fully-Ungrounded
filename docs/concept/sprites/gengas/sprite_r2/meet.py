# meet.py: modelklasse per spritepixel (blok 74/64 uit het natieve model, mediaan, dichtstbijzijnde paletkleur) als tekstkaart.
# Gebruik: python3 meet.py [x0 x1 y0 y1]   ('.'=achtergrond). Alleen meting, geen inkleuring.
import sys,numpy as np
from PIL import Image
sys.path.insert(0,'.'); from pal import PAL,CH
M='../model/gekozen_v3_natief.png'
a=np.asarray(Image.open(M).convert('RGB')).astype(float); s=74/64
P=np.array(PAL[1:7]+PAL[13:16],float); idx=[1,2,3,4,5,6,13,14,15]
def blok(x,y):
    return a[int(y*s):int(np.ceil((y+1)*s)), int(x*s):int(np.ceil((x+1)*s))].reshape(-1,3)
def klas(x,y):
    b=blok(x,y); bgc=(b.min(1)>=232).mean()
    if bgc>0.5: return '.'
    b=b[b.min(1)<232]; m=np.median(b,0)
    if m.min()>200: return 'W'   # wit (tanden)
    if m[0]>200 and m[1]<170: return 'R'  # rood oog
    return CH[idx[int(np.argmin(((P-m)**2).sum(1)))]]
if __name__=='__main__':
    x0,x1,y0,y1=(map(int,sys.argv[1:5]) if len(sys.argv)>4 else (0,64,0,64))
    print('    '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%3d '%y+''.join(klas(x,y) for x in range(x0,x1)))
