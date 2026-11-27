# Ronde 8 gereedschap: Arcanine/Growlithe-vacht 1-op-1 stempelen in de manenzone van de kudu.
import json, numpy as np
from PIL import Image
GP='../../../../../../graphics/pokemon/'
def src(n):
    a=np.array(Image.open(GP+n+'/anim_front_gba.png'))[:64]
    return [''.join('.' if v==0 else '0123456789abcdef'[v] for v in r) for r in a]
ARC=src('arcanine'); GRO=src('growlithe')
# omkleuren naar de manentinten van de kudu (r7-palet): licht l, midden m, lijn d, zwart 0
MAP={'arcanine':{'7':'l','8':'l','9':'m','a':'d','f':'0'},
     'growlithe':{'1':'l','7':'l','8':'m','9':'m','a':'d','f':'0'}}
R6=[list(r) for r in json.load(open('r6/grid.json'))['grid']]
R7=[list(r) for r in json.load(open('r7/grid.json'))['grid']]
KAAL=json.load(open('r6/grid.json'))['kaal']
H,W=len(R6),len(R6[0])
HAAR={(x,y) for y in range(23,48) for x in range(0,33) if R6[y][x] in 'lmd'}
ZONE={(x+a,y+b) for x,y in HAAR for a in(-1,0,1) for b in(-1,0,1)}|{(22,43)}
class Bouw:
    def __init__(s):
        s.g=[r[:] for r in R6]; s.bron={}
        for x,y in HAAR: s.g[y][x]='?'
    def stempel(s,naam,x0,y0,x1,y1,dx,dy,flip=False,label=None,alleen=None):
        S=ARC if naam=='arcanine' else GRO; M=MAP[naam]; n=0
        for sy in range(y0,y1+1):
            for sx in range(x0,x1+1):
                c=S[sy][sx]
                if c not in M: continue
                tx=(dx+(x1-sx) if flip else dx+(sx-x0)); ty=dy+(sy-y0)
                if (tx,ty) not in ZONE: continue
                if alleen and (tx,ty) not in alleen: continue
                cur=s.g[ty][tx]
                if (tx,ty) in HAAR or cur in '.0?' :
                    s.g[ty][tx]=M[c]; s.bron[(tx,ty)]=(label or naam,sx,sy); n+=1
        return n
    def rest(s,buiten='.',lijf='M'):
        # niet-gedekte haarpixels: aan de buitenkant achtergrond, anders lijf (hals/schouder)
        out=set()
        for x,y in HAAR:
            if s.g[y][x]=='?': out.add((x,y))
        return out
    def grid(s): return [''.join(r) for r in s.g]
def toon(g,y0=21,y1=49,x1=36):
    print('   '+''.join(str(x%10) for x in range(x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(g[y][:x1]))
