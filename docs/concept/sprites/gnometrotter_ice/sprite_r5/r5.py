# r5.py: Gnometrotter Ice r5 uit r4 (23 nov). Logt elke gewijzigde pixel per zone (r5_log.txt).
# Opdracht: romp en benen echte ijsvormen uit de modelfacetten (facet_meet.py), schaduwsikkel onder de romp,
# ovaal als eigen bal, rand bovenarm|hand aansluitend. Rest (muts, haar, baard, neus, stok, linkerhand, zolen, riem) = 0.
import numpy as np, os, runpy; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(H,'facet_meet.py'))          # -> facet_romp.npy, facet_been.npy, facet_lum.npy
FR=np.load(os.path.join(H,'facet_romp.npy')); FB=np.load(os.path.join(H,'facet_been.npy'))
LUM=np.load(os.path.join(H,'facet_lum.npy'),allow_pickle=True).item()
im=Image.open(os.path.join(H,'../sprite_r4/gnometrotter_ice.png')); o=np.asarray(im).copy(); n=o.copy()
r3=np.asarray(Image.open(os.path.join(H,'../sprite_r3/gnometrotter_ice.png')))
m=np.asarray(Image.open(os.path.join(H,'../r3/gemini_r3_lijf.png')).convert('RGB')).astype(float); lum=m.mean(2); P=8.1
PINK={6,7,8,15}; zone={}
N4=((1,0),(-1,0),(0,1),(0,-1))
def zet(x,y,v,z):
    if n[y,x]!=v: n[y,x]=v; zone[(x,y)]=z

# ---- ovaal (zelfde modelellips als r4) ----
ys,xs=np.nonzero(lum<60); MX=(xs-512)/P+32; MY=(ys-523)/P+60
sel=(MX>39.5)&(MX<51)&(MY>20.5)&(MY<30)&~((MX>50.2)&(MY>26.3))
x=MX[sel];y=MY[sel];A=np.c_[x*x,x*y,y*y,x,y]; c=np.linalg.lstsq(A,np.ones_like(x),rcond=None)[0]
ce=np.linalg.solve([[2*c[0],c[1]],[c[1],2*c[2]]],[-c[3],-c[4]])
f=lambda X,Y: c@np.array([X*X,X*Y,Y*Y,X,Y])-1; s0=np.sign(f(*ce))
t=(np.arange(6)+.5)/6
OV=np.zeros((64,64),bool)
for Y in range(15,40):
    for X in range(36,56): OV[Y,X]=np.mean([np.sign(f(X+a,Y+b))==s0 for a in t for b in t])>=0.5
for Y,X in np.argwhere(OV):      # losse uitsteekpixel (1 buur) hoort niet bij de bal
    if sum(OV[Y+b,X+a] for a,b in N4)<=1: OV[Y,X]=False

# ---- 1+2. romp: facetten uit het model ----
T=np.zeros((64,64),bool)
for Y in range(19,38):
    for X in range(29,50):
        if OV[Y,X]: continue
        v=n[Y,X]
        if v in (7,8,15) or (v==6 and all(n[Y+b,X+a] in PINK for a,b in N4)): T[Y,X]=True
def vul(F,M):   # spritepixels zonder facet krijgen het facet van de dichtstbijzijnde pixel met facet
    G=F.copy(); G[~M]=-1; todo=[(X,Y) for Y in range(64) for X in range(64) if M[Y,X] and G[Y,X]<0]
    while todo:
        rest=[]
        for X,Y in todo:
            nb=[G[Y+b,X+a] for a,b in N4 if 0<=X+a<64 and 0<=Y+b<64 and M[Y+b,X+a] and G[Y+b,X+a]>=0]
            if nb: G[Y,X]=max(set(nb),key=nb.count)
            else: rest.append((X,Y))
        if len(rest)==len(todo): break
        todo=rest
    return G
def vereenvoudig(G,M,minpx):
    # kleine facetten (< minpx spritepx) gaan op in de buur waarmee ze de langste grens delen; daarna 3x3-meerderheid (2x)
    G=G.copy()
    while True:
        ids,cnt=np.unique(G[M&(G>=0)],return_counts=True)
        if len(ids)==0 or cnt.min()>=minpx: break
        i=ids[cnt.argmin()]; nb={}
        for Y,X in np.argwhere(G==i):
            for a,b in N4:
                j=G[Y+b,X+a]
                if M[Y+b,X+a] and j>=0 and j!=i: nb[j]=nb.get(j,0)+1
        if not nb: G[G==i]=-1; continue
        G[G==i]=max(nb,key=nb.get)
    for _ in range(2):
        H2=G.copy()
        for Y,X in np.argwhere(M):
            v=[G[Y+b,X+a] for a in (-1,0,1) for b in (-1,0,1) if M[Y+b,X+a] and G[Y+b,X+a]>=0]
            if v:
                best=max(set(v),key=v.count)
                if v.count(best)>=5: H2[Y,X]=best
        G=H2
    return G
GR=vereenvoudig(vul(FR,T),T,14)
# basistint per facet: licht linksboven (8), donker rechtsonder (7); kraag onder baard/haar (y<24) 7
ids=[i for i in np.unique(GR[T]) if i>=0]
cen={i:np.argwhere(GR==i).mean(0) for i in ids}     # (y,x)
lr=LUM['romp']
def modlum(i): return float(np.mean([lum[int(round(523-(60-Y-.5)*P)),int(round(512+(X+.5-32)*P))] for Y,X in np.argwhere(GR==i)]))
# licht linksboven: basis 8 als het facet links/boven de diagonaal x+y <= 67 ligt en in het model niet donker is; anders 7
BASIS={i:(8 if (cen[i][1]+cen[i][0]<=67 and modlum(i)>=160) else 7) for i in ids}
# het helderste grote vlak (in het model het lichte bovenvlak midden) krijgt 15 als basis: het lichtste facet
top=max([i for i in ids if (GR==i).sum()>=30],key=modlum); BASIS[top]=15
OP={7:8,8:15,6:7,15:15}; NEER={8:7,7:6,15:8}
def tint_facet(G,M,X,Y,basis,op,neer):
    i=G[Y,X]
    if i not in basis: return None
    b=basis[i]
    licht=any(M[Y+bb,X+aa] and G[Y+bb,X+aa]!=i for aa,bb in ((-1,0),(0,-1)))
    donker=any(M[Y+bb,X+aa] and G[Y+bb,X+aa]!=i for aa,bb in ((1,0),(0,1)))
    if donker: return neer[b]     # schaduwkant van de facetgrens
    if licht: return op[b]        # lichte kant: heldere rand
    return b
for Y in range(64):
    for X in range(64):
        if not T[Y,X]: continue
        v=tint_facet(GR,T,X,Y,BASIS,OP,NEER)
        if v is None: continue
        onder=not T[Y+1,X] and not OV[Y+1,X] and n[Y+1,X] not in PINK
        if onder: v=min(v,7) if v!=6 else 6                       # schaduwsikkel: onderrand 7 (6 alleen als rand)
        zet(X,Y,v,'romp')

# ---- 3. ovaal als eigen bal: rand 6 (linksboven) / 1 (rechtsonder), hooglicht 15 linksboven, 7 rechtsonder ----
cy,cx=ce[1],ce[0]
def ovrand(X,Y): return any(not OV[Y+b,X+a] for a,b in N4)
for Y in range(64):
    for X in range(64):
        if not OV[Y,X]: continue
        dx,dy=X+.5-cx,Y+.5-cy
        if ovrand(X,Y):   # rand 6; zwart alleen rechts waar de bal tegen ijs/achtergrond ligt (niet tegen het lijf)
            buurijs=any((not OV[Y+b,X+a]) and n[Y+b,X+a] not in PINK and n[Y+b,X+a]!=1 for a,b in ((1,0),(1,-1),(1,1)))
            v=1 if (dx>0.5 and buurijs) or n[Y,X]==1 else 6
        else:
            s=(dx*0.75+dy)/3.2            # >0 = rechtsonder
            v=15 if (s<-0.55 and dx<1.0) else (7 if s>0.35 else 8)
        zet(X,Y,v,'schouder')
# rand bovenarm sluit aan op de hand: zwart rechts (zoals Rock af)
if n[32,55]==6: zet(55,32,1,'schouder')

# ---- 4. benen: de r4-dijvlakken (gemeten op de modelribben: rechterdij 4 vlakken met naad 9, linkerdij 2) blijven.
# De automatische facetmeting op de benen (facet_meet.py, facet_been.npy) gaf losse vlekjes en verloor de voetschaduw;
# alleen ter vergelijking bewaard, niet toegepast.
B=np.zeros((64,64),bool)

# ---- netheid: geen tintvlakjes < 3 px in romp en benen (opgaan in de meest voorkomende buurtint van dezelfde zone) ----
def schoon(M,naam):
    for _ in range(6):
        veranderd=False; gezien=np.zeros((64,64),bool)
        for Y,X in np.argwhere(M):
            if gezien[Y,X]: continue
            v=n[Y,X]; stap=[(X,Y)]; cl=[]; gezien[Y,X]=True
            while stap:
                x,y=stap.pop(); cl.append((x,y))
                for a,b in N4:
                    if M[y+b,x+a] and not gezien[y+b,x+a] and n[y+b,x+a]==v: gezien[y+b,x+a]=True; stap.append((x+a,y+b))
            if len(cl)>=3: continue
            nb=[n[y+b,x+a] for x,y in cl for a,b in N4 if M[y+b,x+a] and n[y+b,x+a]!=v]
            if nb:
                w=max(set(nb),key=nb.count)
                for x,y in cl: zet(x,y,w,naam)
                veranderd=True
        if not veranderd: break
schoon(T,'romp'); schoon(B,'benen')
for Y,X in np.argwhere(T):   # schaduwsikkel onder de romp opnieuw afdwingen na het opschonen
    if not T[Y+1,X] and not OV[Y+1,X] and n[Y+1,X] not in PINK and n[Y,X] in (8,15): zet(X,Y,7,'romp')

# ---- uitvoer + log ----
out=Image.fromarray(n.astype('uint8'),'P'); out.putpalette(im.getpalette())
out.save(os.path.join(H,'gnometrotter_ice.png'),transparency=0)
out.resize((512,512),Image.NEAREST).save(os.path.join(H,'gnometrotter_ice_8x.png'),transparency=0)
tel={}; tel3={}
with open(os.path.join(H,'r5_log.txt'),'w') as fh:
    for Y in range(64):
        for X in range(64):
            if n[Y,X]!=o[Y,X]:
                z=zone.get((X,Y),'rest'); tel[z]=tel.get(z,0)+1; fh.write('%s (%d,%d) %X -> %X\n'%(z,X,Y,o[Y,X],n[Y,X]))
print('t.o.v. r4 per zone:',tel,'| silhouet t.o.v. r4:',int(((n>0)!=(o>0)).sum()),'| totaal t.o.v. r3:',int((n!=r3).sum()))
