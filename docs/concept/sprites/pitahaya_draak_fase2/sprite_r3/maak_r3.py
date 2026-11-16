# Pitahaya-draak fase 2, r3 op r2: reparaties 1, 2, 4, 5 uit keuring_r2/KEURING.md (+ variant lipB = reparatie 3).
# Alles uit het model (natief.png via groepen.py, 3x3-blok per spritepixel). Niets getekend.
# Gebruik: python3 maak_r3.py [--lipB]
import sys,numpy as np; from PIL import Image; from collections import Counter
from groepen import laad
R2=Image.open('pitahaya2_r2.png'); r2=np.asarray(R2).astype(int); pal=R2.getpalette()
a,lum,g=laad(); o=r2.copy(); log=[]; ZONES=set()
P=np.array(pal[:39]).reshape(13,3); PL=P@[0.299,0.587,0.114]
N={0:'.',1:'K',2:'d',3:'r',4:'p',5:'P',6:'g',7:'G',8:'h',9:'H',10:'w',11:'W',12:'s'}
def zet(y,x,v,stap):
    ZONES.add((y,x))
    if o[y,x]!=v: log.append((stap,y,x,o[y,x],v)); o[y,x]=v
def blok(Y,X): return slice(3*(Y-13),3*(Y-13)+3),slice(2+3*X,5+3*X)
def toon(Y,X,grp,tonen):
    sl=blok(Y,X); gb=g[sl]==grp; c=a[sl][gb].mean(0); return tonen[int(((P[tonen]-c)**2).sum(1).argmin())],c
def cluster_merge(zone,tonen,stap,rondes=3):
    # clusters < 3 px (4-verbonden, zelfde toon) in de zone -> meest voorkomende 4-buurtint uit dezelfde groep;
    # gelijkspel: de toon die het modelblok het dichtst benadert
    zs=set(zone)
    for _ in range(rondes):
        seen=set(); veranderd=False
        for p in zone:
            if p in seen or o[p] not in tonen: continue
            v=o[p]; st=[p]; cl=[]; seen.add(p)
            while st:
                q=st.pop(); cl.append(q)
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    n=(q[0]+dy,q[1]+dx)
                    if n not in seen and o[n]==v: seen.add(n); st.append(n)
            if len(cl)>=3: continue
            for y,x in cl:
                if (y,x) not in zs: continue
                nb=Counter(o[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if o[y+dy,x+dx] in tonen and o[y+dy,x+dx]!=v)
                if not nb: continue
                top=max(nb.values()); kand=[t for t,c in nb.items() if c==top]
                if len(kand)>1:
                    _,c=toon(y,x,2 if tonen[0]<6 else 4,tonen); kand.sort(key=lambda t:((P[t]-c)**2).sum())
                zet(y,x,kand[0],stap); veranderd=True
        if not veranderd: break
ROZE=[2,3,4,5]; LICHTROZE=[3,4,5]; GROEN=[6,7,8,9]
# 1 mondhoek x15-19, y44-51: r/p/P (+ W (15,49)) uit het modelblok, dan clusters < 3 px samenvoegen
Z1=[(y,x) for y in range(44,52) for x in range(15,20) if r2[y,x] in (3,4,5) or (y,x)==(49,15)]
for y,x in Z1:
    sl=blok(y,x); gb=g[sl]
    if ((gb==6)|(gb==7)).sum()>=4: continue
    # strookregel: blokgemiddelde (alleen roze modelpx); ligt lichtroze P bij de twee dichtstbijzijnde tonen -> P
    # (de lichte modelstreep langs de bekrand, die bij losse 'dichtstbijzijnde' P/p om en om wisselde), anders p bij de twee -> p, anders r
    c=a[sl][gb==2].mean(0); d=((P[ROZE]-c)**2).sum(1); top2=[ROZE[i] for i in np.argsort(d)[:2]]
    zet(y,x,5 if 5 in top2 else 4 if 4 in top2 else 3,'1 mondhoek')
cluster_merge(Z1,LICHTROZE,'1 mondhoek cluster',1)
# 2 linker lipband onderkaak (7,50)-(7,53): d -> r (modeltoon lipband, 70-100 % roze)
for y in range(50,54):
    assert r2[y,7]==2; zet(y,7,3,'2 lipband')
# 4 dambord: voorvoet links x11-13, y57-58 uit de gladde groene modelluminantie (sigma 1,5) + clusterregel
def gauss(x,s):
    r=int(3*s)+1; k=np.exp(-0.5*(np.arange(-r,r+1)/s)**2); k/=k.sum()
    y=np.apply_along_axis(lambda v: np.convolve(v,k,'same'),0,x); return np.apply_along_axis(lambda v: np.convolve(v,k,'same'),1,y)
mg=(g==4).astype(float); TK=gauss(lum*mg,1.5)/np.maximum(gauss(mg,1.5),1e-6)
Z4=[(y,x) for y in (57,58) for x in range(11,14) if r2[y,x] in GROEN]
m=r2>0; pad=np.pad(m,1); rand=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
for y,x in Z4:
    if rand[y,x]: continue
    sl=blok(y,x); gm=g[sl]==4; L=TK[sl][gm].mean()
    zet(y,x,GROEN[int(np.abs(PL[GROEN]-L).argmin())],'4 voorvoet')
# toonkaart geeft hier dezelfde tinten als r2 (om en om zit in het model zelf, blokken op de grens G/g);
# dambord oplossen: per 2x2 om-en-om 1 px naar de tint die zijn modelblok (groene px) het dichtst benadert
for _ in range(4):
    vond=False
    for y0 in (56,57,58):
        for x0 in (10,11,12,13):
            q=o[y0:y0+2,x0:x0+2]
            if not((q>0).all() and q[0,0]==q[1,1] and q[0,1]==q[1,0] and q[0,0]!=q[0,1]): continue
            if not all(v in GROEN for v in q.ravel()): continue
            best=None
            for y,x in ((y0,x0),(y0,x0+1),(y0+1,x0),(y0+1,x0+1)):
                if not (11<=x<=13 and 57<=y<=58) or rand[y,x]: continue
                ander=q[0,1] if o[y,x]==q[0,0] else q[0,0]
                sl=blok(y,x); gm=g[sl]==4; L=lum[sl][gm].mean(); d=abs(L-PL[ander])-abs(L-PL[o[y,x]])
                if best is None or d<best[0]: best=(d,y,x,ander)
            if best: zet(best[1],best[2],best[3],'4 voorvoet dambord'); vond=True
    if not vond: break
#    losse dambordjes (9,36) r/p en (39,46) d/r: 1 px naar de tint die het modelblok het dichtst benadert
for y0,x0 in ((36,9),(46,39),(47,17)):   # (17,47) = dambord p/P dat de strookregel in de mondhoek achterliet
    best=None
    for y,x in ((y0,x0),(y0,x0+1),(y0+1,x0),(y0+1,x0+1)):
        q=o[y0:y0+2,x0:x0+2]; ander=q[0,1] if o[y,x]==q[0,0] else q[0,0]
        _,c=toon(y,x,2,ROZE); d=((P[ander]-c)**2).sum()-((P[o[y,x]]-c)**2).sum()
        if best is None or d<best[0]: best=(d,y,x,ander)
    zet(best[1],best[2],best[3],'4 dambord')
# 5 onderste lipband (9,53),(10,53): W -> roze uit het model; (12,54) K -> p alleen als de buitenlijn op rij 55 sluit
for x in (9,10):
    t,_=toon(53,x,2,LICHTROZE); zet(53,x,t,'5 lipband onder')
if r2[55,12]!=0: zet(54,12,4,'5 lipband onder')
else: print('5: (12,54) blijft K: (12,55) is transparant, de buitenlijn zou openvallen')
# variant B: verre lip (11,46),(12,45) -> r
if '--lipB' in sys.argv:
    for y,x in ((46,11),(45,12)): zet(y,x,3,'3 verre lip (variant B)')
UIT='pitahaya2_r3_lipB.png' if '--lipB' in sys.argv else 'pitahaya2_r3.png'
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal); p.save(UIT,transparency=0)
diff=set(zip(*np.where(o!=r2))); buiten=[d for d in diff if d not in ZONES]
assert not buiten,buiten; assert ((o>0)==(r2>0)).all()
db=[(x,y) for y in range(63) for x in range(63) if (o[y:y+2,x:x+2]>0).all() and o[y,x]==o[y+1,x+1] and o[y,x+1]==o[y+1,x] and o[y,x]!=o[y,x+1]]
mm=o>0; print(UIT,'gewijzigd t.o.v. r2',len(diff),'buiten zones 0, silhouet-diff 0',
  'zwart binnen %.1f%%'%(100*((o==1)&~rand).sum()/mm.sum()),'kleuren',len(set(o.ravel()))-1)
print('dambord over (x,y):',[(x,y,N[o[y,x]],N[o[y,x+1]]) for x,y in db])
print(Counter(s for s,*_ in log))
open(UIT[:-4]+'_afwijkingen.txt','w').write('\n'.join(f'{s}\t({x},{y})\t{N[a_]}->{N[b]}' for s,y,x,a_,b in log)+'\n')
