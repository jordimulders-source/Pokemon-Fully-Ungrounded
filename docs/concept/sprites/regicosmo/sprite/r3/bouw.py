# Regicosmo r3 = r2 + Saturnus opnieuw (Jordi, 28 nov: "kan je de band van links niet pakken met de bol in het midden (dat je
# die dan wel rond maakt?)" · "en hij moet ongeveer even groot zijn als de ijsplaneet"). Buiten Saturnus pixeldiff 0 met r2.
# Bouwen: cd docs/concept/sprites/regicosmo && python3 sprite/r3/bouw.py && python3 sprite/r3/vel.py
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from scipy import ndimage; import pal, gemeen as g, kaal as kl, saturnus as sa
D=g.D
r2=np.load(os.path.join(D,'r2.npy')); DL2=np.load(os.path.join(D,'r2_deel.npy'))
s=r2.copy(); DL=DL2.copy(); log=[]
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
# r3: bol = diameter van de ijsplaneet (10 px), ring met de bol in het midden; zelfde kanteling en verhouding b/a als r2,
# zo lang als past binnen x48-63 (2 px vrij tot Mars).
A2=(amaj-1.75)*kl.s; B2=bmin*kl.s          # r2: a=7,27 b=1,68
scx,scy=56.0,30.0; sr=5.0                  # bol x51-60, y25-34 (ijsplaneet x1-10, y25-34)
rcx,rcy=scx,scy
def xbereik(A,B): return np.sqrt((A*np.cos(ang))**2+(B*np.sin(ang))**2)
A=A2
while xbereik(A+0.01,(A+0.01)*B2/A2)+0.95<scx-47.5: A+=0.01
B=A*B2/A2
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
for y in range(18,42):
    for x in range(44,64):
        d=np.hypot(PX-(x+0.5),PY-(y+0.5)); i=d.argmin(); dmin[y,x]=d[i]; voorz[y,x]=np.sin(T[i])>0
band=dmin<=0.95
U=(X+0.5-rcx)*np.cos(ang)+(Y+0.5-rcy)*np.sin(ang); W=-(X+0.5-rcx)*np.sin(ang)+(Y+0.5-rcy)*np.cos(ang)
# a) bol: planeetkleur per pixel = meerderheid van de planeetkleuren in de modelcel
# planeetkleur: de modelbol (middelpunt cx,cy, straal r natief) geschaald naar deze bol; per spritepixel de meerderheid
# van de planeetkleuren in de bijbehorende natieve cel (strepen en tinten uit het model)
f=r/sr
for y,x in zip(*np.where(bol)):
    sub=(np.arange(8)+0.5)/8
    xs=np.clip((cx+(x+sub-scx)*f).astype(int),0,deel.shape[1]-1); ys=np.clip((cy+(y+sub-scy)*f).astype(int),0,deel.shape[0]-1)
    yy,xx=np.meshgrid(ys,xs,indexing='ij'); yy=yy.ravel(); xx=xx.ravel()
    cc=C[yy,xx]; m=(deel[yy,xx]==2)&np.isin(cc,[2,3,4,5])
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
# r3: grijs mag niet op de buitenrand liggen (geen lichte kleur op de buitenlijn): heeft een grijze pixel een lege 4-buur
# buiten de ellips, dan wordt die buur ringrand (binnen x48-63, y22-37: 2 px vrij tot Mars); past dat niet, dan wordt de
# grijze pixel zelf rand.
for y,x in zip(*np.where(grijs)):
    for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
        if not (0<=xx<64 and 0<=yy<64): grijs[y,x]=False; continue
        if zicht[yy,xx] or bol[yy,xx]: continue
        if (U[yy,xx]/A)**2+(W[yy,xx]/B)**2<1: continue        # binnenkant (lusgat) blijft leeg
        if 48<=xx<=63 and 22<=yy<=37: zicht[yy,xx]=True
        else: grijs[y,x]=False
rand=zicht&~grijs
n[grijs]=13
# ringrand: tegen de achtergrond aan de schaduwkant (normaal van de ellips naar rechts/onder) zwart, anders bruin donker
gnx=U*np.cos(ang)/A**2-W*np.sin(ang)/B**2; gny=U*np.sin(ang)/A**2+W*np.cos(ang)/B**2
buiten=(U/A)**2+(W/B)**2>1
for y,x in zip(*np.where(rand)):
    tegen_bg=any((not(0<=xx<64)) or not(bol[yy,xx] or zicht[yy,xx]) for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)))
    sgn=1 if buiten[y,x] else -1
    n[y,x]=1 if (tegen_bg and sgn*(0.6*gnx[y,x]+0.8*gny[y,x])>0) else 6

M2=((n!=s)|(DL2==2))&(n>0)
DL[M2]=2
# zwart alleen aan de schaduwkant: zwarte randpixel met lege buur links/boven en geen lege buur rechts/onder -> bruin donker
for y,x in zip(*np.where((n==1)&M2)):
    e=lambda yy,xx: not(0<=xx<64) or n[yy,xx]==0
    if (e(y,x-1) or e(y-1,x)) and not (e(y,x+1) or e(y+1,x)): n[y,x]=6
stap('Saturnus bol+ring',n)
SATZ=(DL==2)|(DL2==2)
def compact(idx,P):
    used=[0]+[i for i in range(1,len(P)) if (idx==i).any()]
    m=np.zeros(256,'uint8'); m[used]=np.arange(len(used)); return m[idx],[P[i] for i in used]
if __name__=='__main__':
    uit,P2=compact(s,g.PAL)
    pal.opslaan(uit,os.path.join(D,'regicosmo_r3.png'),P2)
    np.save(os.path.join(D,'r3.npy'),s); np.save(os.path.join(D,'r3_deel.npy'),DL)
    for nm,d,_ in log: print(nm,d)
    print('kleuren (incl. transparant)',len(P2))
    print('Saturnus: bol c=(%.2f,%.2f) r=%.2f; ring a=%.2f b=%.2f hoek %.1f (r2: a=%.2f b=%.2f)'%(scx,scy,sr,A,B,np.degrees(ang),A2,B2))
    ys,xs=np.where(DL==2); print('Saturnus bbox x%d-%d y%d-%d'%(xs.min(),xs.max(),ys.min(),ys.max()))
    lab,k=ndimage.label(s>0,np.ones((3,3))); print('losse delen',k)
    pts=[np.argwhere(lab==i) for i in range(1,k+1)]; si=lab[ys[0],xs[0]]-1
    for j in range(k):
        if j!=si:
            d=np.abs(pts[si][:,None,:]-pts[j][None,:,:]).max(2).min()
            if d<6: print('  lege px tussen Saturnus en deel bij',pts[j].mean(0).round(),':',d-1)
    diff=s!=r2
    print('zone Saturnus diff',(diff&SATZ).sum(),'| BEWIJS: diff buiten Saturnus =',(diff&~SATZ).sum())
