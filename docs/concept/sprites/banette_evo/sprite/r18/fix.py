# r18 = r17 + gat dicht dat Jordi aanwees (transparant zakje (6,26)-(6,27) tussen draad x5 en oorlijn x7).
# Oorlijn schuift daar naar x6 (sluit aan op x6 bij y25 en y28-30), x7 wordt oorvulling.
from PIL import Image; import numpy as np
im=Image.open('../r17/banette_evo.png'); a=np.array(im); pal=im.getpalette()
for (x,y),v in {(6,26):1,(6,27):1,(7,26):2,(7,27):2}.items(): a[y,x]=v
out=Image.fromarray(a.astype('uint8'),'P'); out.putpalette(pal); out.save('banette_evo.png',transparency=0)
