# r2: alleen variant a1. Oog- en spiraalzone 1-op-1 uit r1 (bewijs diff 0 daar).
import numpy as np; from PIL import Image
import varianten as V
from palet import PAL
H,W=V.H,V.W; OX,OY=7,12
r1=np.load('../sprite_r1/r1_a1.npy')
jj,ii=np.mgrid[0:H,0:W]
OOG=((ii>=11)&(ii<=21)|(ii>=24)&(ii<=34))&(jj<=9)
SPI=V.buik&(jj>=17)&(jj<=30)&(ii>=16)&(ii<=30)
o=V.maak('a','1'); o[OOG|SPI]=r1[OOG|SPI]
np.save('r2_a1.npy',o)
S=np.zeros((64,64),'uint8'); S[OY:OY+H,OX:OX+W]=o
im=Image.fromarray(S,'P'); im.putpalette([c for t in PAL for c in t]); im.save('poliwhirl_regional_r2_a1.png',transparency=0)
d=o!=r1
print('diff r1->r2: totaal %d, in oogzone %d, in spiraalzone %d'%(d.sum(),(d&OOG).sum(),(d&SPI).sum()))
print('kleuren incl. transparant:',len(np.unique(np.append(o,0))))
