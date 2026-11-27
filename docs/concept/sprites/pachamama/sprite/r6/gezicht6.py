# r6: Jordi's rode lijnen als bogen i.p.v. vierkanten (Jordi over r5: "dit zijn vierkanten"): oogringen zonder hoekpixels,
# neus = U (zijlijnen + 1 punt onderaan), mond = ∩ met schuine schouder, wanglijnen schuin. Claude per pixel; bouwt vanaf r4.
from PIL import Image; import numpy as np
im=Image.open('../r4/pachamama_r4.png'); a=np.array(im)
G={17:(24,'223432223'),
18:(23,'11124211121'),
19:(23,'16114161612'),
20:(23,'11114111123'),
21:(23,'33331333331'),
22:(23,'31344433313'),
23:(23,'23111133312'),
24:(23,'23144413122'),
25:(23,'2313331312'),
26:(23,'221333312'),
27:(24,'22222222')}
for y,(x0,s) in G.items():
    for i,c in enumerate(s): a[y,x0+i]=int(c,16)
out=Image.fromarray(a,'P'); out.putpalette(im.getpalette()); out.save('pachamama_r6.png',transparency=0)
