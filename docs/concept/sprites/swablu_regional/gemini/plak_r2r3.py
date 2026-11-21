# Altaria A (Jordi 21 nov): wolk + static van r2, kop/hals/kuif van r3 (zelfde raster, elders pixelgelijk).
from PIL import Image, ImageFilter; import numpy as np
a=np.asarray(Image.open('altaria_r2.webp').convert('RGB')); b=np.asarray(Image.open('altaria_r3.webp').convert('RGB'))
d=np.abs(a.astype(int)-b.astype(int)).sum(2)>60
def dil(m,k=7): return np.asarray(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(k)))>0
D=dil(d)
m=np.zeros_like(D); m[450,400]=True
while True:
    n=dil(m,3)&D
    if n.sum()==m.sum(): break
    m=n
out=a.copy(); out[m]=b[m]
Image.fromarray(out).save('altaria_A_r2wolk_r3kop.png'); print(m.sum())
