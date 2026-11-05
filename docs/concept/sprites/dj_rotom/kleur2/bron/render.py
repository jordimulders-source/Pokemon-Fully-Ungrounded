import sys, numpy as np
sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/tools/concept/sprites')
from ascii_sprite import parse
from PIL import Image
from palet import COLS
V=sys.argv[1]
a=parse('dj_rotom_%s.txt'%V)[0]
im=Image.fromarray(a.astype('uint8'),'P'); p=[]
for c in COLS: p+=list(c)
im.putpalette(p+[0]*(768-len(p))); im.save('../dj_rotom_%s.png'%V,transparency=0)
