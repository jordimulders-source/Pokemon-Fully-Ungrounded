import numpy as np; from PIL import Image
import maak2 as M
from palet import PAL
H,W=M.H,M.W; OX,OY=7,12
R={}
for sv in ('S1','S2'):
    M.OOGTEL.clear(); o,P=M.maak(sv); R[sv]=(o,P); np.save('r2_%s.npy'%sv,o)
    S=np.zeros((64,64),'uint8'); S[OY:OY+H,OX:OX+W]=o
    im=Image.fromarray(S,'P'); im.putpalette([c for t in PAL for c in t]); im.save('poliwhirl_regional_r2_%s.png'%sv,transparency=0)
    print(sv,'kleuren incl. transparant',len(np.unique(np.append(o,0))),'spiraalpixels',len(P))
    for n,bb,doel in M.OOGTEL: print('  oog: %d px in de bron (gba x %d-%d, y %d-%d) -> geplakt op x %d-%d, y %d-%d (64-vak +7,+12)'%((n,)+tuple(bb)+tuple(doel)))
    g=np.zeros((H,W),bool)
    for n,bb,(x0,x1,y0,y1) in M.OOGTEL: pass
SPZ=M.V.buik&(M.jj>=17)&(M.jj<=30)&(M.ii>=15)&(M.ii<=31)
d=R['S1'][0]!=R['S2'][0]; print('S1-S2 diff: totaal %d, in spiraalzone %d, ERBUITEN %d'%(d.sum(),(d&SPZ).sum(),(d&~SPZ).sum()))
r1=np.load('../sprite_r1/r1_a1.npy'); d=R['S1'][0]!=r1
OOGZ=M.OOGZ
print('r1->r2 (S1): totaal %d, oogzone %d, spiraalzone %d, rest %d'%(d.sum(),(d&OOGZ).sum(),(d&SPZ).sum(),(d&~OOGZ&~SPZ).sum()))
