# r5: gezichtsvorm naar Jordi's rode lijnen op het model (27 nov): oogkassen als lussen, neus = twee lijnen + onderkant,
# mond als ∩ (bovenlijn + twee poten), wanglijnen van de zijkant naar de mond/kin. Claude per pixel; bouwt vanaf r4.
from PIL import Image; import numpy as np
im=Image.open('../r4/pachamama_r4.png'); a=np.array(im)
G={17:(24,'221412223'),
18:(24,'111411111'),
19:(23,'16114161612'),
20:(23,'12214122213'),
21:(23,'13311133331'),
22:(23,'21334433313'),
23:(23,'23111111312'),
24:(23,'23133331312'),
25:(23,'23133331122'),
26:(23,'221333311'),
27:(24,'21222212')}
for y,(x0,s) in G.items():
    for i,c in enumerate(s): a[y,x0+i]=int(c,16)
out=Image.fromarray(a,'P'); out.putpalette(im.getpalette()); out.save('pachamama_r5.png',transparency=0)
