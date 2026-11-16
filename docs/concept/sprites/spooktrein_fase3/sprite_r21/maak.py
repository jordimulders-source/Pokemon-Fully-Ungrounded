# r21 koeienvanger = r20 + tinten per blad uit het model (Jordi 16 nov: "die koeienvanger moet trouwens nog beter").
# Silhouet, V-bovenrand, naden en spleten (zwart) van r20 blijven: die liggen al op het modelskelet (r18 kv.py) en het
# geprojecteerde modelsilhouet (natief.png, 0,744x, 2 px rechts, 1 rij hoger). Nieuw: per blad (samenhangend vlak tussen
# de lijnen) de toon uit de gladgestreken modelluminantie (toonkaart, zoals de kop in r18): lichte kant 7/10, midden 11,
# donkere kant 12; roest 8/9 waar het model roest heeft (>=50% van de voetafdruk, vlekken >=2 px).
# Bevroren (assert): alles buiten KV (x0-26, y45-60), alle groen, alle zwart (lijnen, buitenlijn).
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r18')
from kv import *
from collections import Counter
im=Image.open(D+'sprite_r20/sprite.png'); r=np.array(im).astype(int); pal=im.getpalette()
GRS=[2,3,4,5,6,13]
KV=np.zeros((64,64),bool); KV[45:61,0:27]=True
groen=np.isin(r,GRS)
# band boven de V-lijn (roest tussen grijns en V) blijft zoals r20
vcells=[c for c in dun(raster(V)) if KV[c]]
vmin={}
for (y,x) in vcells: vmin[x]=min(vmin.get(x,99),y)
band=np.zeros((64,64),bool)
for x,v in vmin.items(): band[:v,x]=True
rnd=np.array([[r[y,x]!=0 and (x==0 or 0 in nb4(r,y,x)) for x in range(64)] for y in range(64)])
vul=KV&np.isin(r,[7,8,9,10,11,12])&~band&~rnd          # buitenrand (selout) blijft
# toonkaart: modelluminantie (ijzer, geen lijn/groen/wit) 3x3 gladgestreken, per spritecel gewogen gemiddeld
def uniform_filter(A,k):
    P=np.pad(A,k//2,mode='edge'); return sum(P[i:i+A.shape[0],j:j+A.shape[1]] for i in range(k) for j in range(k))/k/k
IJ=(~G&~WIT&(LUM>=52)).astype(float)
LS=uniform_filter(LUM*IJ,3)/np.maximum(uniform_filter(IJ,3),1e-6)
def tl(x,y):
    f=[(w,ny,nx) for w,ny,nx in foot(x,y)]; W=sum(w for w,_,_ in f)
    return sum(w*LS[ny,nx] for w,ny,nx in f)/W
def rf(x,y): return frac(RUSTM,x,y,IJZM)
def roze(x,y):   # lichte modelkleur is roze-grijs (7), niet grijs (10)?
    f=[(w,ny,nx) for w,ny,nx in foot(x,y) if IJZM[ny,nx] and LUM[ny,nx]>135]; W=sum(w for w,_,_ in f)
    return W and sum(w*(N[ny,nx,0]-N[ny,nx,2]) for w,ny,nx in f)/W>22
Y,X=np.mgrid[0:64,0:64]
a=r.copy()
# 1. per cel de modelklassen in de voetafdruk (natieve pixels -> dichtstbijzijnde modeltint). Dunne lichte randen winnen
#    (zoals bij de ijskomeet de donkerste pixel won voor lijnen): >=LT licht -> lichte kant; dan roest, donkere kant, grijs.
KL={1:(28,25,18),7:(178,153,138),10:(153,143,137),11:(101,99,92),12:(69,69,65),8:(154,101,72),9:(115,64,46),14:(188,128,88)}
NK=np.zeros((99,99),int)
for ny in range(99):
    for nx in range(99):
        if WIT[ny,nx] or G[ny,nx]: continue
        c=N[ny,nx]; NK[ny,nx]=min(KL,key=lambda k:sum((KL[k][i]-c[i])**2 for i in range(3)))
NK[NK==14]=8
LT=float(sys.argv[1]) if len(sys.argv)>1 else 0.3
LTV=float(sys.argv[3]) if len(sys.argv)>3 else 0.15
vset=set(vcells)
RT=float(sys.argv[2]) if len(sys.argv)>2 else 0.45
for y,x in zip(*np.where(vul)):
    c=Counter()
    for w,ny,nx in foot(x,y):
        if NK[ny,nx] and NK[ny,nx]!=1: c[NK[ny,nx]]+=w
    W=sum(c.values())
    if not W: continue
    f=lambda *k: sum(c[q] for q in k)/W
    onderV=any((y-1,x+dx) in vset for dx in(-1,0,1))           # schuine bovenrand direct onder de V
    if f(7,10)>=(LTV if onderV else LT): a[y,x]=7 if c[7]>=c[10] else 10
    elif f(8,9)>=RT: a[y,x]=8 if c[8]>=c[9] else 9
    elif f(12)>=0.4: a[y,x]=12
    else: a[y,x]=11
# 2b. grijze bladen: per samenhangend grijs vlak (11/12, 4-buren) licht-donker uit de toonkaart van het model
#     (gladgestreken luminantie) + licht linksboven binnen het blad: lichte kant 10, midden 11, donkere kant 12.
GW=float(sys.argv[4]) if len(sys.argv)>4 else 0.5
for bl in comps(list(zip(*np.where(vul&np.isin(a,[11,12]))))):
    if len(bl)<6: continue
    T=np.array([tl(x,y) for y,x in bl]); Tz=(T-T.mean())/(T.std()+1e-6)
    ys=np.array([y for y,x in bl]); xs=np.array([x for y,x in bl])
    Dz=-((xs-xs.min())/(np.ptp(xs)+1)+(ys-ys.min())/(np.ptp(ys)+1)); Dz=(Dz-Dz.mean())/(Dz.std()+1e-6)
    Sb=(1-GW)*Tz+GW*Dz
    q=np.percentile(Sb,(25,75))
    for (y,x),v in zip(bl,Sb): a[y,x]=10 if v>=q[1] else (11 if v>=q[0] else 12)
# 3. opschonen: 1-px-eilandjes (8-buren) behalve glans 7 -> meest voorkomende buur in de familie
FAM={10:(7,10,11),11:(10,11,12),12:(11,12),8:(8,9),9:(8,9)}
for it in range(2):
    b=a.copy()
    for y,x in zip(*np.where(vul)):
        v=a[y,x]
        if v in FAM and nb8(a,y,x).count(v)==0:
            n=[t for t in nb8(a,y,x) if t in FAM[v]] or [t for t in nb8(a,y,x) if t in (7,8,9,10,11,12)]
            if n: b[y,x]=Counter(n).most_common(1)[0][0]
    a=b
# 4. eilandjes van 1-2 px (8-verbonden, zelfde index) in de vulling -> meest voorkomende vulbuur (geen dambord, Gen 3)
def comp8(a,y,x):
    v=a[y,x]; st=[(y,x)]; c={(y,x)}
    while st:
        yy,xx=st.pop()
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                q=(yy+dy,xx+dx)
                if ok(*q) and q not in c and a[q]==v: c.add(q); st.append(q)
    return c
for it in range(3):
    for y,x in zip(*np.where(vul)):
        c=comp8(a,y,x)
        if len(c)<3 and all(vul[q] for q in c):
            n=Counter(a[q[0]+dy,q[1]+dx] for q in c for dy in(-1,0,1) for dx in(-1,0,1)
                      if ok(q[0]+dy,q[1]+dx) and (q[0]+dy,q[1]+dx) not in c and a[q[0]+dy,q[1]+dx] in (7,8,9,10,11,12))
            if n:
                for q in c: a[q]=n.most_common(1)[0][0]
# bewijs bevroren
assert (a[groen]==r[groen]).all() and not np.isin(a[~groen],GRS).any(),'groen gewijzigd'
assert (a[~KV]==r[~KV]).all(),'buiten koeienvanger gewijzigd'
assert ((a==1)==(r==1)).all() and ((a==0)==(r==0)).all(),'lijnen/silhouet gewijzigd'
if __name__=='__main__':
    d=a!=r
    print('gewijzigd in KV',int(d[KV].sum()),' buiten KV',int(d[~KV].sum()),' groen-diff',int(d[groen].sum()),' zwart/transp-diff',int(((a==1)!=(r==1)).sum()+((a==0)!=(r==0)).sum()))
    print('tinten r20',Counter(r[KV].tolist()),'\ntinten r21',Counter(a[KV].tolist()))
    for y in range(44,61): print('%2d'%y,''.join('.' if q==0 else '%X'%q for q in a[y,:28]),'  ',''.join('.' if q==0 else '%X'%q for q in r[y,:28]))
    o=Image.fromarray(a.astype(np.uint8),'P'); o.putpalette(pal); o.save(D+'sprite_r21/sprite.png',transparency=0)
