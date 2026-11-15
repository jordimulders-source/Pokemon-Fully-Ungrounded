# Eén variant naast het model, kop op z (geen raster), plus 2x en 1x. python3 paar.py out z a.npy [b.npy]
import sys,numpy as np
from PIL import Image
from toon6 import big
from zie import mod, F
out=sys.argv[1]; z=int(sys.argv[2]); fs=sys.argv[3:]; b=(0,0,24,24)
ims=[big(np.load(f)[b[1]:b[3],b[0]:b[2]],z,F,(255,255,255,255)) for f in fs]+[mod(b,z)]
V=Image.new('RGBA',(sum(i.width+6 for i in ims),ims[0].height),(255,255,255,255)); x=0
for im in ims: V.alpha_composite(im,(x,0)); x+=im.width+6
V.save(out)
