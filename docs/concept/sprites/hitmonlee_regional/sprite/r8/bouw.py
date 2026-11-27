# r8 = r7 + E: voetkussentjes, teentjes en duimglans per pixel uit de natieve 2x2-blokken (lijst hieronder, gelogd).
from PIL import Image; import numpy as np, sys
D='docs/concept/sprites/hitmonlee_regional/sprite/'
sys.path.insert(0,D); from toon import save_idx, save_p64
PAL=eval(open(D+'r4/bouw.py').read().split('PAL=')[1].split(']')[0]+']')
L=np.load(D+'r7/idx.npy').copy()
log=open(D+'r8/log.txt','w')
def zet(x,y,k,why):
    assert L[y,x]>0, (x,y)
    if L[y,x]!=k: log.write(f'({x},{y}) {L[y,x]}->{k} {why}\n'); L[y,x]=k
E={ # trapvoet-kussentje: grijswit ovaal met donkere rand (natief ww/gg op 31-33 x 3b-5a)
   (31,3):14,(32,3):15,(30,4):13,(31,4):15,(32,4):10,(33,4):15,(34,4):1,(31,5):14,(32,5):15,(33,5):14,
    # standvoet-kussentje (natief wg/gg op 50-51 x 54-56)
   (50,54):13,(50,55):10,(51,55):14,(50,56):14,
    # teentjes standvoet (natief licht op 53, 55-56, 57; donkere naden ertussen)
   (52,61):1,(53,61):15,(54,61):1,(55,61):14,(56,61):1,(57,61):15,(58,61):1,
   (53,62):1,(54,62):1,(55,62):10,(56,62):14,(57,62):1,(58,62):1,(56,60):2,(57,60):15,
    # duimtop linkerhand: glans (natief lichtroze)
   (5,53):12}
for (x,y),k in E.items(): zet(x,y,k,'E voet/teen/duim')
np.save(D+'r8/idx.npy',L); save_p64(L,PAL,D+'r8/sprite.png'); save_idx(L,PAL,D+'r8/r8_10x.png',10)
