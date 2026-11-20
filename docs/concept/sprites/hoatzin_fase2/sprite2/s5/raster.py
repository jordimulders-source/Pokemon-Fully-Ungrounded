# raster.py y0 y1 x0 x1 [png]: tekstraster van de sprite (paletindex als teken)
import sys, numpy as np
from PIL import Image
S = np.array(Image.open(sys.argv[5] if len(sys.argv) > 5 else 'hoatzin.png'))
y0, y1, x0, x1 = map(int, sys.argv[1:5]); ch = '.#abcdefghijklmn'
print('   ' + ''.join(str(i % 10) for i in range(x0, x1)))
for j in range(y0, y1): print('%2d ' % j + ''.join(ch[v] for v in S[j, x0:x1]))
