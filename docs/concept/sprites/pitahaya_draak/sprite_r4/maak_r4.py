# r4 = r3 + MOET eindkeuring r3 (6 wissels). Ook toepasbaar op oogvarianten (alle buiten het ooggebied).
import sys
from PIL import Image
import numpy as np
W=[(35,19,3,4),(37,10,3,4),(29,18,3,4),(36,15,3,4),(41,24,2,3),(41,42,8,10)]
src=sys.argv[1] if len(sys.argv)>1 else 'sprite_r3/pitahaya_r3.png'
dst=sys.argv[2] if len(sys.argv)>2 else 'sprite_r4/pitahaya_r4.png'
im=Image.open(src); a=np.array(im)
for x,y,o,n in W:
    assert a[y,x]==o,(x,y,a[y,x],o); a[y,x]=n
out=Image.fromarray(a,'P'); out.putpalette(im.getpalette()); out.save(dst,transparency=0); print('ok',dst)
