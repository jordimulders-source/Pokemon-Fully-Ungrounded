# Tekstraster van een geindexeerde sprite: . = 0, 1-9, a-f = 10-15. Kolomkop = x mod 10.
import sys; import numpy as np; from PIL import Image
a = np.asarray(Image.open(sys.argv[1])); x0 = int(sys.argv[2]) if len(sys.argv) > 2 else 0; x1 = int(sys.argv[3]) if len(sys.argv) > 3 else 64
print('   ' + ''.join(str(x % 10) for x in range(x0, x1)))
for y in range(64): print('%2d ' % y + ''.join('.123456789abcdef'[v] if v else '.' for v in a[y, x0:x1]))
