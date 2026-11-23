# Technisch opschonen van een kale reductie (geen vormwijziging): buitenlijn, losse tintjes. Elke wijziging wordt geteld per stap.
import numpy as np
from gemeen import label
__all__=['streep_binnen','buitenlijn','ontkorrel','losse_zwart','buren','N4','GROEP','KL_K']
KL_K=1
K,D,E,G,y,Y,L,B,W=1,2,3,4,5,6,7,8,9
GROEP={D:'vacht',E:'vacht',G:'vacht',y:'geel',Y:'geel',L:'geel',B:'wit',W:'wit'}
N4=[(-1,0),(1,0),(0,-1),(0,1)]
def buren(o,y_,x_,nb=N4):
    for dy,dx in nb:
        yy,xx=y_+dy,x_+dx
        yield (o[yy,xx] if 0<=yy<o.shape[0] and 0<=xx<o.shape[1] else 0),dy,dx
def normalen(o,r=2):
    # buitenwaartse normaal per pixel uit het geblurde silhouet (box (2r+1)^2), zodat een rechte schuine rand één richting heeft
    a=(o>0).astype(float); p=np.pad(a,r+1)
    b=np.zeros_like(p)
    for dy in range(-r,r+1):
        for dx in range(-r,r+1): b+=np.roll(np.roll(p,dy,0),dx,1)
    gy,gx=np.gradient(b); gy=gy[r+1:-r-1,r+1:-r-1]; gx=gx[r+1:-r-1,r+1:-r-1]
    n=np.hypot(gx,gy)+1e-9
    return -gx/n,-gy/n
def buitenlijn(o,beschermd=None,drempel=0.3):
    # rand = pixel met transparante 4-buur. Lichtkant = buitenwaartse normaal wijst naar linksboven (dot met (-1,-1)/sqrt2 >= drempel):
    # selout (vacht D, geel y, wit B; ook modelzwart -> D, Emolga: oorrand 32/32/40 linksboven). Anders schaduwkant -> zwart.
    nx,ny=normalen(o)
    n=o.copy(); log=[]
    for y_,x_ in zip(*np.where(o>0)):
        if beschermd is not None and beschermd[y_,x_]: continue
        if not any(v==0 for v,_,_ in buren(o,y_,x_)): continue
        v=o[y_,x_]
        rechts=(x_+1>=o.shape[1]) or o[y_,x_+1]==0
        licht=(-nx[y_,x_]-ny[y_,x_])/np.sqrt(2)>=drempel and not rechts
        nv={K:D,G:D,E:E,D:D,L:y,Y:y,y:y,W:B,B:B}[v] if licht else K
        if nv!=v: n[y_,x_]=nv; log.append((x_,y_,v,nv))
    # niet om en om: een randpixel D/K waarvan alle rand-buren (8) de andere waarde hebben, neemt die over
    rand=np.zeros(o.shape,bool)
    for y_,x_ in zip(*np.where(n>0)):
        rand[y_,x_]=any(v==0 for v,_,_ in buren(n,y_,x_))
    m=n.copy()
    for y_,x_ in zip(*np.where(rand&np.isin(n,(D,K)))):
        if beschermd is not None and beschermd[y_,x_]: continue
        nb=[n[y_+dy,x_+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=y_+dy<64 and 0<=x_+dx<64 and rand[y_+dy,x_+dx]]
        nb=[v for v in nb if v in (D,K)]
        if len(nb)>=2 and all(v==nb[0] for v in nb) and nb[0]!=n[y_,x_]:
            log.append((x_,y_,n[y_,x_],nb[0])); m[y_,x_]=nb[0]
    return m,log
def ontkorrel(o,beschermd=None,minp=3):
    # tintvlakjes < minp px (8-samenhang) binnen een kleurgroep nemen de meest voorkomende buurtint van dezelfde groep aan.
    n=o.copy(); log=[]
    for v in (D,E,G,y,Y,L,B,W):
        lab,k=label(n==v)
        for i in range(1,k+1):
            m=lab==i
            if m.sum()>=minp: continue
            pts=list(zip(*np.where(m)))
            if beschermd is not None and any(beschermd[p] for p in pts): continue
            tel={}
            for (y_,x_) in pts:
                for dy in (-1,0,1):
                    for dx in (-1,0,1):
                        yy,xx=y_+dy,x_+dx
                        if 0<=yy<64 and 0<=xx<64 and not m[yy,xx]:
                            w=n[yy,xx]
                            if GROEP.get(w)==GROEP[v]: tel[w]=tel.get(w,0)+1
            if tel:
                nv=max(tel,key=tel.get)
                for p in pts: n[p]=nv; log.append((p[1],p[0],v,nv))
    return n,log
def losse_zwart(o,beschermd=None):
    # zwarte pixel zonder zwarte 8-buur en zonder transparante buur = los (hatun runa-les)
    res=[]
    for y_,x_ in zip(*np.where(o==K)):
        if beschermd is not None and beschermd[y_,x_]: continue
        nb=o[max(0,y_-1):y_+2,max(0,x_-1):x_+2]
        if (nb==K).sum()==1 and not (nb==0).any(): res.append((x_,y_))
    return res

def streep_binnen(o,log_buitenlijn):
    # Lichte vachtstreep (G) die op de buitenrand lag en selout (D) werd: 1 px naar binnen terugzetten op een D-pixel,
    # zodat de modelopbouw omlijning | lichte streep | vacht blijft (model: K G D aan de vleugel- en oorrand).
    n=o.copy(); log=[]
    for x_,y_,v,nv in log_buitenlijn:
        if not (v==G and nv==D): continue
        bg=[(dy,dx) for w,dy,dx in buren(o,y_,x_) if w==0]
        for dy,dx in bg:
            yy,xx=y_-dy,x_-dx
            if 0<=yy<64 and 0<=xx<64 and n[yy,xx]==D: n[yy,xx]=G; log.append((xx,yy,D,G)); break
    return n,log
