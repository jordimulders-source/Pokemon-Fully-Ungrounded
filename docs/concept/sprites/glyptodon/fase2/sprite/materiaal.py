# materiaal per natieve cel: K lijn, S stekel, R band, B schild, E schildrand/strepen beige, O oog, G grijs (lijf/staartpunt), T staart
import sys; sys.path.insert(0,'../gereedschap')
import numpy as np
from kaart import klasse
def materiaal(nat,bron):
    M=np.full((100,100),'.')
    for y in range(100):
        for x in range(100):
            c=nat[y,x]; k=klasse(c); b=bron[y,x]
            if k=='.': continue
            r,g,bb=[int(v) for v in c]
            if k=='K': M[y,x]='K'; continue
            if r>170 and g<160 and r-bb>80: M[y,x]='O'; continue
            if b=='3': M[y,x]='G' if k in 'Gg' else 'T'; continue
            if b=='6' and y<=27 and x<=36 and k in 'EYBg' and not (y>=23 and x>=33): M[y,x]='S'; continue
            if k in 'Gg': M[y,x]='G'; continue
            if k in 'EY': M[y,x]='E'; continue
            M[y,x]='B'
    return M
if __name__=='__main__':
    nat=np.load('comp_nat.npy'); bron=np.load('comp_bron.npy'); M=materiaal(nat,bron)
    np.save('mat_nat.npy',M)
    for y in range(5,90): print(f'{y:3d} '+''.join(M[y,3:97]))
