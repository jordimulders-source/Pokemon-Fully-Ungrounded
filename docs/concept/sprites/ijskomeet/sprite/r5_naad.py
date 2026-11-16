# r5: naadmasker 1-op-1 uit het model: per spritepixel het aandeel donkere modelpixels (model_12x, 12x12 blok)
from PIL import Image; import numpy as np
from gio import from_txt, CH
m=np.asarray(Image.open('model_12x.png').convert('RGB')).astype(float)
lum=m.mean(2)
D=np.zeros((64,64))
for y in range(64):
    for x in range(64):
        b=lum[y*12:(y+1)*12,x*12:(x+1)*12]; D[y,x]=(b<90).mean()
np.save('r5_D.npy',D)
o=from_txt('r4.txt')
for y in range(18,62):
    print('%2d '%y+''.join(('.' if o[y,x]<0 else ' ') if D[y,x]<0.05 else str(min(9,int(D[y,x]*10))) for x in range(0,36)))
