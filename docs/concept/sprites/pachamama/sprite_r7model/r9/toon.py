import sys, numpy as np
from PIL import Image
o=np.load(sys.argv[1]) if sys.argv[1].endswith('.npy') else np.array(Image.open(sys.argv[1]))
m=np.load('docs/concept/sprites/pachamama/sprite_r7model/r9/masker.npy')
print('   '+''.join(str(c%10) for c in range(18,42)))
for r in range(11,33): print('%2d '%r+''.join((('%x'%o[r,c]) if m[r,c] else ('·' if o[r,c] else ' ')) for c in range(18,42)))
