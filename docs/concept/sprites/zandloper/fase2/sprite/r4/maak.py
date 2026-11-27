# r4 = r3 + de 3 laatste keurderpunten (alleen tinten uit het model, silhouet gelijk).
import os; from PIL import Image; import numpy as np
d=os.path.dirname(os.path.abspath(__file__))
im=Image.open(os.path.join(d,'../r3/zandloper_fase2_r3.png')); a=np.array(im)
for x,y,v in [(15,43,12),(14,44,12),(15,44,12),(16,44,13),(15,45,13),(29,54,4),(31,32,6),(32,32,6)]: a[y,x]=v
o=Image.fromarray(a,'P'); o.putpalette(im.getpalette()); o.save(os.path.join(d,'zandloper_fase2_r4.png'),transparency=0)
print('kleuren',len(set(a[a>0].ravel())))
