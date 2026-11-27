# r3: gezicht per spritepixel door Claude tegen het model (natief, 36x) gezet; bouwt vanaf r2.
from PIL import Image; import numpy as np
im=Image.open('../r2/pachamama_r2.png'); a=np.array(im)
# (rij, startkolom, waarden)
G={17:(25,'2'),
18:(24,'11443111'),
19:(23,'261443616221'),
20:(23,'162443362622'),
21:(22,'223444434332'),
22:(22,'223322243232'),
23:(23,'23244332332'),
24:(23,'23323332332'),
25:(23,'23332323322'),
26:(24,'233323322'),
27:(24,'22332222')}
for y,(x0,s) in G.items():
    for i,c in enumerate(s): a[y,x0+i]=int(c,16)
out=Image.fromarray(a,'P'); out.putpalette(im.getpalette()); out.save('pachamama_r3.png',transparency=0)
