# Regicosmo r1: kale reductie (kaal.py) -> technisch opschonen. Elke stap telt de pixels die hij verandert.
# Bouwen: cd docs/concept/sprites/regicosmo && python3 sprite/r1/natief.py && python3 sprite/r1/kaal.py && python3 sprite/r1/bouw.py && python3 sprite/r1/vel.py
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from scipy import ndimage; import pal, gemeen as g, kaal as kl
D=g.D
kaal=np.load(os.path.join(D,'kaal.npy')); DL0=np.load(os.path.join(D,'kaal_deel.npy'))
s=kaal.copy(); DL=DL0.copy(); log=[]
def stap(naam,nieuw):
    global s
    d=(nieuw!=s); log.append((naam,int(d.sum()),d)); s=nieuw
a,deel,dot=g.natief(); C=kl.C
def subs(x,y,N=8):
    sub=(np.arange(N)+0.5)/N
    xs=np.clip((kl.X0+(x-kl.OX+sub)/kl.s).astype(int),0,deel.shape[1]-1); ys=np.clip((kl.Y0+(y-kl.OY+sub)/kl.s).astype(int),0,deel.shape[0]-1)
    return deel[ys[:,None],xs[None,:]].ravel(), C[ys[:,None],xs[None,:]].ravel()
# ---- 1. Saturnus (15x10 px): de kale reductie brak de dunne ring (gaten, ring en planeet door elkaar). Per spritepixel
#         overgenomen van het model (dominante modelkleur per spritepixel, raster.py 46 24 64 36): ring = grijs midden (g) met donkere
#         rand (b = bruin donker aan de lichtkant/binnen, K = zwart aan de schaduwkant), gaten van de ringlussen 1 px
#         (59,27) zoals het model (links meet het model geen gat: lus dicht); planeetbanden perzik/oranje diagonaal, rood onder de ring, buitenlijn
#         donkerrood (r) aan de lichtkant. Zie NOTITIES.md.
SAT=[".............bb.",     # x47..62, y25..34 (kolom 0 = x47); gemeten met de modeldominantie per spritepixel
     "......rrrrrbbggK",
     ".....rPooPob.bgK",
     "....rooPPoorbgK.",
     "....rPPooPobgK..",
     "...roooPPbgKK...",
     "..bbPPPPggRrK...",
     ".bggbbggbRRK....",
     ".KggbgbRRrrK....",
     "..KKKKKKKK......"]
CH={'.':0,'K':1,'r':2,'R':3,'o':4,'P':5,'b':6,'g':13}
n=s.copy(); n[DL==2]=0; DL[DL==2]=-1
for j,row in enumerate(SAT):
    for i,c in enumerate(row):
        if c!='.': n[25+j,47+i]=CH[c]; DL[25+j,47+i]=2
stap('Saturnus ring',n)
# ---- 2. stippen: kale stippixels -> omringende Mars-toon; dan 7 blokjes 2x2 op de modelplek (centra natief gemeten):
#         3 px cyaan + 1 lichter linksboven, alle 7 gelijk (Regice/Regirock/Registeel).
MARS=[2,3,4,5,6,7]
n=s.copy()
for y,x in zip(*np.where((s==8)&(DL==0))):   # alleen Mars (cyaan is ook de ijsplaneet)
    b=[s[yy,xx] for yy in range(y-2,y+3) for xx in range(x-2,x+3) if s[yy,xx] in MARS]
    n[y,x]=max(set(b),key=b.count)
lab,k=ndimage.label(dot); cen=ndimage.center_of_mass(dot,lab,range(1,k+1)); sz=ndimage.sum(dot,lab,range(1,k+1))
# twee stukjes van dezelfde stip (66,100)+(68.4,100.1) samenvoegen
pts=[]
for (cy,cx),w in zip(cen,sz):
    for p in pts:
        if abs(p[0]-cy)<3 and abs(p[1]-cx)<3: p[0]=(p[0]*p[2]+cy*w)/(p[2]+w); p[1]=(p[1]*p[2]+cx*w)/(p[2]+w); p[2]+=w; break
    else: pts.append([cy,cx,w])
BLOK=[]
# stippen die in het model op dezelfde rij staan (verschil < 1 natieve px) krijgen dezelfde spriterij (gemiddelde)
for p in pts: p.append(np.mean([q[0] for q in pts if abs(q[0]-p[0])<1]))
for cy,cx,w,cym in pts:
    sx,sy=kl.naar_sprite(cx,cym)    # spritecentrum (continu); blok 2x2 met linksboven op floor(c-0.5), half omhoog afgerond
    BLOK.append((int(np.floor(sx-0.5)),int(np.floor(sy-0.5))))
for x,y in BLOK:
    n[y:y+2,x:x+2]=8; n[y,x]=9
stap('stippen',n)
# ---- 3. buitenlijn 1 px per hemellichaam: schaduwkant (normaal naar rechts/onder) zwart, lichtkant selout (donkerste eigen tint).
fig=s>0
def rand(m):
    p=np.pad(m,1); return m&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
n=s.copy(); SCH=np.zeros_like(fig); BND=np.zeros_like(fig)
for k in range(7):
    if k==2: continue      # Saturnus is per pixel gezet (stap 1), incl. buitenlijn
    m=(DL==k)&fig
    if not m.any(): continue
    b=rand(m)
    gy,gx=np.gradient(ndimage.gaussian_filter(m.astype(float),1.5 if k==0 else 1.0))
    nx,ny=-gx,-gy; nn=np.hypot(nx,ny)+1e-9; nx/=nn; ny/=nn
    sch=(0.6*nx+0.8*ny)>0.05
    SCH|=b&sch; BND|=b
    sel=g.SELOUT[g.NAMEN[k]]
    if k==2:   # Saturnus: ring heeft zijn eigen selout (donker), planeet donkerrood
        for y,x in zip(*np.where(b&~sch)): n[y,x]=6 if s[y,x] in (6,13,1) else 2
    else: n[b&~sch]=sel
    n[b&sch]=1
stap('buitenlijn',n)
# ---- 4. zwart binnen een hemellichaam (geen buitenrand) -> binnenlijn in de selout van dat deel (Gen 3: binnenlijnen niet zwart).
n=s.copy()
for k in range(7):
    if k==2: continue
    m=(DL==k)&(s==1)&~BND
    n[m]=g.SELOUT[g.NAMEN[k]]
stap('zwart binnen -> binnenlijn',n)
def compact(idx,P):
    used=[0]+[i for i in range(1,len(P)) if (idx==i).any()]
    m=np.zeros(256,'uint8'); m[used]=np.arange(len(used)); return m[idx],[P[i] for i in used]
if __name__=='__main__':
    uit,P2=compact(s,g.PAL)
    pal.opslaan(uit,os.path.join(D,'regicosmo_r1.png'),P2)
    np.save(os.path.join(D,'r1.npy'),s); np.save(os.path.join(D,'r1_deel.npy'),DL)
    for nm,d,_ in log: print(nm,d)
    print('kleuren (incl. transparant)',len(P2),'stipblokken',BLOK)
    lab,nn=ndimage.label(s>0,np.ones((3,3))); print('losse delen (8-samenhang)',nn)
    tot=(s!=kaal)
    for k in range(7):
        m=(DL==k)|(DL0==k); print('zone %-10s afwijkend %3d px |'%(g.NAMEN[k],(tot&m).sum()),', '.join('%s %d'%(nm,(mk&m).sum()) for nm,_,mk in log if (mk&m).sum()))
    print('totaal afwijkend',tot.sum(),'van',(s>0).sum())
