import numpy as np; from PIL import Image
import maak3 as M3
from palet import PAL
H,W=M3.H,M3.W; OX,OY=7,12
for v in ('E6','E5','EM'):
    o=M3.maak(v); np.save('r3_%s.npy'%v,o)
    S=np.zeros((64,64),'uint8'); S[OY:OY+H,OX:OX+W]=o
    im=Image.fromarray(S,'P'); im.putpalette([c for t in PAL for c in t]); im.save('poliwhirl_regional_r3_%s.png'%v,transparency=0)
    d=o!=M3.r2
    print('%s: diff met r2_S2 %d px, in oogzone %d, ERBUITEN %d, kleuren %d'%(v,d.sum(),(d&M3.M.OOGZ).sum(),(d&~M3.M.OOGZ).sum(),len(np.unique(np.append(o,0)))))
for i in M3.INFO: print(i)
