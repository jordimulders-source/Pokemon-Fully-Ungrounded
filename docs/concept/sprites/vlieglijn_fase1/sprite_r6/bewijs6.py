# bewijs: r6 tegen r5 B; elke afwijking moet in het potengebied liggen (onder de onderrand van borststuk/achterlijf)
import numpy as np
r5=np.loadtxt('../sprite_r5/vlieg_r5_B.txt',dtype=int); basis=np.loadtxt('../sprite_r5/r5_basis_vol.txt',dtype=int)
POOT={7,8,9,10,11,12,14,15}
# potengebied: pixels met y>=41 die in r5 B leeg zijn of een pootkleur/lijn naast een pootkleur hebben (geen lijfkleur 2-6)
def pootgebied(x,y):
    if y<41: return False
    return r5[y,x] in POOT|{0,1} 
for n in ('A1','A2'):
    f=np.loadtxt(f'vlieg_r6_{n}.txt',dtype=int); d=[(x,y) for y,x in zip(*np.where(f!=r5))]
    buiten=[p for p in d if not pootgebied(*p)]
    oud=[p for p in d if r5[p[1],p[0]]!=basis[p[1],p[0]]]
    voet=[p for p in d if p[0]>=45]
    voor=[p for p in d if p[0]<25]
    nieuw=[p for p in d if p not in oud and p not in voet and p not in voor]
    print(f'{n}: anders dan r5 B {len(d)} px; buiten potengebied {len(buiten)} {buiten}')
    print(f'   oude verre middenpoot weg {len(oud)}, nieuwe verre middenpoot {len(nieuw)} (bbox x{min(p[0] for p in nieuw)}-{max(p[0] for p in nieuw)} y{min(p[1] for p in nieuw)}-{max(p[1] for p in nieuw)}), achtervoet {len(voet)}, lijn boven klauwtjes voorpoten {len(voor)}')
    # losse pixels en open randen in het potengebied
    los=[(x,y) for y in range(41,63) for x in range(1,63) if f[y,x] and not any(f[y+a,x+b] for a,b in((1,0),(-1,0),(0,1),(0,-1)))]
    open_=[(x,y) for y in range(41,63) for x in range(1,63) if f[y,x]>1 and any(f[y+a,x+b]==0 for a,b in((1,0),(-1,0),(0,1),(0,-1)))]
    print(f'   losse pixels {los}; kleur tegen transparant (open rand) {open_}')
    print('   kleuren',len(set(f.ravel()))-1)
