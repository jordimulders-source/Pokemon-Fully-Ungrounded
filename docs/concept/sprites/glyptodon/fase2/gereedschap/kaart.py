import numpy as np
def klasse(c):
    r,g,b=[int(v) for v in c]; s=r+g+b
    if s>720: return '.'
    if s<150: return 'K'
    if abs(r-b)<14 and s<450: return 'G'
    if r>170 and r-b>25 and g>150 and r-g<25 and b<120: return 'Y'
    if r>160 and r-b>25: return 'E'
    if r-b>15: return 'B'
    return 'g'
def kaart(nat,x0,x1,y0,y1):
    print('    '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print(f'{y:3d} '+''.join(klasse(nat[y,x]) for x in range(x0,x1)))
