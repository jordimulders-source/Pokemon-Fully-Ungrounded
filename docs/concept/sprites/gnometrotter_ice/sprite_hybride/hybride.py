# hybride.py: Gnometrotter Ice HYBRIDE. Model ../hybride/model_hybride.png = r3 (zelfde omtrek, muts/baard/haar/neus/riem/stok/zolen
# 100 % r3) met de ijsblokken van r1 in het roze/blauwe lijf. Daarom:
#  - alles buiten het lijf = Ice r2 (../sprite_r2/gnometrotter_ice.png), pixel voor pixel (model is daar gelijk)
#  - silhouet, onderdelen, delen, buitenlijn, ringen en deelgrenzen = Ice r2 (zelfde omtrek, zelfde lijnen in het model)
#  - vlakken van het lijf opnieuw uit het hybride model: per spritepixel de modelhelderheid van het roze/blauw (zonder lijnen)
#    + Gen 3-bol per deel -> 3 tinten; daarna 1 rond meerderheidsfilter binnen het deel zodat de blokken vlakken blijven;
#    blokranden = naden in het hybride model (pixel donkerder dan de lokale mediaan - 22, aandeel >= 0,25, lokaal maximum,
#    doorlopend >= 3 px) in 6 (roze) / 9 (blauw)
import sys, numpy as np; from scipy import ndimage as nd; from PIL import Image
sys.path.insert(0,'../sprite')
from gemeen import *
from reductie_gedeeld import bron
R2='../sprite_r2/'
o=lees(R2+'gnometrotter_ice.png'); r2=o.copy(); zone=np.load(R2+'zone_r2.npy'); DE=np.load(R2+'deel_r2.npy')
a=np.asarray(Image.open('../hybride/model_hybride.png').convert('RGB')).astype(float); L=0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2]
r,g,b=a[...,0],a[...,1],a[...,2]
ROZEM=(r>g)&(r>=b-2)&(L>=80); BLAUWM=(b-r>=12)&(L>=80)
med=nd.median_filter(L,size=13); NAAD=(L<med-22)&(L>=60)
LIJF=np.isin(DE,[2,3,4,5,6,7,8,10,11,12,13,20])
fg=o>0
OUT=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg)):
    if any(not(0<=Y+dy<64 and 0<=X+dx<64) or not fg[Y+dy,X+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): OUT[Y,X]=True
# lijnpixels van r2 in het lijf blijven (buitenlijn, ringen, deelgrenzen); vlak = de rest
def islijn(Y,X):
    if OUT[Y,X] or o[Y,X]==1: return True
    if o[Y,X] in (6,9) and any(DE[Y+dy,X+dx]!=DE[Y,X] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): return True
    if o[Y,X]==6 and DE[Y,X] in (3,5,6,8): return True      # ringen van de ronde delen
    if DE[Y,X]==7 and o[Y,X]==6: return True                  # arm L boven-/onderrij
    return False
VL=np.zeros((64,64),bool)
for Y,X in zip(*np.where(LIJF&fg)): VL[Y,X]=not islijn(Y,X)
G=np.full((64,64),np.nan); NS=np.zeros((64,64))
for Y,X in zip(*np.where(LIJF&fg)):
    M=BLAUWM if DE[Y,X]>=10 else ROZEM; s=n=tw=ns=0
    for u,v,w in bron(X,Y):
        tw+=w; ns+=w*NAAD[v,u]
        if M[v,u] and not NAAD[v,u]: s+=w*L[v,u]; n+=w
    if n: G[Y,X]=s/n
    NS[Y,X]=ns/tw
l3=np.array([-0.55,-0.6,0.58]); l3/=np.linalg.norm(l3)
LOG={}
def zet(Y,X,k,why):
    if o[Y,X]!=k: LOG.setdefault(why,[]).append((int(X),int(Y))); o[Y,X]=k
for i in np.unique(DE[LIJF]):
    m=(DE==i)&VL
    if m.sum()<3: continue
    yy,xx=np.where(DE==i); cx,cy=(xx.min()+xx.max()+1)/2,(yy.min()+yy.max()+1)/2; rx,ry=(np.ptp(xx)+1)/2,(np.ptp(yy)+1)/2
    g=np.where(m,np.nan_to_num(G,nan=np.nanmean(G[m]) if np.isfinite(G[m]).any() else 0),0)
    gz=(g-g[m].mean())/(g[m].std()+1e-9)
    sc=np.zeros((64,64))
    for Y,X in zip(*np.where(m)):
        nx=(X+0.5-cx)/rx; ny=(Y+0.5-cy)/ry; rr=nx*nx+ny*ny
        n=np.array([nx,ny,np.sqrt(max(0.04,1-min(rr,0.96)))]); n/=np.linalg.norm(n)
        sc[Y,X]=0.8*gz[Y,X]+1.6*float(n@l3)
    blauw=i>=10; T=[9,10,11] if blauw else [7,8,15]
    lo,hi=(0.22,0.35) if blauw else (0.30,0.14)
    if m.sum()<12: lo,hi=0.3,0.0
    s=sc[m]; t1=np.quantile(s,lo); t2=np.quantile(s,1-hi) if hi>0 else 1e9
    for Y,X in zip(*np.where(m)): zet(Y,X,T[0] if sc[Y,X]<t1 else T[2] if sc[Y,X]>=t2 else T[1],'blokvlak (model + bol)')
    # blokken vlak houden: meerderheid 3x3 binnen het deel
    o2=o.copy()
    for Y,X in zip(*np.where(m)):
        t=[o[y,x] for y in range(Y-1,Y+2) for x in range(X-1,X+2) if m[y,x]]
        c=np.bincount(t,minlength=16)
        if c.max()>=5 and c[o[Y,X]]<c.max() and o[Y,X]!=15: o2[Y,X]=c.argmax()
    for Y,X in zip(*np.where(m)): zet(Y,X,o2[Y,X],'blokvlak (meerderheid)')
# blokranden uit het hybride model
nm=np.zeros((64,64),bool)
for Y,X in zip(*np.where(VL)):
    c=NS[Y,X]
    if c>=0.25 and ((c>=NS[Y,X-1] and c>=NS[Y,X+1]) or (c>=NS[Y-1,X] and c>=NS[Y+1,X])): nm[Y,X]=True
lb,n=nd.label(nm,structure=np.ones((3,3)))
for j in range(1,n+1):
    mm=lb==j
    if mm.sum()>=3:
        for Y,X in zip(*np.where(mm)): zet(Y,X,9 if DE[Y,X]>=10 else 6,'blokrand (modelnaad)')
# vlekjes < 3 px -> buurtint
for i in np.unique(DE[LIJF]):
    for k in (7,8,10,11):
        lb,n=nd.label((o==k)&(DE==i)&VL,structure=np.ones((3,3)))
        for j in range(1,n+1):
            mm=lb==j
            if mm.sum()>=3: continue
            rr=nd.binary_dilation(mm,structure=np.ones((3,3)))&~mm&(DE==i)&VL; t=o[rr]; t=t[~np.isin(t,[1,6,k])]
            if len(t):
                for Y,X in zip(*np.where(mm)): zet(Y,X,np.bincount(t).argmax(),'ruis')
opslaan(o,'gnometrotter_ice_hybride.png')
print('anders t.o.v. Ice r2:',(o!=r2).sum(),'(alleen lijf: %d buiten het lijf)'%((o!=r2)&~LIJF).sum(),' silhouet:',((o>0)!=(r2>0)).sum())
for k,v in LOG.items(): print('  %-30s %3d'%(k,len(v)))
for i in np.unique(DE[LIJF]): print('  deel',i,'anders',((o!=r2)&(DE==i)).sum(),'/',(DE==i).sum())
