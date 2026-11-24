# k10 = k9 + bergwand met de hand in facetten: donkere band (e), lichte facet (f) met hooglichtrand (6) linksboven, putje (e)
import sys, numpy as np
sys.path.insert(0,'../k1')
from gereedschap import *
a8,_=laad('../k8/tempel.png'); a9,pal=laad('../k9/tempel.png'); a=a9.copy()
C={'h':6,'f':15,'e':14}
# per rij: lijst van (x, tekens) ; elk teken is één pixel vanaf x
ONTWERP={
 # boven (x48-57, y19-26): band rechtsboven, facetrand schuin van (55,21) naar (52,23), putje linksonder
 19:[(48,'ffff'),(53,'eee')],
 20:[(48,'ffff'),(55,'ee')],
 21:[(50,'f'),(53,'hhhe')],
 22:[(48,'fffffhhfe')],
 23:[(48,'feefhhffe')],
 24:[(48,'fefffffffe')[:1] if False else (48,'feffffffe')],
 25:[(48,'ffffffffee')],
 26:[(53,'ffeee')],
 # midden (x49-59, y29-39)
 29:[(52,'ffeeee')],
 30:[(49,'ff'),(52,'ffeeeee')],
 31:[(50,'f'),(52,'feeeehh')],
 32:[(53,'eeehhf')],
 33:[(50,'fffeehhff')],
 34:[(49,'ffffeeffff')],
 35:[(49,'ffffeeffffe')],
 36:[(49,'feffeeefffe')[:0] or (49,'feffeeefffe')],
 37:[(49,'feefffeefffe'[:0] or 'feeffeefffe')],
 38:[(49,'ffffffeeffe')],
 39:[(49,'ffffffe'),(59,'e')],
 # onder (x49-61, y42-56)
 42:[(56,'eeeee')],
 43:[(56,'eeeee')],
 44:[(56,'ehhee')],
 45:[(55,'ehhf'),(60,'ee')],
 46:[(54,'eeefff'),(60,'ee')],
 47:[(53,'eeefffff'),(60,'ee')],
 48:[(55,'efffff'),(61,'e')],
 49:[(53,'ef'),(58,'fff')],
 50:[(52,'fefff'[:3]),(58,'fff')],
 51:[(52,'feefff'[:0] or 'feeff'[:3]),(58,'ff')],
 52:[(49,'fhffeeffff'[:0] or 'f'),(51,'ffeeffff'[:0] or 'ffffeeff')],
 53:[(49,'fffffffee'[:0] or 'ffffffee')],
 54:[(49,'ffefff')],
 55:[(49,'feeff')],
 56:[(49,'fff')],
}
ver=[]
for y,lst in ONTWERP.items():
    for x0,s in lst:
        for i,ch in enumerate(s):
            x=x0+i
            ok = a9[y,x] in (14,15) or (a9[y,x]==6 and a8[y,x]==15)
            if not ok: ver.append((x,y,int(a9[y,x]))); continue
            a[y,x]=C[ch]
print('overgeslagen (geen muurpixel):',ver)
np.save('wand.npy',a); bewaar(a,pal,'tempel.png')
