# Oog + ooglid 2x2 -> 1 uit het natieve raster ("donkerste wint" voor lijnen).
from klas import *
def blok(ks):
    nr=sum(k in 'rR' for k in ks); nk=ks.count('K'); nl=ks.count('L'); nc=ks.count('c'); ng=sum(k in 'gw' for k in ks)
    if nr>=2: return 'r' if ks.count('r')>ks.count('R') else 'R'
    if nk>=2: return 'K'
    if nk+nl>=2 or (nl>=1 and nk>=1): return 'L'
    if ng>=3: return 'g'
    if ks.count('A')>=2: return 'A'
    if nl==1 and nc>=1: return 'L'
    if nc>=2: return 'c'
    if nr==1 and nk==1: return 'K'
    pl=[k for k in ks if k in 'aAb']
    return max(set(pl),key=pl.count) if pl else ('c' if nc else ('L' if nl else 'g'))
def red(x0,y0,w,h):
    return [''.join(blok([klas(N[y0+2*j+a,x0+2*i+b]) for a in (0,1) for b in (0,1)]) for i in range(w)) for j in range(h)]
if __name__=='__main__':
    for nm,(x0,y0,w,h) in {'L':(61,84,8,9),'R':(84,86,9,10)}.items():
        for fy in (0,1):
            for fx in (0,1):
                print(nm,fx,fy); [print('   ',r) for r in red(x0+fx,y0+fy,w,h)]
