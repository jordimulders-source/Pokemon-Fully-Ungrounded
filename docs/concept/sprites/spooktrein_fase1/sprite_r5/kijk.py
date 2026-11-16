import sys,numpy as np; from PIL import Image
from toon import rgba
o=np.load(sys.argv[1]); im=rgba(o); w=Image.new('RGBA',(64,64),(255,255,255,255)); w=Image.alpha_composite(w,im).convert('RGB')
r4=rgba(np.load('../sprite_r4/sprite.npy')); w4=Image.alpha_composite(Image.new('RGBA',(64,64),(255,255,255,255)),r4).convert('RGB')
Z=10; V=Image.new('RGB',(2*58*Z+20+200,40*Z),(230,230,230))
V.paste(w.crop((2,24,60,64)).resize((58*Z,40*Z),Image.NEAREST),(0,0))
V.paste(w4.crop((2,24,60,64)).resize((58*Z,40*Z),Image.NEAREST),(58*Z+10,0))
V.paste(w.resize((128,128),Image.NEAREST),(2*58*Z+30,0)); V.paste(w,(2*58*Z+30,140))
V.save(sys.argv[2])
