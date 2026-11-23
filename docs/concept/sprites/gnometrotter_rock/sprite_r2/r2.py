# r2.py: Gnometrotter Rock ronde 2. Basis = r1 (zelfde gedeelde reductie, silhouet en onderdelen: ../sprite/zone_af.npy).
# Nieuw: de vlakken komen uit de MODELFACETTEN (facetten.py): elke spritepixel hoort bij het facet dat het grootste deel van zijn
# modelvlak bedekt; facetgrenzen = de modelnaden op hun gemeten plek (1 px, op de pixel met de meeste modellijn); per facet grote
# vlakken (meerderheidsfilter binnen het facet); lijf en benen Gen 3-volume zoals Gnomad; daarna DC-omlijning.
import sys, numpy as np; from scipy import ndimage as nd
sys.path.insert(0,'../sprite')
from gemeen import *
from reductie_gedeeld import bron
R1='../sprite/'
zone=np.load(R1+'zone_af.npy'); kl=np.load(R1+'lijnkans.npy'); vlak=np.load(R1+'vlak.npy'); r1=lees(R1+'gnometrotter_rock.png')
d=np.load('facet_full.npz'); F=d['F']; FZ=d['FZ']
fg=r1>0; zone[~fg]=0
# ruis in de onderdelenkaart: losse stukjes van een onderdeel (< 5 px, bv. roze tussen muts, baard en haar R) -> omringend onderdeel
zone0=zone.copy(); SNIP=[]
for z in range(1,15):
    lab,n=nd.label(zone0==z)
    for i in range(1,n+1):
        m=lab==i
        if m.sum()>=5 or z==11: continue
        r=nd.binary_dilation(m)&~m&fg&(zone0!=z)
        if r.any(): zone[m]=np.bincount(zone0[r]).argmax(); SNIP+=[(int(x),int(y),ZNAAM[z],ZNAAM[zone[y,x]]) for y,x in zip(*np.where(m))]
# uitlopers van 1 px breed (pixel met hooguit 1 buur van hetzelfde onderdeel) in lijf/muts/haar/baard -> buuronderdeel
for _ in range(3):
    for Y,X in zip(*np.where(np.isin(zone,[1,2,3,4,6]))):
        z=zone[Y,X]; nb=[zone[Y+dy,X+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=Y+dy<64 and 0<=X+dx<64]
        if nb.count(z)<=1:
            ander=[v for v in nb if v not in (0,z)]
            if ander: zone[Y,X]=max(set(ander),key=ander.count); SNIP.append((int(X),int(Y),ZNAAM[z],ZNAAM[zone[Y,X]]))
print('onderdeelsnippers',SNIP)
# 1. facet per spritepixel (meerderheid binnen het eigen onderdeel); geen facet -> dichtstbijzijnde facet van hetzelfde onderdeel
fac=np.zeros((64,64),int)
for Y,X in zip(*np.where(fg)):
    w={}
    for u,v,ww in bron(X,Y):
        i=F[v,u]
        if i and FZ[i]==zone[Y,X]: w[i]=w.get(i,0)+ww
    if w: fac[Y,X]=max(w,key=w.get)
for z in range(1,15):
    m=(zone==z); heb=m&(fac>0)
    if not m.any() or not heb.any(): continue
    _,(iy,ix)=nd.distance_transform_edt(~heb,return_indices=True)
    leeg=m&(fac==0); fac[leeg]=fac[iy[leeg],ix[leeg]]
# 2. kleine facetten (< 6 spritepx) -> buurfacet van hetzelfde onderdeel met de langste gedeelde rand
for _ in range(3):
    for i in np.unique(fac[fac>0]):
        m=fac==i
        if m.sum()>=6: continue
        rand=nd.binary_dilation(m)&~m&(zone==FZ[i])&(fac>0)
        if rand.any(): fac[m]=np.bincount(fac[rand]).argmax()
# 3. tinten
o=np.zeros((64,64),int)
ROTS=[1,2,3,4,10,11,13,14]
for Y,X in zip(*np.where(fg)): o[Y,X]=vlak[Y,X] if vlak[Y,X] in RAMP[zone[Y,X]] else RAMP[zone[Y,X]][0]
for x,y,_,_ in SNIP: o[y,x]=RAMP[zone[y,x]][0]
o[np.isin(r1,ROZE+BLAUW)&np.isin(zone,[5,7,8,9])]=r1[np.isin(r1,ROZE+BLAUW)&np.isin(zone,[5,7,8,9])]   # neus, armen, handen: tinten van r1 (model)
# gesteente: grote vlakken = meerderheidsfilter 5x5 binnen hetzelfde facet (2 rondes)
for _ in range(2):
    o2=o.copy()
    for Y,X in zip(*np.where(np.isin(zone,ROTS))):
        y0,y1,x0,x1=max(0,Y-2),Y+3,max(0,X-2),X+3
        m=fac[y0:y1,x0:x1]==fac[Y,X]; t=o[y0:y1,x0:x1][m]
        c=np.bincount(t,minlength=16); o2[Y,X]=c.argmax()
    o=o2
# Gen 3-volume (licht linksboven) zoals Gnomad: bol per lichaamsdeel, schaduwsikkel rechts
l=np.array([-0.55,-0.6,0.58]); l/=np.linalg.norm(l)
def I(X,Y,cx,cy,rx,ry):
    nx=(X+0.5-cx)/rx; ny=(Y+0.5-cy)/ry; r2=nx*nx+ny*ny
    n=np.array([nx,ny,np.sqrt(max(0.04,1-min(r2,0.96)))]); n/=np.linalg.norm(n); return float(n@l)
def ell(m):
    yy,xx=np.where(m); return (xx.min()+xx.max()+1)/2,(yy.min()+yy.max()+1)/2,(xx.max()-xx.min()+1)/2,(yy.max()-yy.min()+1)/2
lijf=zone==6; E=ell(lijf&(np.arange(64)[:,None]>=22))     # buikbol zonder het gezicht onder de muts
for Y,X in zip(*np.where(lijf)):
    i=I(X,Y,*E); o[Y,X]=15 if i>=0.85 else (8 if i>=0.12 else 7)
# slagschaduw: gezicht onder de muts en de 2 rijen onder muts/neus/baard/haar liggen in de schaduw (model: donkerroze)
for Y,X in zip(*np.where(lijf)):
    if Y<22 or any(zone[Y-k,X] in (1,2,3,4,5) for k in (1,2) if Y-k>=0): o[Y,X]=7
blauw=zone==12; yy,xx=np.where(blauw)
# kruis: de kolom in het onderste deel van het blauw zonder blauw (tussen de benen)
onder=blauw[50:58]; gat=[x for x in range(xx.min(),xx.max()) if not onder[:,x].any()]; split=int(np.median(gat)) if gat else 33
for kant in (blauw&(np.arange(64)[None,:]<split), blauw&(np.arange(64)[None,:]>=split)):
    E=ell(kant)
    for Y,X in zip(*np.where(kant)):
        i=I(X,Y,*E); o[Y,X]=11 if i>=0.30 else (10 if i>=-0.45 else 9)
# tintvlekjes < 3 px in lijf en benen (randen van de volumebanden) -> meest voorkomende buurtint van hetzelfde onderdeel
for zz in (6,12):
    for k in RAMP[zz]:
        lab,n=nd.label((o==k)&(zone==zz),structure=np.ones((3,3)))
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=3: continue
            r=nd.binary_dilation(m,structure=np.ones((3,3)))&~m&(zone==zz); t=o[r]; t=t[t!=k]
            if len(t): o[m]=np.bincount(t).argmax()
# 4. lijnen
OUT=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg)):
    if any(not(0<=Y+dy<64 and 0<=X+dx<64) or not fg[Y+dy,X+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): OUT[Y,X]=True
rank={p:i for i,p in enumerate(PRIO)}
LIJN=OUT.copy()
for Y,X in zip(*np.where(fg&~OUT)):          # onderdeelgrens: lijn op het voorste onderdeel
    if any(zone[Y+dy,X+dx]!=zone[Y,X] and rank[zone[Y+dy,X+dx]]>rank[zone[Y,X]] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): LIJN[Y,X]=True
naad=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg&~LIJN)):        # facetgrens binnen een onderdeel: 1 px, op de pixel met de meeste modellijn
    for dy,dx in ((1,0),(0,1)):
        y,x=Y+dy,X+dx
        if y<64 and x<64 and fg[y,x] and zone[y,x]==zone[Y,X] and fac[y,x]!=fac[Y,X] and not LIJN[y,x]:
            if naad[Y,X] or naad[y,x]: continue
            if kl[Y,X]>kl[y,x]: naad[Y,X]=True
            else: naad[y,x]=True
# naadstompjes < 3 px die geen andere lijn raken weg
lab,n=nd.label(naad,structure=np.ones((3,3)))
for i in range(1,n+1):
    m=lab==i
    if m.sum()<3 and not (nd.binary_dilation(m,structure=np.ones((3,3)))&LIJN).any(): naad[m]=False
LIJN|=naad
LICHT=np.array([-0.6,-0.8])
def normaal(Y,X):
    v=np.zeros(2)
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if (dy or dx) and (not(0<=Y+dy<64 and 0<=X+dx<64) or not fg[Y+dy,X+dx]): v+=(dx,dy)
    n_=np.linalg.norm(v); return v/n_ if n_ else v
for Y,X in zip(*np.where(LIJN)):
    o[Y,X]=(BASIS[zone[Y,X]] if normaal(Y,X)@LICHT>0.35 else 1) if OUT[Y,X] else BASIS[zone[Y,X]]
# naden in baard/haar middengrijs (4) i.p.v. de buitenlijnkleur 2: lichtgrijs vlak + middengrijs facetlijnen zoals het model
for Y,X in zip(*np.where(naad&np.isin(zone,[2,3,4]))): o[Y,X]=4
for zz in (5,9,8):     # ronde delen: rand in 6, zwarte boog linksmidden-linksonder-ondermidden (SPRITE_KERN)
    m=zone==zz; yy,xx=np.where(m); cy,cx=yy.mean(),xx.mean()
    rand=m&nd.binary_dilation(~m,structure=np.array([[0,1,0],[1,1,1],[0,1,0]]))
    for Y,X in zip(*np.where(rand)):
        h=np.degrees(np.arctan2(Y-cy,X-cx)); o[Y,X]=1 if 80<=h<=190 else 6
np.save('fac.npy',fac); np.save('zone.npy',zone); np.save('naad.npy',naad)
opslaan(o,'stap1.png')
print('facetten in sprite',len(np.unique(fac[fac>0])),'naadpx',naad.sum(),'split',split)
