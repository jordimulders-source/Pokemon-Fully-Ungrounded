# per spritecel 4x4 submonsters van het origineel, als paletletter (W=wit bg)
import sys,numpy as np
from PIL import Image
from tools import P,CH
a=np.array(Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/nachtaap_fase3/gemini/gekozen_r4.png').convert('RGB')).astype(int)
Pa=np.array(P[1:])
x0,y0,x1,y1=map(int,sys.argv[1:5])
def c(p):
    if p.min()>247: return '.'
    return CH[1+((Pa-p)**2).sum(1).argmin()]
print('    '+''.join(('%-4d'%x)+'|' for x in range(x0,x1)))
for y in range(y0,y1):
    for sub in range(4):
        oy=16*y-1+2+4*sub
        print(('%2d  '%y if sub==0 else '    ')+'|'.join(''.join(c(a[oy,16*x-2+2+4*k]) for k in range(4)) for x in range(x0,x1)))
    print()
