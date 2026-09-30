import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
REPO=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..'))
from gridrender import render
N=json.load(open(os.path.join(REPO,'data/tilesets/secondary/snow/metatile_names.json')))
class M:
    def __init__(s,W,H,base='snow'):
        s.W,s.H=W,H; s.g=[[N[base]]*W for _ in range(H)]; s.col=[[0]*W for _ in range(H)]; s.elev=[[3]*W for _ in range(H)]
    def put(s,x,y,n,c=None,e=None):
        if not(0<=x<s.W and 0<=y<s.H): return
        s.g[y][x]=N[n] if isinstance(n,str) else n
        if c is not None: s.col[y][x]=c
        if e is not None: s.elev[y][x]=e
    def plateau(s,x0,y0,w,h,face=1,open_=''):
        # open_: sides that continue past (no rim): n,s,w,e
        for y in range(y0,y0+h):
            for x in range(x0,x0+w):
                top=y==y0 and 'n' not in open_; bot=y>=y0+h-face and 's' not in open_
                l=x==x0 and 'w' not in open_; r=x==x0+w-1 and 'e' not in open_
                if bot:
                    n='cliff_b' if y==y0+h-face else 'cliff_front_b'
                    if y==y0+h-face:
                        if l: n='cliff_bl'
                        elif r: n='cliff_br'
                    else:
                        if l: n='cliff_front_a'
                        elif r: n='cliff_front_c'
                    s.put(x,y,n,1)
                elif top:
                    s.put(x,y,'cliff_tl' if l else 'cliff_tr' if r else 'cliff_t',1)
                elif l: s.put(x,y,'cliff_l',1)
                elif r: s.put(x,y,'cliff_r',1)
                else: s.put(x,y,'cliff_c',0)
    def water(s,cells,extra=()):
        cells=set(cells); allw=cells|set(extra)
        for (x,y) in cells:
            n=(x,y-1) in allw; so=(x,y+1) in allw; w=(x-1,y) in allw; e=(x+1,y) in allw
            k='water'
            if (not so and not w and not e) and n: k='shore_swe'
            elif (not n and not w and not e) and so: k='shore_nwe'
            elif (not n and not so and not w) and e: k='shore_nsw'
            elif (not n and not so and not e) and w: k='shore_nse'
            elif not n and not w: k='shore_nw'
            elif not n and not e: k='shore_ne'
            elif not so and not w: k='shore_sw'
            elif not so and not e: k='shore_se'
            elif not n: k='shore_n'
            elif not so: k='shore_s'
            elif not w: k='shore_w'
            elif not e: k='shore_e'
            else:
                if (x-1,y-1) not in allw: k='shore_in_nw'
                elif (x+1,y-1) not in allw: k='shore_in_ne'
                elif (x-1,y+1) not in allw: k='shore_in_sw'
                elif (x+1,y+1) not in allw: k='shore_in_se'
            s.put(x,y,k,0,1)
    def pine(s,x,y,green=False):
        p='pinegreen' if green else 'pine'
        for dy in range(3):
            for dx in range(2): s.put(x+dx,y+dy,f'{p}_{dx}{dy}',1)
    def img(s,scale=1):
        return render(s.g,'general','snow',1)
    def bin(s):
        return [ (s.g[y][x]&0x3ff)|(s.col[y][x]<<10)|(s.elev[y][x]<<12) for y in range(s.H) for x in range(s.W)]

def autopath(m,cells,key='path_stone'):
    cells=set(cells)
    for (x,y) in cells:
        n=(x,y-1) in cells; so=(x,y+1) in cells; w=(x-1,y) in cells; e=(x+1,y) in cells
        k='c'
        if not n and not w: k='tl'
        elif not n and not e: k='tr'
        elif not so and not w: k='bl'
        elif not so and not e: k='br'
        elif not n: k='t'
        elif not so: k='b'
        elif not w: k='l'
        elif not e: k='r'
        else:
            if (x-1,y-1) not in cells: k='in_br'
            elif (x+1,y-1) not in cells: k='in_bl'
            elif (x-1,y+1) not in cells: k='in_tr'
            elif (x+1,y+1) not in cells: k='in_tl'
        m.put(x,y,f'{key}_{k}',0)
def rect(x0,y0,x1,y1): return [(x,y) for x in range(x0,x1+1) for y in range(y0,y1+1)]
import math
def blob(cx,cy,rx,ry,seed=0,rough=0.18):
    import random; r=random.Random(seed); ph=[r.random()*6.28 for _ in range(3)]
    out=[]
    for y in range(int(cy-ry-3),int(cy+ry+4)):
        for x in range(int(cx-rx-3),int(cx+rx+4)):
            a=math.atan2(y-cy,x-cx)
            k=1+rough*(math.sin(3*a+ph[0])+0.6*math.sin(5*a+ph[1])+0.4*math.sin(7*a+ph[2]))/2
            if ((x-cx)/rx)**2+((y-cy)/ry)**2 <= k*k: out.append((x,y))
    return out
def smooth(cells):
    # verwijder 1-tile uitsteeksels (min. 2 buren in elke as)
    s=set(cells)
    changed=True
    while changed:
        changed=False
        for (x,y) in list(s):
            if not(((x-1,y) in s or (x+1,y) in s) and ((x,y-1) in s or (x,y+1) in s)) or \
               (((x-1,y) not in s and (x+1,y) not in s)) or (((x,y-1) not in s and (x,y+1) not in s)):
                s.discard((x,y)); changed=True
    return s

def terrace(m,R,face=2,skip=set()):
    R=set(R)
    def depth(x,y):
        for k in range(1,face+1):
            if (x,y+k) not in R: return k
        return 0
    isface=lambda x,y: (x,y) in R and depth(x,y)>0
    for (x,y) in R:
        if not(0<=x<m.W and 0<=y<m.H) or (x,y) in skip: continue
        d=depth(x,y)
        if d:
            l=not isface(x-1,y); r=not isface(x+1,y)
            if d==face or (d==1 and face==1):
                n='cliff_bl' if l else 'cliff_br' if r else 'cliff_b'
            elif d==1 or face<=2:
                n='cliff_front_a' if l else 'cliff_front_c' if r else 'cliff_front_b'
            else:
                n='cliff_l' if l else 'cliff_r' if r else 169
            c=1
        else:
            t=(x,y-1) not in R; l=(x-1,y) not in R; r=(x+1,y) not in R
            if t: n='cliff_tl' if l else 'cliff_tr' if r else 'cliff_t'
            elif l: n='cliff_l'
            elif r: n='cliff_r'
            else: n='cliff_c'
            c=0 if n=='cliff_c' else 1
        m.put(x,y,n,c)
def fall(m,x0,y0,y1,w=3,foam=True):
    for y in range(y0,y1+1):
        for x in range(x0,x0+w):
            if y==y0: t=187 if x==x0 else 188 if x==x0+w-1 else 179
            else: t=185
            m.put(x,y,t,0,1)
    if foam:
        for x in range(x0,x0+w): m.put(x,y1+1,193,0,1)

def hforest(m,region,ok,path=set()):
    """Hoenn-bosbomen (besneeuwd) op een 2x2-raster (even x/y, gelijk aan de border.bin).
    Buiten de kaart geldt als bos, zodat de rand naadloos doorloopt. Een boom komt er alleen
    als zijn top past: bovenaan de kaart, onder een andere boom, of met een vrije cel erboven."""
    region=set(region)
    out=lambda x,y: not(0<=x<m.W and 0<=y<m.H)
    cand={(x,y) for (x,y) in region if x%2==0 and y%2==0 and all(out(x+dx,y+dy) or ((x+dx,y+dy) in region and ok(x+dx,y+dy)) for dx in (0,1) for dy in (0,1))}
    TOPS={N['htree_1d4'],N['htree_1d6']}
    old=lambda x,y: 0<=x<m.W and 0<=y<m.H and m.g[y][x] in TOPS     # boom die er al staat (linkerbovenkwart)
    anchors=set()
    for (x,y) in sorted(cand,key=lambda p:p[1]):
        if y==0 or (x,y-2) in anchors or old(x,y-2) or all(ok(x+dx,y-1) and (x+dx,y-1) not in path for dx in (0,1)):
            anchors.add((x,y))
    A=lambda x,y: (x,y) in anchors or out(x,y) or old(x,y)
    T=lambda k: 'htree_'+k
    for (x,y) in anchors:
        L=A(x-2,y); R=A(x+2,y); B=A(x,y+2)
        m.put(x,y,T('1d4' if L else '1d6'),1); m.put(x+1,y,T('1d5' if R else '1d7'),1)
        if B: m.put(x,y+1,T('1dc'),1); m.put(x+1,y+1,T('1dd'),1)
        else: m.put(x,y+1,T('1e4' if L else '1e6'),1); m.put(x+1,y+1,T('1e5' if R else '1e7'),1)
    for (x,y) in anchors:
        if y>0 and old(x,y-2):
            m.put(x,y-1,T('1dc'),1); m.put(x+1,y-1,T('1dd'),1)   # bestaande boom erboven: stam met onze top erover
        elif y>0 and (x,y-2) not in anchors:
            m.put(x,y-1,T('1ce'),0); m.put(x+1,y-1,T('1cf'),0)
    # buren die er al stonden: hun zijkant laten aansluiten
    for (x,y) in anchors:
        for (nx,side) in ((x-2,'r'),(x+2,'l')):
            if old(nx,y) and (nx,y) not in anchors:
                if side=='r': m.put(nx+1,y,T('1d5'),1); m.put(nx+1,y+1,T('1dd' if m.g[y+1][nx]==N['htree_1dc'] else '1e5'),1)
                else: m.put(nx,y,T('1d4'),1); m.put(nx,y+1,T('1dc' if m.g[y+1][nx+1]==N['htree_1dd'] else '1e4'),1)
    return anchors
