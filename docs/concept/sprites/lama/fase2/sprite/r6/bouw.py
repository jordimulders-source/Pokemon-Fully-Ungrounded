# r6 = r5 + kleed-binnenkant van r4b (Jordi: "ik vind wat de vorige ronde probeerde te doen nog wel netjes op zich,
# daardoor iets minder kaal") + achterste poot geleidelijker ("heeft nog wel een duidelijke streep, die geleidelijker mag")
from PIL import Image; import numpy as np
r5=Image.open('r5/lama.png'); a=np.array(r5); b=np.array(Image.open('r4/lama_b.png'))
O=a.copy(); RED={9,10,11}
# 1. kleed: binnenkant uit r4b waar beide rood zijn (silhouet en kleedrand van r5 blijven)
for y in range(27,42):
    for x in range(26,46):
        if a[y,x] in RED and b[y,x] in RED: O[y,x]=b[y,x]
# 2. achterste poot (x 46-53, rij 46-61): lichte middenstreep (3) loopt nu door; naar beneden geleidelijk naar 2
for y in range(46,62):
    for x in range(44,54):
        if a[y,x]==3:
            if y>=56: O[y,x]=2
            elif y>=53 and (x+y)%2==0: O[y,x]=2
# overgang lijf -> poot (rij 47-49) geleidelijker: schuine grens i.p.v. vlakke band
for y in range(46,50):
    for x in range(40,52):
        v=a[y,x]
        if v in (3,4):
            t=(y-47.5)+(x-44)/4.0
            O[y,x]=4 if t<-0.3 else (3 if t<1.2 else 2)
out=Image.fromarray(O,'P'); out.putpalette(r5.getpalette()); out.save('r6/lama.png',transparency=0)
assert ((O>0)==(a>0)).all(); print('veranderd',(O!=a).sum())
