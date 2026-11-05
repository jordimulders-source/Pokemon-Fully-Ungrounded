"""Salticonda kleurronde 1: A (silhouet1) en E (silhouet2) inkleuren.
Palet = Silicobra-Uyuni (af). Tekens = die van het pre-evo-raster:
. 0 transparant | O 1 warm bijna-zwart | K 2 omlijningsbasis | h 3 omlijning lichtkant
e 4 donkere schaduw | d 5 schaduw | c 6 midden | b 7 basis | a 8 hooglicht
f 9 gezicht | g 10 gezichtsschaduw | q 11 pekel licht | r 12 pekel | s 13 pekel donker | t 14 pekel diepst
Kop = handgetekend raster (KOP), gelijk voor A en E. Lijf: zones (windingen, pekelringen,
naden, staart) met de hand vastgelegd per variant; de toon per pixel volgt licht van linksboven.
Daarna handmatige pixelcorrecties (FIX per variant)."""
import math, sys
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/'
D=R+'docs/concept/sprites/salticonda/'
sys.path.insert(0,D+'scripts')
CH='.OKhedcbafgqrst'
PAL=Image.open(D+'../silicobra_uyuni/af/silicobra_uyuni.png').getpalette()[:48]

KOP = [
"..............hhhhhh.......",
"...........hhaabbbbccK.....",
".........heeeeebbbdbccK....",
"........heaaaaaebhbccdcK...",
".......hrOOddddOOshbcdccK..",
"..hhh.harttOOOOttshccdcdcK.",
".haOaaaarrastOtssfheedcddeK",
"haaaaaaaarqqrOrssfeeeeddceK",
"haaaaaaaafrrrrssffggeeeddeK",
"KeddaafffffffffffggggeedeK.",
"KfgeegfffffffffgggggddeeK..",
".KffffffffffgggggggdddeeK..",
"..KgffffffgggggggdddeeeK...",
"....KKggggggggdddddeeeeK...",
".......KKKgggddddeeeeeeeK..",
]

def load(f):
    P=Image.open(f).load(); return {(x,y) for x in range(64) for y in range(64) if P[x,y]!=0}

def colour(spec):
    S=load(spec['src'])
    hx,hy=spec['head']
    C={}
    # kop
    H={}
    for j,row in enumerate(KOP):
        for i,c in enumerate(row):
            if c!='.': H[(hx+i,hy+j)]=c
    assert set(H)<=S, 'kop past niet in het silhouet'
    tail=set(spec['tail'])&S
    body=S-set(H)-tail
    rows={}
    for (x,y) in body: rows.setdefault(y,[]).append(x)
    ext={y:(min(v),max(v)) for y,v in rows.items()}
    bounds=spec['bounds']          # per gleuf: (xL,yL,xR,yR,sag)
    def by(k,x):
        xL,yL,xR,yR,sag=bounds[k]; u=min(1,max(0,(x-xL)/(xR-xL)))
        return yL+(yR-yL)*u+sag*math.sin(math.pi*u)
    yt,yb=spec['yt'],spec['yb']
    sext={y:(min(ext[yy][0] for yy in range(y-2,y+3) if yy in ext),max(ext[yy][1] for yy in range(y-2,y+3) if yy in ext)) for y in ext}
    for (x,y) in body:
        xl,xr=sext[y]; u=min(1,max(0,(x-xl)/max(1,xr-xl)))
        # in welke winding: boven gleuf k?
        k=0
        while k<len(bounds) and y>math.floor(by(k,x))+1: k+=1
        top=math.floor(by(k-1,x))+1 if k>0 else yt
        bot=math.floor(by(k,x))-1 if k<len(bounds) else yb+1
        v=(y-top)/max(1,bot-top)
        # ring: drie rijen rond de gleuflijn (licht boven, donker onder)
        hit=None
        for kk in range(len(bounds)):
            y0=math.floor(by(kk,x))
            lo=-1 if spec.get('ring3',True) else 0
            if kk==0 or True:
                if y0+lo<=y<=y0+1 and (kk>0 or (spec['neck'][0]<=x<=spec['neck'][1])): hit=y-y0 if lo==-1 else (y-y0)*2-1
        if hit is not None:
            if hit is not None and spec['neck'][0]<=x<=spec['neck'][1] and y<spec['neck_y']:
                nx0,nx1=spec['neck']; uu=(x-nx0)/(nx1-nx0)
                if (uu<0.1 or uu>0.9) and hit!=0: hit=None   # halsband loopt taps uit
        if hit is not None:
            if hit==-1: C[(x,y)]= 'q' if u<0.16 else ('r' if u<0.62 else 's')
            elif hit==0: C[(x,y)]= 's' if u<0.7 else 't'
            else: C[(x,y)]= 't'
            continue
        # buis: bovenkant licht, onderkant (onder de bolling, boven de ring) schaduw
        tube= -0.4 if v<0.28 else (0.0 if v<0.58 else (0.3 if v<0.8 else 0.5))
        if k<len(bounds) and bot-y<1: tube=0.75          # slagschaduw van de winding op de ring
        sc=0.9*u+0.5*tube+0.12
        if y>yb-3: sc+=0.25*(y-(yb-3))/3
        lv='a' if sc<0.2 else 'b' if sc<0.42 else 'c' if sc<0.6 else 'd' if sc<0.8 else 'e'
        C[(x,y)]=lv
    # ruis weg: een toonpixel die op geen enkele buur lijkt krijgt de meerderheidskleur
    for _ in range(2):
        for (x,y) in list(C):
            c=C[(x,y)]
            if c in 'qrst': continue
            n=[C.get(q) for q in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)] if q in C and C.get(q) not in 'qrst']
            if len(n)>=3 and c not in n:
                best=max(set(n),key=n.count)
                if n.count(best)>=2: C[(x,y)]=best
    # naden (Y-punten) – handmatig per variant: lijst van pixels
    for (x,y) in spec.get('seams',[]):
        if (x,y) in body and C[(x,y)] not in 'qrst':
            C[(x,y)]={'a':'c','b':'c','c':'d','d':'e','e':'e'}[C[(x,y)]]
    # na de naden: eilandjes naast een naad opruimen (naden zelf blijven)
    seamset=set(spec.get('seams',[]))
    for (x,y) in list(body):
        c=C[(x,y)]
        if (x,y) in seamset or c in 'qrst': continue
        n=[C.get(q) for q in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)] if q in body and q not in seamset and C.get(q) not in 'qrst']
        if n and c not in n: C[(x,y)]=max(set(n),key=n.count)
    # staart: banden langs de spits, punt turquoise
    tx,ty=spec['tip']
    for (x,y) in tail:
        s=math.hypot(x-tx,y-ty)
        if s<2.2: C[(x,y)]='r' if (x+y)%2 else 's'
        elif s<3.2: C[(x,y)]='s'
        else:
            band=int((s-3.2)/2.2)%2
            C[(x,y)]='e' if band==0 else 'c'
    # kop erover
    C.update(H)
    # omlijning
    def tr(p): return p not in S
    for (x,y) in S:
        n=[(x,y-1),(x-1,y),(x+1,y),(x,y+1)]
        if not any(tr(q) for q in n):
            if (x,y) in H and H[(x,y)] in 'hKO' and x>=hx+19 and not (((x,y+1) in S and (x,y+1) not in H)):
                C[(x,y)]='e'   # rechterrand van de kop loopt in het lijf over: geen lijn
            continue
        if (x,y) in H:
            if H[(x,y)] not in 'hKO':
                C[(x,y)]='h' if (n[0] not in S or n[1] not in S) and x<hx+18 else 'K'
            continue
        c=C[(x,y)]
        up,lf,rt,dn=[tr(q) for q in n]
        xl,xr=ext.get(y,(x,x)); u=(x-xl)/max(1,xr-xl)
        if c in 'qrst':
            C[(x,y)]='s' if u<0.5 else 't'; continue
        if (x,y) in tail:
            C[(x,y)]='O' if dn or (rt and not up) else 'K'; continue
        lower_right = (dn and x>spec['dark_x']) or (rt and y>spec['dark_y'])
        if lower_right: C[(x,y)]='O'
        elif (up or lf) and u<0.55 and not dn: C[(x,y)]='h'
        else: C[(x,y)]='K'
    # kin en staart: contour waar ze over het lijf liggen
    for p in spec.get('contour',[]):
        if p in S: C[p]='K'
    for p in spec.get('lone',[]):          # losse pixel -> kleur van de buren
        n=[C.get(q) for q in [(p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1)] if q in C]
        C[p]=max(set(n),key=n.count)
    for p,c in spec.get('fix',{}).items(): C[p]=c
    return S,C

def save(S,C,name):
    im=Image.new('P',(64,64),0); im.putpalette(PAL+[0]*(768-48))
    for p,c in C.items(): im.putpixel(p,CH.index(c))
    im.save(D+'kleur1/'+name+'.png',transparency=0)
    ras='\n'.join(''.join(C.get((x,y),'.') for x in range(64)) for y in range(64))
    open(D+'kleur1/'+name+'_raster.txt','w').write(ras+'\n')

def seam(pts):
    """polylijn -> pixels, trapsgewijs (1 px stappen)"""
    out=[]
    for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
        n=max(abs(x1-x0),abs(y1-y0))
        for i in range(n+1):
            out.append((round(x0+(x1-x0)*i/n),round(y0+(y1-y0)*i/n)))
    return out

def ys(lst):
    out=[]
    for c,ends in lst:
        for e in ends: out+=seam([c,e])
    return out

A_TAIL=[(x,y) for y,a,b in [(50,61,62),(51,58,62),(52,56,61),(53,55,60),(54,54,59),(55,54,57),(56,53,55)] for x in range(a,b+1)]
E_TAIL=[(x,y) for y,a,b in [(47,61,62),(48,60,62),(49,59,62),(50,58,61),(51,58,60),(52,57,60),(53,56,59),(54,55,58),(55,54,57),(56,52,55),(57,50,51)] for x in range(a,b+1)]
V={
 'A': dict(src=D+'silhouet1/variant_A.png', head=(9,11), tail=A_TAIL, tip=(62,50),
           yt=26, yb=58, lone=[(31,29),(17,44)], dark_x=34, dark_y=40, ring3=False, neck=(17,37), neck_y=29,
           bounds=[(17,27.0,37,26.5,1.5),(19,33.5,48,33.5,3.0),(12,41.5,54,41.5,3.5),(9,49.5,57,49.5,4.0)],
           seams=ys([((30,30),[(27,28),(34,28),(31,32)]),((24,37),[(21,35),(28,35),(23,40)]),((41,38),[(38,35),(45,36),(42,40)]),
                     ((17,45),[(14,43),(21,43),(18,48)]),((34,46),[(31,43),(38,44),(33,48)]),
                     ((25,54),[(21,52),(29,51),(25,57)]),((44,53),[(41,51),(48,51),(45,57)])])),
 'E': dict(src=D+'silhouet2/variant_E.png', head=(9,6), tail=E_TAIL, tip=(62,47),
           yt=19, yb=60, lone=[(21,59),(44,23)], dark_x=32, dark_y=36, neck=(14,35), neck_y=24,
           bounds=[(14,21.2,35,20.4,2.0),(9,32.5,51,28.5,3.5),(4,46.5,56,42.5,4.0)],
           seams=ys([((36,25),[(33,23),(41,23),(37,29)]),((21,38),[(17,35),(26,35),(22,43)]),((41,39),[(38,35),(46,36),(43,44)]),
                     ((15,52),[(11,49),(20,49),(16,57)]),((35,53),[(32,49),(40,49),(34,58)])])),
}
if __name__=='__main__':
    for k in sys.argv[1:] or V:
        S,C=colour(V[k]); save(S,C,'salticonda_'+k)
        print(k,len(S),'px')
