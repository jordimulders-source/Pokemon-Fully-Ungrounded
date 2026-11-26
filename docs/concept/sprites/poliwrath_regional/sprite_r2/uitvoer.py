# Uitvoer r2: 6 png's + bewijs dat alles buiten oog- en mondzone gelijk is aan r1 O1S1 (zelfde basis, spiraal S1).
import numpy as np; from PIL import Image
import varianten as V
from palet import PAL
OX,OY=1,2; H,W=V.H,V.W; R={}
for e in ('E1','E2'):
    for m in ('M1','M2','M3'):
        o=V.maak(e,m); R[e+m]=o; np.save('r2_%s%s.npy'%(e,m),o)
        S=np.zeros((64,64),'uint8'); S[OY:OY+H,OX:OX+W]=o
        im=Image.fromarray(S,'P'); im.putpalette([c for t in PAL for c in t]); im.save('poliwrath_regional_r2_%s%s.png'%(e,m),transparency=0)
r1=np.array(Image.open('../sprite_r1/poliwrath_regional_r1_O1S1.png'))[OY:OY+H,OX:OX+W]
jj,ii=V.jj,V.ii
OOG=(jj<=12)&(ii>=12)&(ii<=45)
MOND=(jj>=12)&(jj<=18)&(ii>=13)&(ii<=43)
if __name__=='__main__':
    for k,o in R.items():
        d=o!=r1
        print('%s: verschil met r1 O1S1 %d px, in oogzone %d, mondzone %d, ERBUITEN %d'%(k,d.sum(),(d&OOG).sum(),(d&MOND&~OOG).sum(),(d&~OOG&~MOND).sum()),
              '| silhouet +%d -%d'%(((o>0)&(r1==0)).sum(),((o==0)&(r1>0)).sum()))
    print(V.INFO)
