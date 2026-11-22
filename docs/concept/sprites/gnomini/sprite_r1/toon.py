# toon.py SPRITE.png : tekstraster (. transp, # zwart, muts abcd+e, roze ABCD (donker..licht), blauw wxyz)
import sys, numpy as np; from PIL import Image
o=np.asarray(Image.open(sys.argv[1])); CH='.#abcdABCDwxyz'
yy,xx=np.where(o>0); x0,x1=xx.min()-1,xx.max()+2
print('   '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(yy.min()-1,yy.max()+2): print('%2d '%y+''.join(CH[v] for v in o[y,x0:x1]))
