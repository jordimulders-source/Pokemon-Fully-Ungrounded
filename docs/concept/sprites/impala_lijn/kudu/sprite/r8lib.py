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
hx=lambda h: tuple(int(h[i:i+2],16) for i in (1,3,5))
PAL={'.':(0,0,0),'0':hx('#302418'),'L':hx('#F8D888'),'M':hx('#D8A850'),'D':hx('#A07030'),
     'l':hx('#D8AC30'),'m':hx('#B08824'),'d':hx('#7C5A10'),'A':hx('#4A4A52'),'3':hx('#8A8A92'),'4':hx('#C8C8CC'),
     'W':hx('#FFFFFF'),'R':hx('#E0A090'),'r':hx('#B06A58'),'K':hx('#5C4434')}
ORDER=list(PAL)
def png(g,pad,schaal=1):
    H,W=len(g),len(g[0]); OX=(64-W)//2; OY=64-H
    img=np.zeros((64,64),'uint8')
    for y in range(H):
        for x in range(W): img[OY+y,OX+x]=ORDER.index(g[y][x])
    pal=[v for k in ORDER for v in PAL[k]]; pal+=[0]*(48-len(pal))
    im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(pad,transparency=0)
    return im
def rgba8(g,bg=(255,255,255)):
    H,W=len(g),len(g[0]); OX=(64-W)//2; OY=64-H
    im=Image.new('RGB',(64,64),bg)
    for y in range(H):
        for x in range(W):
            if g[y][x]!='.': im.putpixel((OX+x,OY+y),PAL[g[y][x]])
    return im
