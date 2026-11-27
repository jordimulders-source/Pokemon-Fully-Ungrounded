# r7: gezicht per spritecel gemeten op het natieve model (kaart: natief x=3*sx+3, y=3*sy-9; donker L<70).
# Ogen/neus/lijnen staan nu op de modelcellen (in r3-r6 1 px te ver rechts). Jordi's belangrijke lijnen:
# oogringen, neus (lichte rug x26, rechterzijde x27, onderkant x26-27), mond-∩ (top x26-28 y23, poten x25/x29),
# wanglijnen (links x24 y22-23, rechts x32 y21 -> x31 y22 -> x30 y23). Mondtop 1 rij lager dan het model (y23 i.p.v. y22),
# anders valt hij samen met de neusonderkant. Gezichtscontour links x22 (model), hoodkleur x21.
from PIL import Image; import numpy as np
im=Image.open('../r4/pachamama_r4.png'); a=np.array(im)
G={17:(23,'1234441222'),
18:(23,'1114411112'),
19:(21,'4161423616322'),
20:(21,'4123341334434'),
21:(21,'413331133331'),
22:(21,'514134433314'),
23:(21,'513131113133'),
24:(21,'513214331332'),
25:(21,'512313331332'),
26:(21,'51231432212'),
27:(24,'22333122')}
for y,(x0,s) in G.items():
    for i,c in enumerate(s):
        if c!=' ': a[y,x0+i]=int(c,16)
out=Image.fromarray(a,'P'); out.putpalette(im.getpalette()); out.save('pachamama_r7.png',transparency=0)
