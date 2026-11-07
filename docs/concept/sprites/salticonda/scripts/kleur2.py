"""Salticonda kleurronde 2: 3/4-lijf + handgetekende kop/hals en staart.
- Lijf: onderlaag2.py (drie windingen als tori, iets van boven, licht linksboven) -> tonen, pekelringen
  in de gleuven, Y-naden, omlijning.
- Kop/hals/halsband: handgetekend raster kleur2/bron/kop_A.txt (koepel) en kop_B.txt (kroon van platen).
- Staart: handgetekend raster kleur2/bron/staart.txt (ligt achter de onderste winding).
Tekens = palet van de Silicobra-Uyuni (zie kleur1.py).
Gebruik: python3 kleur2.py  -> schrijft kleur2/salticonda_A/B.png + _raster.txt"""
import math, sys
from PIL import Image
sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/scripts')
import onderlaag2
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
CH='.OKhedcbafgqrst'
PAL=Image.open(D+'../silicobra_uyuni/af/silicobra_uyuni.png').getpalette()[:48]

def body():
    px=onderlaag2.render()
    C={}; coil={}
    for (x,y),(dep,ci,l,b) in px.items():
        coil[(x,y)]=ci
        C[(x,y)]='a' if l>0.95 else 'b' if l>0.76 else 'c' if l>0.50 else 'd' if l>0.22 else 'e'
    # gleuven: pekelringen op de lagere winding, direct onder de hogere
    for (x,y),ci in list(coil.items()):
        if ci==0 and False: pass
    for (x,y),ci in coil.items():
        up=[coil.get((x,y-k)) for k in (1,2,3)]
        for k,u in enumerate(up):
            if u is not None and u>ci:
                C[(x,y)]={0:'r',1:'s',2:'t'}[k]
                break
    for (x,y),ci in coil.items():   # slagschaduw: onderste rij van de hogere winding
        if C[(x,y)] in 'abc' and coil.get((x,y+1)) is not None and coil[(x,y+1)]<ci: C[(x,y)]='d'
    return C,coil

def outline(C,S,H=set()):
    """randpixels van het lijf: h lichtkant (links/boven), K midden, O rechtsonder; pekel s/t"""
    out={}
    ys=[p[1] for p in S]
    for (x,y) in S:
        if (x,y) in H: continue
        n=[(x,y-1),(x-1,y),(x+1,y),(x,y+1)]
        up,lf,rt,dn=[q not in S for q in n]
        if not (up or lf or rt or dn): continue
        c=C[(x,y)]
        if c in 'qrst': out[(x,y)]='s' if x<32 else 't'; continue
        if (dn and x>26) or (rt and y>30) or (dn and y>56): out[(x,y)]='O'
        elif (up or lf) and x<30: out[(x,y)]='h'
        else: out[(x,y)]='K'
    C.update(out)

def render(C):
    im=Image.new('P',(64,64),0); im.putpalette(PAL+[0]*(768-48))
    for p,c in C.items():
        if c!='.': im.putpixel(p,CH.index(c))
    return im
def overlay(C,txt,ox,oy,under=False):
    for j,row in enumerate(open(txt).read().split('\n')):
        for i,c in enumerate(row):
            if c!='.' and (not under or (ox+i,oy+j) not in C): C[(ox+i,oy+j)]=c

def seam(pts):
    out=[]
    for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
        n=max(abs(x1-x0),abs(y1-y0))
        for i in range(n+1): out.append((round(x0+(x1-x0)*i/n),round(y0+(y1-y0)*i/n)))
    return out
SEAMS=[((20,54),[(16,52),(24,51),(21,57)]),((40,55),[(36,52),(44,52),(41,58)]),
       ((18,42),[(14,41),(22,40),(19,44)]),((36,42),[(33,40),(40,40),(37,45)])]
def seams(C):
    for c,ends in SEAMS:
        for e in ends:
            for p in seam([c,e]):
                if C.get(p) in tuple('abcd'): C[p]={'a':'c','b':'c','c':'d','d':'e'}[C[p]]

def build(kop, staart):
    C,coil=body()
    for (x,y) in list(C):
        if C[(x,y)]=='e' and x<26 and y<56: C[(x,y)]='d'
    for (x,y) in list(C):   # ruis: toonpixel zonder gelijke buur (8 buren) -> meerderheid
        c=C[(x,y)]
        if c not in 'abcde': continue
        n=[C.get((x+dx,y+dy)) for dx in (-1,0,1) for dy in (-1,0,1) if (dx or dy) and C.get((x+dx,y+dy),'.') in 'abcde' and (x+dx,y+dy) in C]
        if n and c not in n: C[(x,y)]=max(set(n),key=n.count)
    seams(C)
    outline(C,set(C))
    overlay(C,staart,43,36,under=True)
    overlay(C,kop,0,0)
    # afwerking: gaatjes dicht, randpixels zonder lijnkleur -> lijnkleur
    for _ in range(3):
        S=set(C)
        for x in range(1,63):
            for y in range(1,63):
                if (x,y) not in S and sum((x+dx,y+dy) in S for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))>=3: C[(x,y)]='K'
    S=set(C)
    for (x,y) in list(C):
        if C[(x,y)] not in 'OKhst' and any(q not in S for q in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]):
            C[(x,y)]='O' if y>28 and x>30 else 'K'
    return C

def save(C,name):
    im=render(C); im.save(D+'kleur2/'+name+'.png',transparency=0)
    open(D+'kleur2/'+name+'_raster.txt','w').write('\n'.join(''.join(C.get((x,y),'.') for x in range(64)) for y in range(64))+'\n')

if __name__=='__main__' and len(sys.argv)==1:
    for v in 'AB':
        C=build(D+'kleur2/bron/kop_%s.txt'%v,D+'kleur2/bron/staart.txt'); save(C,'salticonda_'+v); print(v,len(C),'px')
elif __name__=='__main__':
    C=build(sys.argv[1],sys.argv[2])
    bg=Image.new('RGBA',(64,64),(150,200,160,255)); im=render(C).convert('RGBA')
    m=Image.new('L',(64,64),0)
    for p in C: m.putpixel(p,255)
    bg.paste(im,(0,0),m)
    out=Image.new('RGBA',(600,512),(150,200,160,255)); out.paste(bg.resize((512,512),Image.NEAREST),(0,0)); out.paste(bg,(525,10))
    out.save(sys.argv[3]); print(len(C))
