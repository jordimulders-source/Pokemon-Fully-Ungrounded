# toon.py in.npy uit.png x0 y0 x1 y1 K: npy (indexen) -> png met r14-palet, plus uitsnede naast het model (zoom.py)
import sys, numpy as np, subprocess; from PIL import Image
a=np.load(sys.argv[1]).astype('uint8'); im=Image.fromarray(a,'P'); im.putpalette(Image.open('../r14/hoatzin.png').getpalette())
im.info['transparency']=0; im.save('_t.png', transparency=0)
subprocess.run(['python3','zoom.py','_t.png']+sys.argv[2:])
