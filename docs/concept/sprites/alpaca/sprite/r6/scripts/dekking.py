# dekking.py: per spritepixel de modeldekking (fractie voorgrond in het natieve model) naast r5-alfa, torsogebied
import numpy as np; from PIL import Image; from px import *
A=np.array(Image.open('../../r5/palpaca.png'))
def dek(x,y):
    ax,bx,ay,by=cell(x,y)
    z=Z[int(np.floor(ay)):int(np.ceil(by)),int(np.floor(ax)):int(np.ceil(bx))]
    return (z!='.').mean() if z.size else 0
print('    '+''.join('%3d'%x for x in range(16,48)))
for y in range(30,52):
    print('%3d '%y+''.join(('%3d'%int(dek(x,y)*99)) if True else '' for x in range(16,48)))
print('r5 alfa')
for y in range(30,52): print('%3d '%y+''.join('  #' if A[y,x] else '  .' for x in range(16,48)))
