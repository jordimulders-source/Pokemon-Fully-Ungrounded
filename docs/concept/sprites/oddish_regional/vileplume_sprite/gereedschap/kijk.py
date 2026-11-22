import sys; sys.path.insert(0,'gereedschap'); from gemeen import *; from PIL import Image; import numpy as np
im=Image.open(sys.argv[1]); o=np.asarray(im); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
img=np.full((64,64,3),255,'uint8')
for k in range(1,16): img[o==k]=pal[k]
a=Image.fromarray(img).resize((512,512),Image.NEAREST); b=model_op_schaal(8)
v=Image.new('RGB',(1032,512),'white'); v.paste(a,(0,0)); v.paste(b,(520,0)); v.save(sys.argv[2])
