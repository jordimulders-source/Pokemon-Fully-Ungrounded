# klassenraster -> geïndexeerde PNG's (index 0 transparant): tango.png (r7) + tango_r7_donker.png
import numpy as np, sys; from PIL import Image; from palet import pal
o=np.load(sys.argv[1] if len(sys.argv)>1 else 'tango_r7.npy').astype('uint8')
def save(p,naam):
    im=Image.fromarray(o,'P'); fl=[c for t in p for c in t]; im.putpalette(fl+[0]*(768-len(fl))); im.save(naam,transparency=0)
save(pal('r7'),'tango.png'); save(pal('r7_donker'),'tango_r7_donker.png'); print('kleuren in gebruik',len(set(o.ravel()))-1)
