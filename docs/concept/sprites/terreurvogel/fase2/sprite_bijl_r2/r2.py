# Ronde 2 (afwerking) vanaf ../swaps_r1/v8.png. Bouwt vanaf de png; elke stap logt zijn pixels.
import numpy as np; from PIL import Image
import lib1 as l
V8=Image.open('../swaps_r1/v8.png'); S0=np.array(V8).astype(int); S=S0.copy()
PAL=[tuple(V8.getpalette()[i*3:i*3+3]) for i in range(16)]
FIGM=S0>0
GROEP={1:1,2:0,3:2,4:2,5:2,6:3,7:3,8:3,9:4,10:4,11:4,12:4,13:5,14:5,15:5}
DONKER={2:3,3:6,4:9,5:13}
LOG=[]
def g(i): return GROEP.get(int(i),0)
def zet(y,x,v,stap):
    if S[y,x]!=v: LOG.append((stap,y,x,int(S[y,x]),int(v))); S[y,x]=v
def leeg(y,x): return not(0<=y<64 and 0<=x<64) or not FIGM[y,x]
def rand(y,x): return FIGM[y,x] and any(leeg(y+a,x+b) for a,b in((-1,0),(1,0),(0,-1),(0,1)))
def zone(y,x):
    if x<=13 or (x<=15 and y>=31): return 'snavel'
    if x<=26 and y<=36: return 'kop'
    if y>=48 or (y>=44 and x<=20): return 'poten'
    return 'lijf'
OOG={(29,16),(29,17),(29,18),(30,15),(30,16),(30,17),(30,18),(31,15),(31,16),(31,17),(31,18),(32,15),(32,16)}

# 1. tinten: antraciet lijf en stenen snavel lichter/donkerder gezet voor stappen van ±30-40 (zwart 16 -> lijn/vlak)
PAL[6]=(52,52,58); PAL[7]=(86,84,90); PAL[8]=(124,118,116)     # v8: (40,40,44)(70,68,72)(108,102,100), zelfde tint
PAL[3]=(62,57,52)                                               # v8: (76,70,64); snavel donker iets dieper t.o.v. midden (104,97,89)

# 2. binnenlijnen: zwart binnen de figuur -> donkerste eigen tint (DC: binnenlijnen niet zwart);
#    uitzonderingen: mondlijn van de snavel (opening in het model) en het oog
def groep_buren(y,x):
    c={}
    for a in(-1,0,1):
        for b in(-1,0,1):
            yy,xx=y+a,x+b
            if 0<=yy<64 and 0<=xx<64 and S[yy,xx]>1 and (yy,xx) not in OOG:
                c[g(S[yy,xx])]=c.get(g(S[yy,xx]),0)+1
    return max(c,key=c.get) if c else None
def binnenlijnen():
    for y in range(64):
        for x in range(64):
            if S0[y,x]!=1 or rand(y,x) or (y,x) in OOG: continue
            gg=groep_buren(y,x)
            if gg==2 or gg is None: continue
            d=DONKER[gg]
            buren=[S0[y+a,x+b] for a,b in((-1,0),(1,0),(0,-1),(0,1)) if S0[y+a,x+b]>1]
            # DC "very deepest shadows": een lijn die helemaal in de donkerste vlaktint ligt blijft zwart (anders verdwijnt de vorm)
            if buren and sum(v==d for v in buren)>=max(2,len(buren)-0): continue
            zet(y,x,d,'binnenlijn')

# 3. schublijnen in de poten: banden op gemeten donkere modelplekken (projectie van donkere natieve pootpixels op de pootas)
BANDEN={'links':(np.array([37.9,66.2]),np.array([0.94,-0.33]),[-9.5,-4.0,1.0],(lambda nx,ny: nx<=50 and 59<=ny<=71)),
        'rechts':(np.array([81.8,69.1]),np.array([0.67,0.74]),[-10.0,-5.5,-1.5],(lambda nx,ny: nx>=70 and 59<=ny<=77))}
def schubben():
    # oude losse schubpixels (r1, drempel 0.5) terug naar de pootmiddentint; banden vervangen ze
    for y in range(64):
        for x in range(64):
            if S0[y,x]==13 and not rand(y,x) and zone(y,x)=='poten':
                zet(y,x,14,'schubben')
    for naam,(c,ax,ts,sel) in BANDEN.items():
        for y in range(64):
            for x in range(64):
                if S[y,x] not in (13,14) or rand(y,x): continue
                nx=l.X0+(x+0.5-l.OX)/l.S; ny=l.Y0+(y+0.5-l.OY)/l.S
                if not sel(nx,ny): continue
                t=(np.array([nx,ny])-c)@ax
                if min(abs(t-q) for q in ts)<0.9: zet(y,x,13,'schubben')

# 4. buitenlijn (DC): outline base = donkerste eigen tint aan de lichtkant, zwart alleen als outline shadow rechts/onder.
#    Kant = gladde buitennormaal (5x5) . lichtrichting linksboven; daarna geen zwart/donker om en om op een rand.
def buitenlijn():
    T=~FIGM
    R=[(y,x) for y in range(64) for x in range(64) if rand(y,x) and (y,x) not in OOG]
    kant={}
    for y,x in R:
        nx=ny=0.0
        for a in range(-2,3):
            for b in range(-2,3):
                yy,xx=y+a,x+b
                e=True if not(0<=yy<64 and 0<=xx<64) else T[yy,xx]
                if e: nx+=b; ny+=a
        d=(-nx-ny)/max(1e-6,np.hypot(nx,ny))     # cos met linksboven (-1,-1)/sqrt2 * sqrt2
        kant[(y,x)]='licht' if d>0.35 else 'schaduw'
    # om-en-om op de rand gladstrijken: randpixel waarvan beide randburen (8-buren op de rand) de andere kant hebben
    for _ in range(2):
        nieuw=dict(kant)
        for (y,x),k in kant.items():
            bb=[kant[(y+a,x+b)] for a in(-1,0,1) for b in(-1,0,1) if (a or b) and (y+a,x+b) in kant]
            if len(bb)>=2 and all(v!=k for v in bb): nieuw[(y,x)]=bb[0]
        kant=nieuw
    for (y,x),k in kant.items():
        gg=groep_buren(y,x)
        if k=='licht' and gg in DONKER: zet(y,x,DONKER[gg],'buitenlijn')
        else: zet(y,x,1,'buitenlijn')
    return kant

def opslaan(pad,A=None):
    A=S if A is None else A
    im=Image.fromarray(A.astype('uint8'),'P'); p=[]
    for c in PAL: p+=list(c)
    im.putpalette(p+[0]*(768-len(p))); im.save(pad,transparency=0)

if __name__=='__main__':
    binnenlijnen(); schubben(); buitenlijn()
    np.save('r2.npy',S); opslaan('terreurvogel_bijl_r2.png')
    from collections import Counter
    print(sorted(Counter((s,zone(y,x)) for s,y,x,a,b in LOG).items()))
    print('afwijkend t.o.v. v8 per zone (pixelindex):',dict(Counter(zone(y,x) for y,x in zip(*np.where(S!=S0)))))
    print('alpha-diff t.o.v. r1/v8:',int(((S>0)!=FIGM).sum()))
