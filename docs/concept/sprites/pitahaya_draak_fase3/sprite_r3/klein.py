# Model als 64x64 vlakgemiddelde (zelfde raster) naast sprites, op Z x. Gebruik: python3 klein.py Z UIT SPRITE...
import sys,numpy as np; from PIL import Image; from box import win
Z=int(sys.argv[1]); M=np.asarray(Image.open('../model/model.png').convert('RGB')).astype(float)
m=np.zeros((64,64,3))
for Y in range(64):
    for X in range(64):
        w=win(M,X,Y); m[Y,X]=w.mean(0) if len(w) else 255
ims=[Image.fromarray(m.astype('uint8'))]
for p in sys.argv[3:]:
    im=Image.open(p); im.save('/tmp/_k.png',transparency=0); t=Image.open('/tmp/_k.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(t); ims.append(bg.convert('RGB'))
out=Image.new('RGB',(len(ims)*(64*Z+8),64*Z),(200,200,200))
for i,im in enumerate(ims): out.paste(im.resize((64*Z,64*Z),Image.NEAREST),(i*(64*Z+8),0))
out.save(sys.argv[2])
