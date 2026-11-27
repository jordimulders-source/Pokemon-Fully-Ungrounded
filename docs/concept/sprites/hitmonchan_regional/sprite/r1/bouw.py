# r1: kale reductie = gekwantiseerd natief raster (15 modelkleuren) met geschrapte rijen/kolommen (schrap.py). Niets getekend.
import numpy as np, sys
D='docs/concept/sprites/hitmonchan_regional/sprite/'
sys.path.insert(0,D); from toon import save_idx, save_p64; from schrap import schrap
q=np.load(D+'natief_q.npy'); rd,cd,kr,kc=schrap(q)
pal=eval(open(D+'pal.txt').read())
S=q[np.ix_(kr,kc)]
np.save(D+'r1/idx.npy',S)
save_p64(S,pal,D+'r1/sprite.png'); save_idx(S,pal,D+'r1/r1_8x.png',8)
