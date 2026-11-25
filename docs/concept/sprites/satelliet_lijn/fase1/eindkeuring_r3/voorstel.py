# Optionele micro-reparatie (geen voorwaarde voor PASS): dither "p P p" op de bovenrand van antenne 3.
# Draaien vanuit fase1/eindkeuring_r3/.
import numpy as np
from PIL import Image
im=Image.open('../sprite_r3/sprite.png'); o=np.array(im).copy(); src=o.copy()
P,p=3,4
assert o[33,54]==p and o[33,55]==P and o[33,56]==p
o[33,55]=p                      # (33,55): P -> p  => 'ppp' glim van 3 px i.p.v. p P p
assert ((o>0)==(src>0)).all()   # silhouet gelijk
print('diff px:',int((o!=src).sum()))
np.save('voorstel.npy',o)
out=Image.fromarray(o.astype(np.uint8),'P'); out.putpalette(im.getpalette()); out.save('voorstel.png',transparency=0)
