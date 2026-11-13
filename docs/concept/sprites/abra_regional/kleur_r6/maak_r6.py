# maak_r6.py: r5 (oog A) + beide ogen meer hangend zoals het model
# Jordi: "kan je beide ogen nog iets meer laten hangen? zoals in het model? Als het niet kan ook prima, de pose is al goed"
# Model (natief, gemeten): rechteroog (30.5,28)->(28,30.5), linkeroog (22.5,30)->(24,31): beide zakken naar de neus toe.
# A: rechteroog 45-gradendiagonaal (30,28)(29,29)(28,30); linkeroog (22,29)(23,30)+(24,31)
# B: alleen het rechteroog; linkeroog blijft r5
import numpy as np; from PIL import Image
K,B=1,9
src=Image.open('../kleur_r5/abra_r5.png'); a0=np.array(src).astype(int)
RECHTS=[((29,28),B),((28,29),B),((30,28),K),((29,29),K)]
EDITS={'A':RECHTS+[((24,31),K)],'B':RECHTS}
for n,ed in EDITS.items():
    a=a0.copy()
    for (x,y),v in ed: a[y,x]=v
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(src.getpalette())
    im.save(f'abra_r6_{n}.png',transparency=0)
