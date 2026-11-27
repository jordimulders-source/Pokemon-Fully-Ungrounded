# Ronde 3: vanaf r2. (1) losse zwarte pixels -> modus van de modelcellen; (2) lijnen rond het oog minder donker.
import numpy as np
from basis import png,PAL
from modus import modus
I=np.load('r2_I.npy').copy(); I0=I.copy(); nat=np.load('comp_nat.npy')
op=I>0; P=np.pad(op,1)
buiten=(I==1)&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
DONK=(I==1)|(I==10)   # zwart en de donkerste grijstint (op 8x allebei zwart)
binnen=DONK&~buiten
# losse donkere pixels: geïsoleerd, of een uitsteeksel van <=2 px dat niet aan de buitenlijn vastzit
def buren(y,x):
    return [(y+dy,x+dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=y+dy<64 and 0<=x+dx<64 and DONK[y+dy,x+dx]]
los=set()
for y,x in zip(*np.where(binnen)):
    nb=buren(y,x)
    if len(nb)==0: los.add((y,x)); continue
    if len(nb)!=1: continue
    keten=[(y,x)]; vorige=(y,x); cur=nb[0]; ok=False
    while True:
        if buiten[cur]: ok=True; break             # vast aan de buitenlijn: houden
        nb2=[q for q in buren(*cur) if q not in keten]
        if len(buren(*cur))>=3 or len(nb2)!=1:   # knooppunt of einde
            if len(buren(*cur))<3: keten.append(cur)   # eind van een los stukje
            break
        keten.append(cur); cur=nb2[0]
        if len(keten)>2: ok=True; break           # doorlopende lijn >=3
    if not ok and len(keten)<=2: los.update(keten)
# bultjes: donkere binnenpixel waarvan alle donkere buren aan één kant liggen en samen al een lijn vormen
#  (2-3 buren, onderling verbonden, geen enkele buur aan de buitenlijn) -> geen eigen lijn, maar een uitsteeksel
bult=set()
for y,x in zip(*np.where(binnen)):
    nb=buren(y,x)
    if not (2<=len(nb)<=3): continue
    if any(buiten[q] for q in nb): continue
    dys={q[0]-y for q in nb}; dxs={q[1]-x for q in nb}
    eenkant= dys=={-1} or dys=={1} or dxs=={-1} or dxs=={1}
    if not eenkant: continue
    # buren moeten onderling verbonden zijn (lijn langs P), en P moet niet een hoek in een lijn zijn
    if len(nb)==2 and max(abs(nb[0][0]-nb[1][0]),abs(nb[0][1]-nb[1][1]))>1: continue
    bult.add((y,x))
los=sorted(set(los)|bult)
n=len(los)
TONEN={'g':None}
def kleur(y,x):
    w=modus(x,y,nat); w.pop('.',None); w.pop('#',None)
    if not w: return None
    k=max(w,key=w.get)
    if k=='g':  # grijs: tint per helderheid uit de grijze cellen
        from reduceer import X0,Y0,s,LEFT,TOP
        ya=Y0+(y-TOP)*s; xa=X0+(x-LEFT)*s
        cs=[nat[yy,xx] for yy in range(int(ya),int(np.ceil(ya+s))) for xx in range(int(xa),int(np.ceil(xa+s))) if 0<=yy<100 and 0<=xx<100 and nat[yy,xx].mean()>=45 and abs(int(nat[yy,xx][0])-int(nat[yy,xx][2]))<16]
        c=np.median(np.array(cs),0)
        return [10,11,12,13][int(np.argmin([((np.array(PAL[i])-c)**2).sum() for i in (10,11,12,13)]))]
    return int(k)
opg=[]; gehouden=[]
for y,x in los:
    v=kleur(y,x)
    if v is None: gehouden.append((x,y)); continue
    I[y,x]=v; opg.append((x,y,v))
print('los:',sorted((x,y,int(I0[y,x])) for y,x in los)); print('binnen-zwart',binnen.sum(),'componenten',n,'opgeruimd',len(opg),'geen modelkleur (blijft zwart)',gehouden)
np.save('r3_opg.npy',np.array([(x,y) for x,y,v in opg]))
