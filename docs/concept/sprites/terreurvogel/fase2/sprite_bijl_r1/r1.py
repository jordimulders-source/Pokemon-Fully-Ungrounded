# Ronde 1: kale reductie -> technisch opschonen. Elke stap telt zijn gewijzigde pixels per zone.
import numpy as np, lib
class ndimage:
    @staticmethod
    def label(m):
        lab=np.zeros(m.shape,int); n=0
        for y0,x0 in zip(*np.where(m)):
            if lab[y0,x0]: continue
            n+=1; st=[(y0,x0)]; lab[y0,x0]=n
            while st:
                y,x=st.pop()
                for dy,dx in((-1,0),(1,0),(0,-1),(0,1)):
                    yy,xx=y+dy,x+dx
                    if 0<=yy<m.shape[0] and 0<=xx<m.shape[1] and m[yy,xx] and not lab[yy,xx]:
                        lab[yy,xx]=n; st.append((yy,xx))
        return lab,n
S0=np.load('kaal.npy'); S=S0.copy()
FIGM=S0>0                                   # silhouet = kale reductie, bevroren
GROEP=lib.GROEP; DONKER={2:3,3:6,4:9,5:13}
LOG=[]
def g(i): return GROEP.get(int(i),0)
def N4(y,x):
    for dy,dx in((-1,0),(1,0),(0,-1),(0,1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<64 and 0<=xx<64: yield yy,xx,S[yy,xx]
        else: yield yy,xx,0
def zet(y,x,v,stap):
    if S[y,x]!=v: LOG.append((stap,y,x,int(S[y,x]),int(v))); S[y,x]=v
# zones (spritecoördinaten) om afwijkingen te tellen
def zone(y,x):
    if x<=13 or (x<=15 and y>=31): return 'snavel'
    if x<=26 and y<=36: return 'kop'
    if y>=48 or (y>=44 and x<=20): return 'poten'
    return 'lijf'

# 1. oog: per pixel naar het model (natief oog 3x3 -> 2x2 binnenin + wenkbrauw), zie rapport
OOG={(29,16):1,(29,17):1,(29,18):1,(30,15):1,(30,16):10,(30,17):2,(30,18):1,(31,15):1,(31,16):10,(31,17):2,(31,18):1,(32,15):1,(32,16):1}
for (y,x),v in OOG.items(): zet(y,x,v,'oog')
OOGSET=set(OOG)

# 2. losse tintvlakjes < 3 px (4-samenhangend, zelfde index) -> meest voorkomende buurtint binnen dezelfde groep
def kleine(stap,minpx=3,groepen=(2,3,4,5)):
    for it in range(3):
        for idx in range(3,16):
            if g(idx) not in groepen: continue
            lab,n=ndimage.label(S==idx)
            for k in range(1,n+1):
                ys,xs=np.where(lab==k)
                if len(ys)>=minpx: continue
                if idx in (3,6,9,13) and len(ys)>=2: continue
                if idx==15: continue
                if any((y,x) in OOGSET for y,x in zip(ys,xs)): continue
                for y,x in zip(ys,xs):
                    if any(leeg(y+dy,x+dx) for dy,dx in((-1,0),(1,0),(0,-1),(0,1))): continue   # buitenlijn niet aanraken
                    c={}
                    for yy,xx,v in N4(y,x):
                        if v>1 and v!=idx and g(v)==g(idx): c[v]=c.get(v,0)+1
                    if c: zet(y,x,max(c,key=c.get),stap)
# vlekken (Jordi: mogen verplaatst/aangepast): roest/oranje-specks < 3 px in het lijf gaan op in de lijftint eromheen
def roestspecks():
    for idx in (10,11,12):
        lab,n=ndimage.label(S==idx)
        for k in range(1,n+1):
            ys,xs=np.where(lab==k)
            if len(ys)>=3: continue
            for y,x in zip(ys,xs):
                if (y,x) in OOGSET: continue
                if any(leeg(y+dy,x+dx) for dy,dx in((-1,0),(1,0),(0,-1),(0,1))): continue
                c={}
                for yy,xx,v in N4(y,x):
                    if v>1 and v!=idx: c[v]=c.get(v,0)+1
                # binnen de roestgroep blijven als er roest omheen ligt, anders de buurtint
                r={v:n for v,n in c.items() if g(v)==4 and v!=idx}
                if r: zet(y,x,max(r,key=r.get),'vlekken')
                elif c: zet(y,x,max(c,key=c.get),'vlekken')

def leeg(y,x): return not(0<=y<64 and 0<=x<64) or not FIGM[y,x]
def binnengroep(y,x):
    """groep van de figuurpixels rond (y,x) (niet zwart), meerderheid."""
    c={}
    for dy in(-1,0,1):
        for dx in(-1,0,1):
            yy,xx=y+dy,x+dx
            if 0<=yy<64 and 0<=xx<64 and S[yy,xx]>1 and (yy,xx) not in OOGSET:
                c[g(S[yy,xx])]=c.get(g(S[yy,xx]),0)+1
    return max(c,key=c.get) if c else None
# 3. buitenlijn: 1 px; lichtkant (leeg boven of links, niet onder/rechts) = gekleurde selout (donkerste groepstint), rest zwart
def buitenlijn():
    rand=[(y,x) for y in range(64) for x in range(64) if FIGM[y,x] and any(leeg(y+dy,x+dx) for dy,dx in((-1,0),(1,0),(0,-1),(0,1)))]
    for y,x in rand:
        if (y,x) in OOGSET: continue
        licht=(leeg(y-1,x) or leeg(y,x-1)) and not(leeg(y+1,x) or leeg(y,x+1))
        if licht:
            gg=binnengroep(y,x)
            binnen=[S[y+dy,x+dx] for dy,dx in((1,0),(0,1)) if not leeg(y+dy,x+dx) and S[y+dy,x+dx]>1]
            if gg in DONKER and binnen and min(lib.L_(v) for v in binnen)-lib.L_(DONKER[gg])>=40:
                zet(y,x,DONKER[gg],'buitenlijn'); continue
            zet(y,x,1,'buitenlijn'); continue
        if not licht: zet(y,x,1,'buitenlijn')
# 4. zwart binnen de figuur: binnenlijn in de donkere eigen tint, behalve op de schaduwkant (buren al donker)
def binnenzwart():
    for y in range(64):
        for x in range(64):
            if S[y,x]!=1 or (y,x) in OOGSET: continue
            if any(leeg(y+dy,x+dx) for dy,dx in((-1,0),(1,0),(0,-1),(0,1))): continue
            buren=[v for _,_,v in N4(y,x)]
            nzw=sum(v==1 for v in buren)
            kleur=[v for v in buren if v>1]
            if not kleur: continue
            gg=max(set(g(v) for v in kleur),key=lambda q:sum(g(v)==q for v in kleur))
            if gg not in DONKER or gg==2: continue   # snavel: mondlijn blijft zwart (opening, model)
            d=DONKER[gg]
            donker=sum(v==d for v in kleur)
            # lijn tussen lichte tinten -> donkere eigen tint; lijn in een donker vlak blijft zwart
            if donker<=len(kleur)/2: zet(y,x,d,'binnenlijn')

# 5. schublijnen in de poten: modelpixels met L<100 (donkerfractie per spritepixel >= 0.5) -> donkerste pootint
def schubben():
    f=np.load('donkerfr.npy')
    for y in range(64):
        for x in range(64):
            if S[y,x] in (14,15) and f[y,x]>=0.5 and not any(leeg(y+dy,x+dx) for dy,dx in((-1,0),(1,0),(0,-1),(0,1))):
                zet(y,x,13,'schubben')
if __name__=='__main__':
    buitenlijn(); binnenzwart(); roestspecks(); kleine('ruis'); schubben()
    # roeststreep in de staart (model: twee 2-px rode streepjes op (49-50,36) en (53-54,35)) als één veerstreep van 6 px
    for y,x in [(36,49),(36,50),(36,51),(35,52),(35,53),(35,54)]: zet(y,x,10,'vlekken')
    zet(25,20,9,'binnenlijn')   # losse zwarte veerlijnpixel in de kuif -> donkere roesttint
    np.save('r1.npy',S); lib.opslaan(S,'r1_tmp.png')
    from collections import Counter
    c=Counter((st,zone(y,x)) for st,y,x,a,b in LOG); print(sorted(c.items()))
    tot=Counter(zone(y,x) for y,x in zip(*np.where(S!=S0))); print('afwijkend t.o.v. kaal per zone',dict(tot))
    print('alpha-diff',int(((S>0)!=FIGM).sum()))
