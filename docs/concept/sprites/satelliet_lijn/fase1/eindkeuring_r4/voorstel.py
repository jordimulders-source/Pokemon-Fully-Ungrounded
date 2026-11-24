# Optioneel voorstel eindkeuring r4: 1 px. (41,35) P -> m (losse reflectiepixel in de schaduwsikkel).
import numpy as np
from PIL import Image
im=Image.open('../sprite_r4/sprite.png'); o=np.array(im); v=o.copy()
assert o[41,35]==3, o[41,35]
v[41,35]=8
assert ((v>0)==(o>0)).all() and int((v!=o).sum())==1
np.save('voorstel.npy',v)
out=Image.fromarray(v,'P'); out.putpalette(im.getpalette()); out.save('voorstel.png',transparency=0)
print('diff 1 px, silhouet gelijk')
