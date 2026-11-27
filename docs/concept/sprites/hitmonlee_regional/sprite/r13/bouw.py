# r13 = r12 + I: glasrand (prompt: "thin bright rim of light along the edges"). Binnenrandpixel (1 px binnen de buitenlijn)
#   waar de twee lichtste natieve pixels van het blok wit/bleek zijn (M_2e in 9,10,15) en de pixel nu rood glas is
#   (3,4,11) -> 12 (bleekroze). Alleen waar het model die rand heeft. Gelogd.
from PIL import Image; import numpy as np, sys
from scipy import ndimage
D='docs/concept/sprites/hitmonlee_regional/sprite/'
sys.path.insert(0,D); from toon import save_idx, save_p64
PAL=eval(open(D+'r4/bouw.py').read().split('PAL=')[1].split(']')[0]+']')
L=np.load(D+'r12/idx.npy').copy(); F=L>0
inner=ndimage.binary_erosion(F)&~ndimage.binary_erosion(F,iterations=2)
M2=np.load(D+'M_2e.npy')
log=open(D+'r13/log.txt','w'); n=0
for y,x in zip(*np.where(inner&np.isin(M2,[9,10,15])&np.isin(L,[3,4,11]))):
    log.write(f'({x},{y}) {L[y,x]}->12 I glasrand\n'); L[y,x]=12; n+=1
print('I',n)
np.save(D+'r13/idx.npy',L); save_p64(L,PAL,D+'r13/sprite.png'); save_idx(L,PAL,D+'r13/r13_10x.png',10)
