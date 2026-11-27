# los.py A B: rode tintpixels (S/M/H) zonder 8-buur van dezelfde tint, nieuw in B t.o.v. A
import sys; sys.path.insert(0,'sprite_r9'); from hulp import *; import numpy as np; from PIL import Image
def single(a):
    return [(x,y,int(a[y,x])) for y in range(64) for x in range(64) if a[y,x] in (3,4,5) and not any(ok(y+dy,x+dx) and a[y+dy,x+dx]==a[y,x] for dy,dx in N8)]
a=np.array(Image.open(sys.argv[1])); b=np.array(Image.open(sys.argv[2])); sa,sb=single(a),single(b)
print(len(sa),len(sb),'nieuw',[p for p in sb if p not in sa])
