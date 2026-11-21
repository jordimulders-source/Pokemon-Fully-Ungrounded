# cumbia_kls.npy -> cumbia.png (+ varianten) als geïndexeerde PNG, index 0 transparant
import numpy as np; from PIL import Image; from palet import pal, VARIANT
o=np.load('cumbia_kls.npy').astype('uint8')
def save(p,naam):
    im=Image.fromarray(o,'P'); fl=[c for t in p for c in t]; im.putpalette(fl+[0]*(768-len(fl))); im.save(naam,transparency=0)
save(pal('B_midden'),'cumbia_B_midden.png')
save(pal('model'),'cumbia_modelkleur.png')
import shutil; shutil.copy('cumbia_B_midden.png','cumbia.png')
print('kleuren',len(set(o.ravel()))-1)
