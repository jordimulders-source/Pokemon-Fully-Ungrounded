# acht.py SPRITE [SPRITE2] out: sprites op 8x naast elkaar (wit), voor snel kijken
import sys; sys.path.insert(0,'sprite_r6'); from gemeen2 import *; import numpy as np; from PIL import Image
ps=sys.argv[1:-1]; T=Image.new('RGB',(528*len(ps),424),'white')
for i,p in enumerate(ps): T.paste(rgb(np.array(Image.open(p)),(255,255,255)).crop((0,0,64,53)).resize((512,424),0),(i*528,0))
T.save(sys.argv[-1])
