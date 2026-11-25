# npy (H x 64) -> png 64x64 (7 px marge onder) + 8x
import numpy as np, sys; from PIL import Image
o=np.load(sys.argv[1]); PAL=np.load('pal.npy'); H=o.shape[0]; from cfg import TOP
full=np.zeros((64,64),int); full[TOP:TOP+H]=o
im=Image.fromarray(full.astype('uint8'),'P'); pal=[int(v) for c in PAL for v in c]; im.putpalette(pal+[0]*(768-len(pal))); im.save(sys.argv[2],transparency=0)
im.convert('RGB').resize((512,512),Image.NEAREST).save(sys.argv[2].replace('.png','_8x.png'))
