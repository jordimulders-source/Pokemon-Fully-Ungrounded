# meet.py (ook N_donker: aantal natieve lijnpixels (gem.<80) per spritepixel; ook M_2e: op een na lichtste natieve pixel; ook M_zonderlijn: gemiddelde van de natieve pixels zonder lijn (L*>=40) en zonder achtergrond): per spritepixel de modelkleur als (a) gemiddelde van de 2x2 natieve pixels, (b) donkerste, (c) lichtste,
# telkens als dichtstbijzijnde paletindex (Lab). Slaat M_gem, M_donker, M_licht op (64x59) voor reparaties.
from PIL import Image; import numpy as np, sys
D='docs/concept/sprites/hitmonlee_regional/sprite/'
sys.path.insert(0,D); from toon import lab
PAL=eval(open(D+'r4/bouw.py').read().split('PAL=')[1].split(']')[0]+']')
PL=lab(np.array(PAL[1:],float))
RD=[4,8,13,17,22,28,45,55,64,70]; CD=[1,5,16,37,42,50,56,60,65]
keepr=[r for r in range(74) if r not in RD]; keepc=[c for c in range(68) if c not in CD]
nat=np.asarray(Image.open(D+'natief.png').convert('RGB')).astype(float)
nl=lab(nat)
def idx(c): return int(((PL-lab(np.array(c,float)))**2).sum(1).argmin())+1
G=np.zeros((64,59),int); Dk=G.copy(); Li=G.copy(); NL=G.copy(); T2=G.copy(); NDK=G.copy()
for y,r in enumerate(keepr):
    for x,c in enumerate(keepc):
        blk=nat[2*r:2*r+2,2*c:2*c+2].reshape(-1,3); l=nl[2*r:2*r+2,2*c:2*c+2,0].ravel()
        G[y,x]=idx(blk.mean(0)); Dk[y,x]=idx(blk[l.argmin()]); Li[y,x]=idx(blk[l.argmax()])
        m=(l>=40)&(blk.min(1)<226)
        NDK[y,x]=int(((blk.mean(1)<80)&(blk.min(1)<226)).sum())
        T2[y,x]=idx(blk[np.argsort(l)[-2]])
        NL[y,x]=idx(blk[m].mean(0)) if m.any() else Dk[y,x]
np.save(D+'M_gem.npy',G); np.save(D+'M_donker.npy',Dk); np.save(D+'M_licht.npy',Li); np.save(D+'M_zonderlijn.npy',NL); np.save(D+'M_2e.npy',T2); np.save(D+'N_donker.npy',NDK)
