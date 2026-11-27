# r11 = r10 + H: rood glas en gloed als toonkaart uit het model (Gen 3-netheid: hele tintvlakken i.p.v. spikkels).
#   Per spritepixel: modelkleur natief gladgestreken (gauss sigma=S natieve px (1,0 gekozen uit 1,0/1,5/2,0), alleen
#   figuurpixels zonder lijnen), gemiddeld over het 2x2-blok. Materiaal: G-B > GRENS(40) of helderheid > 190 = gloed (5-9),
#   anders rood glas (3,4,11,12). Tint = dichtstbijzijnde kleur (Lab) binnen de materiaalreeks bij de gladgestreken modelkleur.
#   Niet aangeraakt: lijnen (1,2), glans 10, doorschijnend 13-15, oog-, ring-, kussentje-, teenzones.
# gebruik: bouw.py [S] [GRENS] [uitmap]
from PIL import Image; import numpy as np, sys, os
from scipy import ndimage
D='docs/concept/sprites/hitmonlee_regional/sprite/'
sys.path.insert(0,D); from toon import save_idx, save_p64, lab
PAL=eval(open(D+'r4/bouw.py').read().split('PAL=')[1].split(']')[0]+']')
S=float(sys.argv[1]) if len(sys.argv)>1 else 1.0
GRENS=float(sys.argv[2]) if len(sys.argv)>2 else 40
uit=sys.argv[3] if len(sys.argv)>3 else 'r11'
L=np.load(D+'r10/idx.npy').copy(); H,W=L.shape
RD=[4,8,13,17,22,28,45,55,64,70]; CD=[1,5,16,37,42,50,56,60,65]
keepr=[r for r in range(74) if r not in RD]; keepc=[c for c in range(68) if c not in CD]
nat=np.asarray(Image.open(D+'natief.png').convert('RGB')).astype(float)
lum=nat.mean(2); m=(nat.min(2)<226)&(lum>=80)
sm=np.stack([ndimage.gaussian_filter(np.where(m,nat[...,i],0),S) for i in range(3)],-1)/np.maximum(ndimage.gaussian_filter(m.astype(float),S),1e-6)[...,None]
C=np.zeros((H,W,3))
for y,r in enumerate(keepr):
    for x,c in enumerate(keepc): C[y,x]=sm[2*r:2*r+2,2*c:2*c+2].reshape(-1,3).mean(0)
VAST=np.zeros((H,W),bool)
VAST[11:23,30:50]=True; VAST[44:54,46:59]=True; VAST[24:34,16:30]=True
VAST[2:7,29:35]=True; VAST[53:57,49:52]=True; VAST[59:63,51:59]=True
doel=(L>0)&~np.isin(L,[1,2,10,13,14,15])&~VAST
gb=C[...,1]-C[...,2]; lu=C.mean(2)
isg=(gb>GRENS)|(lu>190)
gloed=doel&isg; glas=doel&~isg
PL=lab(np.array(PAL,float)); CL=lab(C)
def tonen(mask,ramp):
    d=((CL[mask][:,None,:]-PL[np.array(ramp)][None])**2).sum(-1)
    return np.array(ramp)[d.argmin(1)]
L0=L.copy()
L[glas]=tonen(glas,[3,4,11,12]); L[gloed]=tonen(gloed,[5,6,7,8,9])
print('S',S,'grens',GRENS,'gewijzigd',(L!=L0).sum(),'glas',glas.sum(),'gloed',gloed.sum())
os.makedirs(D+uit,exist_ok=True)
with open(D+uit+'/log.txt','w') as f:
    for y,x in zip(*np.where(L!=L0)): f.write(f'({x},{y}) {L0[y,x]}->{L[y,x]} H toonkaart\n')
np.save(D+uit+'/idx.npy',L); save_p64(L,PAL,D+uit+'/sprite.png'); save_idx(L,PAL,D+uit+'/'+uit+'_10x.png',10)
