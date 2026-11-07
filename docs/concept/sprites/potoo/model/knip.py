# Stap 1: model losknippen van het nep-dambord, tak weg (Jordi 6-7 nov). Uitvoer: model_los.png
import numpy as np; from PIL import Image; from collections import deque
a=np.asarray(Image.open('../referenties/gemini_model_jordi.jpg').convert('RGB')).astype(int)
H,W,_=a.shape; lum=a.mean(2); chroma=a.max(2)-a.min(2)
bgc=(chroma<16)&((abs(lum-212)<16)|(lum>238))
def flood(m,seeds):
    o=np.zeros_like(m); q=deque()
    for y,x in seeds:
        if m[y,x] and not o[y,x]: o[y,x]=1; q.append((y,x))
    while q:
        y,x=q.popleft()
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and m[yy,xx] and not o[yy,xx]: o[yy,xx]=1; q.append((yy,xx))
    return o
seeds=[(y,x) for y in range(H) for x in (0,W-1)]+[(y,x) for x in range(W) for y in (0,H-1)]
bg=flood(bgc,seeds)
fg=~bg
# alleen de grootste samenhangende vorm (takje en losse vlek vallen weg)
from scipy import ndimage
lab,n=ndimage.label(fg); sizes=ndimage.sum(fg,lab,range(1,n+1)); fg=lab==(1+np.argmax(sizes))
# takeinde in de klauwen: olijfkleur
olive=(a[...,1]>a[...,2]+12)&(lum>40)&(lum<165)
box=np.zeros_like(olive); box[790:890,430:540]=True; olive&=box
olive=flood(olive,[(840,482),(830,470)])
olive=ndimage.binary_closing(olive,iterations=2)
olive&=fg
fg&=~olive
np.save('fg.npy',fg)
o=np.zeros((H,W,4),'uint8'); o[...,:3]=a; o[...,3]=fg*255
Image.fromarray(o).save('model_los.png')
print(fg.sum(), np.where(fg.any(0))[0][[0,-1]], np.where(fg.any(1))[0][[0,-1]])
