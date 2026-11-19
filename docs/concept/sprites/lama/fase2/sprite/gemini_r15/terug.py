# Gemini r15 (16x) terug naar 64x64 op het r3-palet (mediaan per 16x16-vak, dichtstbijzijnde paletkleur)
from PIL import Image; import numpy as np
g=np.array(Image.open('gemini_r15/r15.png').convert('RGB')).astype(int)
r3=Image.open('r3/lama.png'); pal=np.array(r3.getpalette()[:48]).reshape(16,3)
out=np.zeros((64,64),np.uint8)
for y in range(64):
    for x in range(64):
        blk=g[y*16+4:y*16+13, x*16+4:x*16+13].reshape(-1,3); c=np.median(blk,0)
        if c.sum()>720: out[y,x]=0; continue
        out[y,x]=1+np.argmin(((pal[1:]-c)**2).sum(1))
im=Image.fromarray(out,'P'); im.putpalette(r3.getpalette()); im.save('gemini_r15/r15_64.png',transparency=0)
