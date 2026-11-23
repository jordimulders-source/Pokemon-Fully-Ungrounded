# bouw2.py: automatische technische opschoning op a0_pre.png -> ../A0.png
# (1) buitenlijn: randpixel (4-buur transparant): schaduwkant -> K; lichtkant (normaal naar linksboven) -> selout van het vlak
#     (donker -> D, geel -> y, wit -> w, masker -> M). Lichte pixels (wit/masker) op de rand van het lijf (rij < 38) zijn
#     randmengsels van zwarte lijn en achtergrond -> als donker behandeld. Beschermde pixels (ogen, lijnen) blijven.
# (2) niet om en om: randpixel D/K met alleen de andere waarde als randburen neemt die over.
# (3) ontkorrel: tintvlakjes < 3 px (8-samenhang) binnen een kleurgroep -> meest voorkomende buurtint van die groep.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/sprite_r1/gereedschap')
from fv import *; import palet, pickle
K,Dk,E,Gl,y,Y,L,B,W,w,M,N,O=range(1,14)
GROEP={Dk:'d',E:'d',Gl:'d',y:'g',Y:'g',L:'g',B:'w',W:'w',w:'w',M:'m',N:'m',O:'m'}
def normalen(o,r=2):
    a=(o>0).astype(float); p=np.pad(a,r+1); b=np.zeros_like(p)
    for dy in range(-r,r+1):
        for dx in range(-r,r+1): b+=np.roll(np.roll(p,dy,0),dx,1)
    gy,gx=np.gradient(b); gy=gy[r+1:-r-1,r+1:-r-1]; gx=gx[r+1:-r-1,r+1:-r-1]
    n=np.hypot(gx,gy)+1e-9; return -gx/n,-gy/n
def rand(o,y_,x_):
    return any((not(0<=y_+dy<64 and 0<=x_+dx<64)) or o[y_+dy,x_+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))
def buitenlijn(o,besch,log):
    nx,ny=normalen(o); n=o.copy()
    for y_,x_ in zip(*np.where(o>0)):
        if besch[y_,x_] or not rand(o,y_,x_): continue
        v=o[y_,x_]
        licht=(-nx[y_,x_]-ny[y_,x_])/np.sqrt(2)>=0.3 and x_+1<64 and o[y_,x_+1]!=0
        if y_<38 and v in (B,W,w,M,N,O): v=Dk                       # randmengsel op het lijf
        if licht: nv={K:Dk,Dk:Dk,E:E,Gl:E,y:y,Y:y,L:y,B:w,W:w,w:w,M:M,N:M,O:M}[v]
        else: nv=K
        if nv!=o[y_,x_]: n[y_,x_]=nv; log.append(('rand',x_,y_,palet.CH[o[y_,x_]],palet.CH[nv],'buitenlijn '+('licht' if licht else 'schaduw')))
    m=n.copy()
    R=np.zeros(n.shape,bool)
    for y_,x_ in zip(*np.where(n>0)): R[y_,x_]=rand(n,y_,x_)
    for y_,x_ in zip(*np.where(R&np.isin(n,(Dk,K)))):
        if besch[y_,x_]: continue
        nb=[n[y_+dy,x_+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=y_+dy<64 and 0<=x_+dx<64 and R[y_+dy,x_+dx]]
        nb=[v for v in nb if v in (Dk,K)]
        if len(nb)>=2 and all(v==nb[0] for v in nb) and nb[0]!=n[y_,x_]:
            log.append(('rand',x_,y_,palet.CH[n[y_,x_]],palet.CH[nb[0]],'niet om en om')); m[y_,x_]=nb[0]
    return m
def ontkorrel(o,besch,log,minp=3):
    n=o.copy()
    for v in GROEP:
        lab,k=label(n==v)
        for i in range(1,k+1):
            msk=lab==i
            if msk.sum()>=minp: continue
            pts=list(zip(*np.where(msk)))
            if any(besch[p] for p in pts): continue
            tel={}
            for (y_,x_) in pts:
                for dy in (-1,0,1):
                    for dx in (-1,0,1):
                        yy,xx=y_+dy,x_+dx
                        if 0<=yy<64 and 0<=xx<64 and not msk[yy,xx] and GROEP.get(n[yy,xx])==GROEP[v]: tel[n[yy,xx]]=tel.get(n[yy,xx],0)+1
            if tel:
                nv=max(tel,key=tel.get)
                for p in pts: log.append(('korrel',p[1],p[0],palet.CH[v],palet.CH[nv],'tintvlakje < 3 px')); n[p]=nv
    return n
def opschoon(o,besch):
    log=[]
    o=buitenlijn(o,besch,log); o=ontkorrel(o,besch,log)
    return o,log
if __name__=='__main__':
    o=np.asarray(Image.open(D+'sprite_r1/tussen/a0_pre.png')).astype(int)
    besch=np.load(D+'sprite_r1/tussen/beschermd.npy')
    o,log=opschoon(o,besch)
    # losse zwarte stipjes midden in donker (lijnresten < 1 px in het model) -> D; tintresten naar modelmediaan
    for p in [(31,11),(40,21),(24,27),(26,32),(33,35),(24,36),(35,39),(21,54)]:
        log.append(('korrel',p[0],p[1],palet.CH[o[p[1],p[0]]],'D','los zwart stipje in donker vlak')); o[p[1],p[0]]=Dk
    for p,v,r in [((28,14),Dk,'model mediaan 29'),((34,40),B,'model mediaan 222'),((24,37),B,'model mediaan 159, wit vlak')]:
        log.append(('korrel',p[0],p[1],palet.CH[o[p[1],p[0]]],palet.CH[v],r)); o[p[1],p[0]]=v
    palet.opslaan(o,D+'sprite_r1/A0.png'); pickle.dump(log,open(D+'sprite_r1/tussen/log2.pkl','wb'))
    from collections import Counter; print(Counter(l[0] for l in log),'kleuren',sorted(set(o.ravel().tolist())))
