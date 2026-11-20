# dump.py [png]: raster als tekst (index hex)
import sys, numpy as np
from PIL import Image
a = np.array(Image.open(sys.argv[1] if len(sys.argv) > 1 else 'hoatzin.png'))
y0, y1 = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, 64)
print('   ' + ''.join(str(x // 10) for x in range(64))); print('   ' + ''.join(str(x % 10) for x in range(64)))
for y in range(y0, y1): print('%2d ' % y + ''.join('.' if v == 0 else '0123456789ABCDEF'[v] for v in a[y]))
