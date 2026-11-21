# klassenraster -> geïndexeerde PNG's (index 0 transparant) per paletvariant
import numpy as np, sys; from PIL import Image; from palet import pal, VARIANT
src=sys.argv[1] if len(sys.argv)>1 else 'tango_kls.npy'; o=np.load(src).astype('uint8')
def save(p,naam):
    im=Image.fromarray(o,'P'); fl=[c for t in p for c in t]; im.putpalette(fl+[0]*(768-len(fl))); im.save(naam,transparency=0)
for v in VARIANT: save(pal(v),'tango_%s.png'%v)
save(pal('model'),'tango_modelkleur.png')
print('kleuren',len(set(o.ravel()))-1)
