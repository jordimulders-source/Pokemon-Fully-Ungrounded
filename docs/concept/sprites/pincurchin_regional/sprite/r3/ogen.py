# r3b: linkeroog smaller (1 kolom uit Pincurchins oog geschrapt), rechteroog 1 px lager (gemeten: model-rechteroog
# ligt 0,73 px lager dan het linker -> 1 px), mond 115/130 % bovenop de naad (mond.py). Niets getekend.
import numpy as np
from PIL import Image
from toon import save
from mond import maak
pin=np.array(Image.open('../../../../../../graphics/pokemon/pincurchin/anim_front.png'))[:64].astype(int)
MAP={3:0,10:8,9:9,7:10,5:11,8:12,11:13}
OOG=pin[39:44,27:32]                    # Pincurchins oog, 6 = lijf
A2=np.load('../r2/A.npy'); B2=np.load('../r2/B.npy'); kaal=np.load('../r1/schoon.npy')   # lijf zonder ogen
def zet(A,oog,y0,x0):
    m=np.zeros((64,64),bool)
    for j in range(oog.shape[0]):
        for i in range(oog.shape[1]):
            v=oog[j,i]
            if v in MAP: A[y0+j,x0+i]=MAP[v]; m[y0+j,x0+i]=True
    return m
LINKS={'c4':np.delete(OOG,4,1),       # kolom 4 schrappen: neemt 3 ringpixels weg (minste)
       'c3':np.delete(OOG,3,1)}       # kolom 3 schrappen: 5 ringpixels, symmetrisch ovaal
# scheel-variant: pupilkolom (7/5) 1 px naar rechts schuiven binnen de ring, pixels uit hetzelfde oog (wissel kolom 2 en 3 in rij 2-3)
sc=LINKS['c4'].copy(); sc[2:4,[1,2,3]]=sc[2:4,[3,1,2]]; LINKS['c4_pupil']=sc
ozone=np.zeros((64,64),bool); ozone[39:44,13:18]=True; ozone[39:45,28:33]=True
res={}
for ln,lo in LINKS.items():
    A=A2.copy(); A[ozone]=kaal[ozone]                     # oude ogen weg -> lijf
    oog=zet(A,lo,39,13)|zet(A,OOG,40,28)                  # links x13-16 rij 39-43, rechts x28-32 rij 40-44
    B2b=B2.copy(); B2b[ozone]=A[ozone]                    # zelfde ogen in de B-basis
    for s in (1.15,1.30):
        B,niet,over,vak=maak(A,B2b,oog,s)
        tag=f'B{int(round(s*100))}_{ln}'
        np.save(tag+'.npy',B); save(B,tag+'.png')
        print(tag,'| px niet uit geschaalde mond',niet,'| oogpx die mond zou bedekken',over,
              '| diff buiten oog+mondzone t.o.v. r2/B',((B!=B2)&~(vak|ozone)).sum())
        res[tag]=B
for ln in LINKS: print(ln); print('\n'.join(''.join('.#'[0] if v==6 else 'Ayp5o'[[10,9,7,5].index(v)] if v in (10,9,7,5) else '.' for v in r) for r in LINKS[ln]))
