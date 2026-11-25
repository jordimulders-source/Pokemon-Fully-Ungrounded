"""Modelhelderheid per spritepixel: luminantie van model_r5, wit genegeerd (genormaliseerde gauss, sigma s modelpx),
puntmeting in het midden van elke spritecel (mapping px.py: x0=133, p=12.0645, sprite = modelgrid +1 in x)."""
import numpy as np
from PIL import Image, ImageFilter
M=np.asarray(Image.open('../../referenties/model_r5.png').convert('RGB')).astype(float)
L=M@[.299,.587,.114]; fg=(M.min(2)<225).astype(float)
def bl(a,s):
    r=int(3*s); k=np.exp(-np.arange(-r,r+1)**2/(2*s*s)); k/=k.sum()
    a=np.apply_along_axis(lambda v: np.convolve(v,k,'same'),0,a)
    return np.apply_along_axis(lambda v: np.convolve(v,k,'same'),1,a)
for s in (4,5):
    B=bl(L*fg,s)/np.maximum(bl(fg,s),1e-3)
    p=12.064516129032258; X0,Y0=133,860-62*p
    g=np.full((64,64),np.nan)
    for y in range(64):
        for x in range(1,63):
            my=Y0+(y+.5)*p; mx=X0+(x-1+.5)*p
            if 0<=my<1024 and fg[int(my),int(mx)]>0: g[y,x]=B[int(my),int(mx)]
    np.save(f'lum_s{s}.npy',g)
