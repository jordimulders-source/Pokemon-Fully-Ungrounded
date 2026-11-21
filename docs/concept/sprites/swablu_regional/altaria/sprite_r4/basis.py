# basis.py: r1-reductie (zelfde regels als sprite_r1/bouw.py) op het kop x1,5-dy10-model (model_kop/natief_kop15_dy10.png; Jordi: linkeroog moet zichtbaar zijn).
# Levert het silhouet, de static-plekken en de kuiftinten waarop r3 voortbouwt -> sprite_r4/basis_kop15.png.
# Het model is bovenaan 3 natieve rijen gepad (kuif reikt nu tot rij 0); blokuitlijning blijft gelijk (V0 14 -> 17).
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen, statisch
import gemeen as G; from gemeen import label, opslaan, toon, WOLK, VIOLET
NAT='model_kop/natief_kop15_dy10.png'; KOP=(50,75,60,106); KUIF=(48,70); PAD=3
a,c,L=klassen(NAT,KOP=KOP,KUIF=KUIF)
c[(c==5)&(a.min(2)>=225)]=0     # bijna-wit naast de vergrote kop (halo van het plakken, in het model wit) = achtergrond, geen kuiflicht
st=statisch(a,c,L,KOP=KOP)
pad=lambda z,v: np.concatenate([np.full((PAD,)+z.shape[1:],v,z.dtype),z])
a=pad(a,255); c=pad(c,0); L=pad(L,255.); st=pad(st,False)
U0,V0,X0,Y0=G.U0,G.V0+PAD,G.X0,G.Y0
def blok(X,Y): return U0+3*(X-X0), V0+3*(Y-Y0)
def kuif(X,Y): return (Y<=13 and X>=19) or (Y<=21 and 34<=X<=51)
P=np.array(G.PAL,float)
q=np.zeros(c.shape,int)
for cl,grp in ((1,[1]),(2,[2,3,4,5]),(3,[6,7,8]),(4,[10]),(5,[9])):
    m=c==cl
    if m.any(): d=((a[m][:,None,:]-P[grp][None])**2).sum(2); q[m]=np.array(grp)[d.argmin(1)]
q[st]=10; q[(c==4)&~st]=5
def kies(Y,X):
    u,v=blok(X,Y); b=q[v:v+3,u:u+3].ravel(); n=lambda k:(b==k).sum(); fig=(b>0).sum()
    w=sum(n(k) for k in WOLK); vi=sum(n(k) for k in (6,7,8,9))
    if kuif(X,Y) and vi+n(1)>=w:                 # kuif (niet waar de wolk overheerst: de kuifpunt rechts ligt nu tegen de vleugel)
        if n(10)>=2 and vi<3: return 10
        if fig<5: return 0
        if n(1)>=4: return 1
        t={6:n(6)+n(2)+n(3),7:n(7)+n(4),8:n(8)+n(9)+n(5)}; m=max(t.values())
        return [k for k in (8,7,6) if t[k]==m][0]
    if n(10)>=2: return 10
    if fig<5: return 0
    if n(1)>=3: return 1
    if n(9)>=2: return 9
    w=sum(n(k) for k in WOLK); vi=sum(n(k) for k in VIOLET)
    if max(w,vi)==0: return 1
    grp=WOLK if w>=vi else VIOLET
    gem=a[v:v+3,u:u+3].reshape(-1,3)[np.isin(b,list(grp))].mean(0)
    return min(sorted(grp),key=lambda k:((P[k]-gem)**2).sum())
o=np.zeros((64,64),int)
for Y in range(64):
    for X in range(64):
        u,v=blok(X,Y)
        if 0<=u<a.shape[1]-2 and 0<=v<a.shape[0]-2: o[Y,X]=kies(Y,X)
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def meest(l): return max(set(l),key=l.count)
lab,n=label(o==10,acht=True)                                   # static-stukjes van 1-2 px weg (zoals r1)
for i in range(1,n+1):
    m=lab==i
    if m.sum()>=3: continue
    for Y,X in zip(*np.where(m)):
        nb=[o[Y+dy,X+dx] for dy,dx in N4 if o[Y+dy,X+dx]!=10]; o[Y,X]=meest(nb) if nb else 0
lab,n=label(o>0,acht=True)                                     # losse figuurpixels (geen 8-buur) weg
for i in range(1,n+1):
    if (lab==i).sum()==1: o[lab==i]=0
opslaan(o,'sprite_r4/basis_kop15.png')
if __name__=='__main__':
    yy,xx=np.where(o>0); print('bbox x%d-%d y%d-%d, %d px'%(xx.min(),xx.max(),yy.min(),yy.max(),(o>0).sum())); toon(o,2,30,14,56)
