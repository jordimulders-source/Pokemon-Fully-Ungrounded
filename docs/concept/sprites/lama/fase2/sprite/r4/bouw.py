# r4 = r3 (lijf, kop, kleding) + poten van Gemini r15 (Jordi: "De poten kan je grotendeels overnemen,
# alleen de voorpoten qua kleur boven de handschoenen zijn onnodig veranderd")
from PIL import Image; import numpy as np
r3=Image.open('r3/lama.png'); a=np.array(r3); b=np.array(Image.open('gemini_r15/r15_64.png'))
O=a.copy(); CUT=47
O[CUT:]=b[CUT:]
# kleur boven de handschoenen terug naar vacht: nabije voorpoot (licht) en verre voorpoot (donker)
NEAR={11:6,10:5,9:4,8:3}; FAR={11:4,10:4,9:3,8:2}
for y in range(CUT,57):
    for x in range(0,30):
        v=O[y,x]
        if v in (8,9,10,11):
            far = v in (8,9)
            if y>=55 and not far: continue      # nabije handschoen begint op rij 55
            O[y,x]=(FAR if far else NEAR)[v]
im=Image.fromarray(O,'P'); im.putpalette(r3.getpalette()); im.save('r4/lama.png',transparency=0)
