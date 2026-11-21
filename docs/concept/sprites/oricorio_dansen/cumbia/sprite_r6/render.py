# cumbia_kls.npy -> cumbia.png (+ varianten) als geïndexeerde PNG, index 0 transparant
import numpy as np; from PIL import Image; from palet import pal, VARIANT
import sys
o=np.load(sys.argv[1] if len(sys.argv)>1 else 'cumbia_r6.npy').astype('uint8')
def save(p,naam):
    im=Image.fromarray(o,'P'); fl=[c for t in p for c in t]; im.putpalette(fl+[0]*(768-len(fl))); im.save(naam,transparency=0)
save(pal('r5'),'cumbia_r6.png')

import shutil; shutil.copy('cumbia_r6.png','cumbia.png')
print('kleuren',len(set(o.ravel()))-1)
