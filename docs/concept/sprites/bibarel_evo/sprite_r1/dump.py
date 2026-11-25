# dump.py SPRITE.png x0 y0 x1 y1 : indexkaart als tekst (0='.', 10..15 = a..f)
import sys,numpy as np; sys.path.insert(0,'sprite_r1'); from gemeen import *
o=laad(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6])
print('    '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%3d '%y+''.join('.' if v==0 else '%x'%v for v in o[y,x0:x1]))
