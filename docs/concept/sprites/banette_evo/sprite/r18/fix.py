# r18 = r17 + Jordi's geel gestipte pixel (8,24): donkergrijs ingesloten door zwart las als gat.
# Mutsrand loopt nu op x8 door t/m y24; (9,24) wordt mutsvulling. (Eerdere r18-poging op (6,26-27) was de verkeerde plek.)
from PIL import Image; import numpy as np
im=Image.open('../r17/banette_evo.png'); a=np.array(im); pal=im.getpalette()
for (x,y),v in {(8,24):1,(9,24):3}.items(): a[y,x]=v
out=Image.fromarray(a.astype('uint8'),'P'); out.putpalette(pal); out.save('banette_evo.png',transparency=0)
