# Eindkeuring r2: alleen voeten, alleen tinten (Jordi: "kloppen de poten wel? zijn die niet te effen nu").
# Linkervoet: lichte rand 3 linksboven, kern 5, sikkel A rechtsonder. Rechtervoet: kapje 5 linksboven, kern A, sikkel 6 langs de onderrand.
import os,sys,numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(H,'..'))
import eind
for p in ('../../r6','../..','../../r2','../../r3','../../r5'): sys.path.insert(0,os.path.join(H,p))
from schets import delen
VOET={  # (x,y): tint
 **{(x,55):3 for x in range(23,27)}, (24,56):3,
 **{(x,55):5 for x in range(27,31)}, **{(x,56):5 for x in range(25,28)},
 (28,56):10, **{(x,57):10 for x in range(26,30)},
 **{(x,55):5 for x in range(31,35)}, **{(x,56):5 for x in range(31,34)},
 **{(x,59):6 for x in range(35,40)}, **{(x,58):6 for x in range(38,41)},
}
def bouw():
    S=eind.bouw(); D=delen()
    for (x,y),v in VOET.items():
        assert D[y,x] in ('voetL','voetR'),(x,y); S[y,x]=v
    return S
if __name__=='__main__':
    S=bouw(); print('t.o.v. r6 per klasse:',eind.check(S))
    E=eind.bouw(); D=delen(); d=S!=E
    print('t.o.v. eind:',int(d.sum()),'px, buiten voeten:',int((d&~np.isin(D,('voetL','voetR'))).sum()))
    from schets2 import clusters
    m=np.isin(D,('voetL','voetR'))&~np.isin(S,(7,))
    print('kleine vlakjes voeten:',[( '%X'%t,c) for t,c in clusters(S,m)])
    eind.save(S,os.path.join(H,'claydol_eind_r2'))
    for y in range(53,61): print(y,''.join('%X'%S[y,x] if S[y,x] else '.' for x in range(20,46)))
