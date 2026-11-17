# r8: maakt de probeersels a-e (oog8.bouw) op basis r5 115% geel + vlamtong (vlam8). Zie oog8.py voor de regels.
import json, numpy as np; from PIL import Image
from oog8 import bouw; from vlam8 import vlam
PAL=json.load(open('palet.json'))
basis=vlam(np.asarray(Image.open('../r5/sprite_115_geel.png')).astype(int))
#        O           F    RV0  RV1  BOVEN DICHT PUPIL GLANS
P={'r7':((13,22),   1.5, 2.0, 3.2, 0,    0,    'h',  0),     # = r7 (controle)
   'a': ((13,23.4), 2.0, 2.6, 4.6, 1,    0,    'h',  0),     # 2x
   'b': ((13,22),   1.5, 2.0, 3.2, 0,    1,    'h',  0),     # 1,5x + gesloten omlijning
   'c': ((13,23.4), 2.0, 2.6, 4.6, 1,    1,    'v',  0),     # 2x + gesloten + pupil verticaal
   'd': ((13,23.4), 2.0, 2.6, 4.6, 1,    1,    'h',  1),     # 2x + gesloten + glans
   'e': ((13,23.4), 2.0, 2.6, 4.6, 1,    1,    'v',  1)}     # voorstel: 2x + gesloten + verticale pupil + glans
if __name__=='__main__':
    HX='.123456789ABCDEF'; out={}
    for k,p in P.items():
        a,info=bouw(*p,basis); out[k]=a
        im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save('sprite_%s.png'%k,transparency=0)
        print(k,info,'| diff t.o.v. basis',int((a!=basis).sum()))
    for y in range(15,28): print('%2d'%y,'  '.join(''.join(HX[v] for v in out[k][y,4:20]) for k in P))
