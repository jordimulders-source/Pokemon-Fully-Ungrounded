# png.py raster.txt uit.png [S] : geindexeerde PNG (index 0 transparant) + optioneel vergroot RGBA
import sys,numpy as np; from PIL import Image
from kaal_pal import PAL
a=np.loadtxt(sys.argv[1],dtype=int); im=Image.new('P',(64,64)); im.putpalette([v for c in PAL for v in c]); im.putdata(a.flatten().tolist())
im.save(sys.argv[2],transparency=0)
if len(sys.argv)>3:
    S=int(sys.argv[3]); r=Image.open(sys.argv[2]).convert('RGBA').resize((64*S,64*S),Image.NEAREST); r.save(sys.argv[2].replace('.png',f'_{S}x.png'))
