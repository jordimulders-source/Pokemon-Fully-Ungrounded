import sys,numpy as np; from PIL import Image
from toon import rgba
o=np.load(sys.argv[1]); w=Image.alpha_composite(Image.new('RGBA',(64,64),(255,255,255,255)),rgba(o)).convert('RGB')
w.crop((4,18,58,64)).resize((54*16,46*16),Image.NEAREST).save(sys.argv[2])
