import sys, numpy as np
from PIL import Image
CH = '.1234qrsxyzABCwk'
a = np.array(Image.open(sys.argv[1])); f = int(sys.argv[2])
fr = a[f*64:(f+1)*64]
for y in range(64):
    print('%2d ' % y + ''.join(CH[v] for v in fr[y]))
