# Jordi (25 nov): "de ogen en mond in 3 wat minder duidelijk dan in 2, die mogen precies dezelfde kleuren
# gebruiken, nu lijken ze wat doffer" -> gezichtskleuren van fase 3 vervangen door de paletkleuren van fase 2.
import sys; from PIL import Image; import numpy as np
IN, OUT = sys.argv[1], sys.argv[2]
MAP = {(51, 224, 208): (18, 240, 247),   # cyaan
       (70, 34, 34): (74, 24, 27), (81, 35, 29): (74, 24, 27),   # donkerrode oogkassen
       (118, 126, 79): (221, 252, 70),   # dof geel in de monden -> geel van fase 2
       (199, 230, 105): (221, 252, 70)}  # geel van ogen/mond (het foutkleurbalkje 248,240,64 blijft)
a = np.asarray(Image.open(IN).convert('RGBA')).copy()
for k, v in MAP.items():
    m = (a[..., :3] == k).all(2) & (a[..., 3] > 0); a[m, :3] = v
Image.fromarray(a).save(OUT)
