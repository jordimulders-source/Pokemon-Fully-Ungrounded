import sys, json, numpy as np; from PIL import Image
PAL=json.load(open('palet_r2.json')); a=np.load(sys.argv[1]).astype('uint8')
im=Image.fromarray(a,'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save(sys.argv[2],transparency=0)
