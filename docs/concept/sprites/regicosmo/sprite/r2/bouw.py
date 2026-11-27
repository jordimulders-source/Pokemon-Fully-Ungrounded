# Regicosmo r2 = r1 + drie benoemde reparaties (Claude, na vergelijking met het model). Buiten de zones pixeldiff 0 (bewezen onderaan).
# Bouwen: cd docs/concept/sprites/regicosmo && python3 sprite/r2/bouw.py && python3 sprite/r2/vel.py
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from scipy import ndimage; import pal, gemeen as g, kaal as kl, saturnus as sa
D=g.D
r1=np.load(os.path.join(D,'r1.npy')); DL1=np.load(os.path.join(D,'r1_deel.npy'))
s=r1.copy(); DL=DL1.copy(); log=[]
def stap(naam,nieuw):
    global s
    d=(nieuw!=s); log.append((naam,int(d.sum()),d)); s=nieuw
a,deel,dot=g.natief(); C=kl.C
def cel(x,y,N=8):
    sub=(np.arange(N)+0.5)/N
    xs=np.clip((kl.X0+(x-kl.OX+sub)/kl.s).astype(int),0,deel.shape[1]-1); ys=np.clip((kl.Y0+(y-kl.OY+sub)/kl.s).astype(int),0,deel.shape[0]-1)
    yy,xx=np.meshgrid(ys,xs,indexing='ij'); return yy.ravel(),xx.ravel()
# ---------- 1. SATURNUS: ronde bol + schuine elliptische ring, gemeten (saturnus.meet) ----------
# bol: cirkelfit op de modelrand; ring: middenlijn van een ellips door de twee uiterste ringpunten (as, kanteling, lengte)
# met de halve korte as = mediane afstand van de grijze ringmiddenlijn voor de bol. Niets verzonnen: alleen deze maten.
(cx,cy,r),(ce,ang,amaj,bmin),_=sa.meet()
scx,scy=sa.naar(cx,cy); sr=r*kl.s
rcx,rcy=sa.naar(*ce)
A=(amaj-1.75)*kl.s     # middenlijn: buitenste ringpunt min de halve ringband (3,5 natieve px)
B=bmin*kl.s
n=s.copy(); n[DL==2]=0; DL[DL==2]=-1
Y,X=np.mgrid[0:64,0:64]
bol=np.hypot(X+0.5-scx,Y+0.5-scy)<=sr
def dun(m):   # hoekpixels weg zolang de lijn 8-samenhangend blijft; eindpunten blijven
    m=m.copy()
    for y,x in zip(*np.where(m)):
        m[y,x]=False
        nb=m[y-1:y+2,x-1:x+2].sum(); lab,k=ndimage.label(m,np.ones((3,3)))
        if k>1 or nb<2: m[y,x]=True
    return m
# ringband = pixels waarvan het middelpunt binnen 0,95 px van de middenlijn ligt (ringband in het model 3,5-4 natieve
# px = 1,7-1,9 spritepx); grijs = de pixel die het dichtst bij de middenlijn ligt (d < 0,5), de rest donkere ringrand.
T=np.linspace(0,2*np.pi,4000,endpoint=False)
PX=rcx+A*np.cos(T)*np.cos(ang)-B*np.sin(T)*np.sin(ang); PY=rcy+A*np.cos(T)*np.sin(ang)+B*np.sin(T)*np.cos(ang)
dmin=np.full((64,64),9.0); voorz=np.zeros((64,64),bool)
for y in range(20,40):
    for x in range(44,64):
        d=np.hypot(PX-(x+0.5),PY-(y+0.5)); i=d.argmin(); dmin[y,x]=d[i]; voorz[y,x]=np.sin(T[i])>0
band=dmin<=0.95
U=(X+0.5-rcx)*np.cos(ang)+(Y+0.5-rcy)*np.sin(ang); W=-(X+0.5-rcx)*np.sin(ang)+(Y+0.5-rcy)*np.cos(ang)
# a) bol: planeetkleur per pixel = meerderheid van de planeetkleuren in de modelcel
for y,x in zip(*np.where(bol)):
    yy,xx=cel(x,y); cc=C[yy,xx]; m=(deel[yy,xx]==2)&np.isin(cc,[2,3,4,5])
    n[y,x]=np.bincount(cc[m],minlength=16).argmax() if m.any() else -5
for y,x in zip(*np.where(n==-5)):
    b=[n[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if n[yy,xx] in (2,3,4,5)]
    n[y,x]=max(set(b),key=b.count) if b else 4
# b) buitenlijn bol: lichtkant donkerrood, schaduwkant zwart (normaal vanuit het middelpunt)
q=np.pad(bol,1); bb=bol&~(q[:-2,1:-1]&q[2:,1:-1]&q[1:-1,:-2]&q[1:-1,2:])
nx=X+0.5-scx; ny=Y+0.5-scy; sch=(0.6*nx+0.8*ny)>0.05*np.hypot(nx,ny)
n[bb&sch]=1; n[bb&~sch]=2
# c) ringband: voorkant over de bol, achterkant alleen buiten de bol
zicht=band&(voorz|~bol)
grijs=zicht&(dmin<0.5)
# grijze middenlijn moet doorlopen: ontbreekt er een stap, dan de bandpixel die het dichtst bij de middenlijn ligt erbij
lab,k=ndimage.label(grijs,np.ones((3,3)))
while k>1:
    best=None
    for y,x in zip(*np.where(zicht&~grijs)):
        nbl=set(lab[max(0,y-1):y+2,max(0,x-1):x+2].ravel())-{0}
        if len(nbl)>=2 and (best is None or dmin[y,x]<best[0]): best=(dmin[y,x],y,x)
    if best is None: break
    grijs[best[1],best[2]]=True; lab,k=ndimage.label(grijs,np.ones((3,3)))
rand=zicht&~grijs
n[grijs]=13
# ringrand: tegen de achtergrond aan de schaduwkant (normaal van de ellips naar rechts/onder) zwart, anders bruin donker
gnx=U*np.cos(ang)/A**2-W*np.sin(ang)/B**2; gny=U*np.sin(ang)/A**2+W*np.cos(ang)/B**2
buiten=(U/A)**2+(W/B)**2>1
for y,x in zip(*np.where(rand)):
    tegen_bg=any(not(bol[yy,xx] or zicht[yy,xx]) for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)))
    sgn=1 if buiten[y,x] else -1
    n[y,x]=1 if (tegen_bg and sgn*(0.6*gnx[y,x]+0.8*gny[y,x])>0) else 6
M2=n>0; M2&=~(s>0)|((DL1==2))   # alleen nieuwe Saturnuspixels
M2=(n!=s)|(DL1==2); M2&=(n>0)
DL[M2]=2
stap('Saturnus bol+ring',n)
SATZ=(DL==2)|(DL1==2)
# ---------- 2. ASTEROIDE: donkere holte (krater linksboven) en inkeping uit het model ----------
# Per binnenpixel de gemiddelde modelhelderheid L van de asteroidepixels in de cel: L < 72 -> bruin donker 6 (holte,
# inkeping, schaduw rechtsonder), 72-112 -> bruin midden 7, >= 112 -> licht 10. In r1 was bijna alles 6, waardoor de
# holte (6) niet tegen de omgeving las; nu is de omgeving van de holte het lichtere 7/10 van het model. Rand blijft r1.
n=s.copy(); AST=(DL==3)
q=np.pad(AST,1); rnd=AST&~(q[:-2,1:-1]&q[2:,1:-1]&q[1:-1,:-2]&q[1:-1,2:])
L=(a*[0.3,0.59,0.11]).sum(2)
for y,x in zip(*np.where(AST&~rnd)):
    yy,xx=cel(x,y); m=deel[yy,xx]==3
    if not m.any(): continue
    lm=L[yy,xx][m].mean(); n[y,x]=6 if lm<72 else (7 if lm<112 else 10)
stap('asteroide holte',n)
# ---------- 3. IJS: bijna-wit hoofdtint, cyaan alleen de schaduwsikkel rechtsonder (modelhelderheid per pixel) ----------
n=s.copy(); IJS=(DL==1)
q=np.pad(IJS,1); rnd=IJS&~(q[:-2,1:-1]&q[2:,1:-1]&q[1:-1,:-2]&q[1:-1,2:])
ijsL=[]
for y,x in zip(*np.where(IJS&~rnd)):
    yy,xx=cel(x,y); m=deel[yy,xx]==1
    ijsL.append(L[yy,xx][m].mean())
GR=np.percentile(ijsL,30)      # donkerste 30 % van het ijs (gemeten) = sikkel; model: blauwer rechtsonder
for (y,x),l in zip(zip(*np.where(IJS&~rnd)),ijsL):
    n[y,x]=8 if l<GR else 9
stap('ijs bijna-wit/cyaan',n)
def compact(idx,P):
    used=[0]+[i for i in range(1,len(P)) if (idx==i).any()]
    m=np.zeros(256,'uint8'); m[used]=np.arange(len(used)); return m[idx],[P[i] for i in used]
if __name__=='__main__':
    uit,P2=compact(s,g.PAL)
    pal.opslaan(uit,os.path.join(D,'regicosmo_r2.png'),P2)
    np.save(os.path.join(D,'r2.npy'),s); np.save(os.path.join(D,'r2_deel.npy'),DL)
    for nm,d,_ in log: print(nm,d)
    print('kleuren (incl. transparant)',len(P2),'| ijsgrens L<%.0f'%GR)
    print('Saturnus: bol sprite c=(%.2f,%.2f) r=%.2f; ring c=(%.2f,%.2f) a=%.2f b=%.2f hoek %.1f'%(scx,scy,sr,rcx,rcy,A,B,np.degrees(ang)))
    lab,k=ndimage.label(s>0,np.ones((3,3))); print('losse delen',k)
    diff=s!=r1
    Z={'Saturnus':SATZ,'asteroide':DL1==3,'ijs':DL1==1}
    for z,m in Z.items(): print('zone %-9s diff %d px'%(z,(diff&m).sum()))
    buiten=diff&~(SATZ|(DL1==3)|(DL1==1)); print('BEWIJS: diff buiten de drie zones =',buiten.sum())
