# Pitahaya-draak fase 2, r2 op r1: alleen benoemde reparaties, alles uit het model (natief.png + groepen.py).
#  1 BEK  (zone X 5-19, Y 43-56, binnenpixels, geen groen): per spritepixel opnieuw uit zijn 3x3 modelblok:
#         vruchtvlees bij >= 4 wit/pit-px (toon: gem. helderheid wit >= 215 -> licht, anders grijs),
#         lijn bij >= 3 zwarte px, anders roze (gemiddelde -> dichtstbijzijnde roze modeltoon).
#         Pitjes: elke pitcomponent van het model -> spritepixel van zijn zwaartepunt; groot eerst;
#         alleen op vlees, niet op de vleesrand, nooit 8-naast elkaar.
#  2 KAAKLIJN: rij 42 X 3-9 doorlopend zwart, tanden 1 px wit op (43,4) en (43,8) (modeltanden), geen ander wit.
#  3 NADEN LIJF: binnenzwart in het roze lijf (blok zonder groen, >= 4 roze px; X >= 19, buiten de bek)
#         -> blokgemiddelde = donkerste roze (113,43,55) (model: 1 natieve px zwart naast 2 roze per rij).
#  4 KOP-ROZE: binnenvulling roze van de kop (X <= 24, Y <= 42, buiten oog) uit de modelluminantie per blok
#         (sigma S), drempels uit de modelverdeling van de kop (zelfde aandeel per toon als het model).
import sys,numpy as np; from PIL import Image; from collections import Counter
from groepen import laad
R1=Image.open('pitahaya2_r1.png'); r1=np.asarray(R1).astype(int); pal=R1.getpalette()
a,lum,g=laad(); o=r1.copy(); log=[]
P=np.array(pal[:39]).reshape(13,3); PL=P@[0.299,0.587,0.114]
def zet(y,x,v,stap):
    if o[y,x]!=v: log.append((stap,y,x,o[y,x],v)); o[y,x]=v
def blok(Y,X): return slice(3*(Y-13),3*(Y-13)+3),slice(2+3*X,5+3*X)
m=r1>0; pad=np.pad(m,1); rand=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
ROZE=[2,3,4,5]; GROEN={6,7,8,9}
OOG=lambda y,x: 12<=x<=18 and 37<=y<=42
def roze_toon(c): return ROZE[int(((P[ROZE]-c)**2).sum(1).argmin())]
# 1 bek
Z1=[(y,x) for y in range(43,57) for x in range(5,20) if (y,x)!=(43,9) and m[y,x] and not rand[y,x] and r1[y,x] not in GROEN]
VLEES=set()
for y,x in Z1:
    sl=blok(y,x); gb=g[sl]; nf=((gb==6)|(gb==7)).sum(); nz=(gb==1).sum(); nr=(gb==2).sum()
    if nf>=4:
        w=gb==6; L=lum[sl][w].mean() if w.any() else 200
        zet(y,x,11 if L>=215 else 10,'1 vlees'); VLEES.add((y,x))
    elif nz>=3: zet(y,x,1,'1 lijn')
    elif nr: zet(y,x,roze_toon(a[sl][gb==2].mean(0)),'1 roze')
    else: zet(y,x,1,'1 lijn')
# pitcomponenten uit het model
H,W=g.shape; seen=np.zeros((H,W),bool); comps=[]
for y0,x0 in zip(*np.where(g==7)):
    if seen[y0,x0]: continue
    st=[(y0,x0)]; seen[y0,x0]=1; cl=[]
    while st:
        y,x=st.pop(); cl.append((y,x))
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if g[y+dy,x+dx]==7 and not seen[y+dy,x+dx]: seen[y+dy,x+dx]=1; st.append((y+dy,x+dx))
    cy=np.mean([c[0] for c in cl]); cx=np.mean([c[1] for c in cl])
    comps.append((len(cl),int(cy)//3+13,(int(cx)-2)//3))
PITS=[]
RANDMAX=int(sys.argv[sys.argv.index('--rand')+1]) if '--rand' in sys.argv else 1
for n,y,x in sorted(comps,reverse=True):
    if (y,x) not in VLEES: continue
    if sum((y+dy,x+dx) not in VLEES for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))>RANDMAX: continue
    if any(abs(y-py)<=1 and abs(x-px)<=1 for py,px in PITS): continue
    if any((y==py and abs(x-px)<=2) or (x==px and abs(y-py)<=2) for py,px in PITS): continue   # geen rij/kolom-paartje op 2 px (leest als dobbelsteen)
    PITS.append((y,x))
for y,x in PITS: zet(y,x,12,'1 pit')
# 2 kaaklijn
for x in range(3,10): zet(42,x,1,'2 kaaklijn')
zet(43,4,11,'2 tand'); zet(43,8,11,'2 tand')
# 3 naden lijf
for y,x in zip(*np.where((r1==1)&~rand)):
    if x<19 or (y>=43 and x<=19): continue
    sl=blok(y,x); gb=g[sl]
    if (gb==4).any() or (gb==2).sum()<4: continue
    zet(y,x,roze_toon(a[sl].mean(0)) if False else 2,'3 naad')
# 4 kop-roze
S=float(sys.argv[sys.argv.index('--S')+1]) if '--S' in sys.argv else 0.8
def gauss(x,s):
    if s<=0: return x
    r=int(3*s)+1; k=np.exp(-0.5*(np.arange(-r,r+1)/s)**2); k/=k.sum()
    y=np.apply_along_axis(lambda v: np.convolve(v,k,'same'),0,x); return np.apply_along_axis(lambda v: np.convolve(v,k,'same'),1,y)
mg=(g==2).astype(float); TK=gauss(lum*mg,S)/np.maximum(gauss(mg,S),1e-6)
kop=[(y,x) for y in range(30,43) for x in range(2,25) if m[y,x] and not rand[y,x] and o[y,x] in (3,4,5) and not OOG(y,x)]
# modelverdeling van de kop: natieve roze px in hetzelfde gebied, naar dichtstbijzijnde toon (3,4,5)
ny0,ny1=3*(30-13),3*(43-13); nx0,nx1=2+3*2,2+3*25
kp=a[ny0:ny1,nx0:nx1][g[ny0:ny1,nx0:nx1]==2]
tl=np.array([ROZE[int(((P[ROZE]-c)**2).sum(1).argmin())] for c in kp])
aand={t:(tl==t).sum() for t in (3,4,5)}; tot=sum(aand.values())
waarden=[]
for y,x in kop:
    sl=blok(y,x); gm=g[sl]==2
    if gm.sum()<3: continue
    if (g[sl]==1).sum()>=3: continue
    waarden.append((TK[sl][gm].mean(),y,x))
waarden.sort(); n=len(waarden); i=0
for t in (3,4,5):
    k=round(n*aand[t]/tot) if t!=5 else n-i
    for _ in range(k):
        if i<n: _,y,x=waarden[i]; zet(y,x,t,'4 kop-roze'); i+=1
UIT=sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('--') else 'pitahaya2_r2.png'
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal); p.save(UIT,transparency=0)
# bewijs: diff buiten de zones = 0
ZONES=set(Z1)|{(42,x) for x in range(3,10)}|{(43,4),(43,8)}
ZONES|={(y,x) for y,x in zip(*np.where((r1==1)&~rand)) if not(x<19 or (y>=43 and x<=19))}
ZONES|={(y,x) for _,y,x in waarden}
diff=set(zip(*np.where(o!=r1))); buiten=[d for d in diff if d not in ZONES]
assert not buiten, buiten
assert ((o>0)==(r1>0)).all()
m2=o>0; print('modelaandeel kop 3/4/5:',{k:round(v/tot,2) for k,v in aand.items()})
print('gewijzigd',len(diff),'buiten zones',len(buiten),'pits',len(PITS),PITS,
      'zwart binnen %.1f%%'%(100*((o==1)&~rand).sum()/m2.sum()),'kleuren',len(set(o.ravel()))-1)
cnt=Counter(s for s,*_ in log); print(cnt)
open(UIT[:-4]+'_afwijkingen.txt','w').write('\n'.join(f'{s}\t({x},{y})\t{a_}->{b}' for s,y,x,a_,b in log)+'\n')
