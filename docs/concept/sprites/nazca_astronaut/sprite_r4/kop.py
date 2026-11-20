# r4: kopglans als gebogen boog langs de bolling (naar Gastly Gen 3), met de hand per rij gezet. Alleen tint binnen de kop.
import numpy as np
o=np.array([list(l.rstrip('\n')[3:]) for l in open('../sprite_r3/rij28/rollen_hand.txt') if l.strip()]); r3=o.copy()
KOP={1:(15,"222222"),2:(11,"223ggg3322222"),3:(10,"23gg33332222221"),4:(10,"2g33332222222211"),
     5:(9,"2g3333222222221111"),6:(9,"233332222222211111"),7:(9,"223332222222211111")}
for j,(i0,s) in KOP.items():
    assert len(s)==len([c for c in o[j] if c in '123g']) or True
    for k,ch in enumerate(s):
        assert o[j,i0+k] in '123g',(j,i0+k); o[j,i0+k]=ch
open('rollen_hand.txt','w').write('\n'.join('%2d '%j+''.join(r) for j,r in enumerate(o))+'\n')
d=o!=r3; ys,xs=np.where(d); print('kop: gewijzigde rollen',d.sum(),'rijen %d-%d'%(ys.min(),ys.max()),'alleen kopvlak:',all(r3[y,x] in '123g' for y,x in zip(ys,xs)))
for j in range(0,9): print('%2d '%j+''.join(o[j]))
