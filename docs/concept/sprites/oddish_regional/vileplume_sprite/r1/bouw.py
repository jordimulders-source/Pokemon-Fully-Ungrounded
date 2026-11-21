# Vileplume (Kelp-/anemoonlijn) r1: model overnemen. Natief raster 5,12 px (128x144) -> 55x62 (S=0,43), x4-58, y1-62.
# Stap 1 kale reductie (r1/kaal.py). Stap 2 = de enige toegestane afwijking (Jordi, optie A): tentakels per anemoon
# klonteren tot N dikke tentakels op de modelplekken/-richting (sectoren uitgelijnd op de modeltentakels, lengte en
# tint per sector gemeten op het model), donkere rand om elke anemoon. Stap 3 technische opschoning, elke stap geteld.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); sys.path.insert(0,'r1')
from klassen import klassen; from gemeen import *; from anemonen import *
from kaal import kaal, PAL
RONDE=sys.argv[1] if len(sys.argv)>1 else 'r1'
N=9                 # klonten per anemoon (Jordi: +-8-10)
RIN_MIN=float(sys.argv[3]) if len(sys.argv)>3 and sys.argv[3][0].isdigit() else 0.35
LENGTE=float(sys.argv[4]) if len(sys.argv)>4 and sys.argv[4][0].isdigit() else 0.45
KERN=0.70           # deel van de sector dat tentakel is (rest = gleuf)
a,c,L=klassen(); H,W=c.shape
RED={2,3,4,5}; WG={6,7,8,9,10}; KR={11,12,13,14,15}
TINT=[5,5,5,5,4]    # tentakeltint per anemoon (gemeten: T heeft 9 px R3, 200 R2 -> R2)
BODY=[{3,4},{3,4},{3,4},{3,4},{3}]
# ---- natieve statistiek per anemoon ----
own=np.full((H,W),-1); D=np.zeros((H,W)); T=np.zeros((H,W))
for v in range(105):
    for u in range(W):
        if c[v,u] in (1,2,3,4,5):
            i=eigenaar(u+.5,v+.5); own[v,u]=i; D[v,u]=afstand(i,u+.5,v+.5); T[v,u]=hoek(i,u+.5,v+.5)
def wrap(x): return (x+np.pi)%(2*np.pi)-np.pi
KLONT=[]   # per anemoon: lijst (hoek, r_in, r_uit)
RDISC=[]   # per anemoon: schijfrand per 10 graden
for i in range(5):
    licht=(own==i)&(c==TINT[i])&(D>0.18)
    for v,u in zip(*np.where(licht)):
        if in_mond(i,u+.5,v+.5,0.5): licht[v,u]=False
    th=T[licht]; dd=D[licht]
    tent_all=(own==i)&np.isin(c,[TINT[i],2])&(D>0.18)
    sec=2*np.pi/N; best=None
    for phi in np.linspace(0,sec,80,endpoint=False):
        rel=np.abs(wrap(th-phi-sec*np.round((th-phi)/sec)))
        sc=(rel<=KERN*sec/2).sum()-(rel>KERN*sec/2).sum()
        if best is None or sc>best[0]: best=(sc,phi)
    phi=best[1]; kl=[]
    for k in range(N):
        c0=wrap(phi+k*sec); m=np.abs(wrap(th-c0))<=sec/2
        if m.sum()<4: continue
        cm=np.angle(np.exp(1j*th[m]).mean())         # massamidden van de modeltentakels in deze sector
        # punt van de klont = waar de modeltentakels in deze sector eindigen (92e percentiel van d over tentakeltint + R0-lijnen);
        # kort: de klont loopt LENGTE (genormaliseerd) terug naar het mondje, niet verder dan RIN_MIN
        mt=tent_all&(np.abs(wrap(T-cm))<=sec/2)
        ru=np.percentile(D[mt],92) if mt.sum()>4 else np.percentile(dd[m],93)
        kl.append((cm,max(RIN_MIN,ru-LENGTE),ru,int(m.sum())))
    KLONT.append(kl)
    body=(own==i)&np.isin(c,list(BODY[i]))
    rd=[]
    for b in range(36):
        t0=-np.pi+b*np.pi/18; m=body&(T>=t0)&(T<t0+np.pi/18)
        rd.append(np.percentile(D[m],92) if m.sum()>3 else 0.0)
    RDISC.append(rd)
# lichaamstint-kaart: elke rode natieve pixel krijgt de tint van de dichtstbijzijnde lichaamspixel van dezelfde anemoon
from collections import deque
BT=np.zeros((H,W),int); q=deque()
for v,u in zip(*np.where(own>=0)):
    if c[v,u] in BODY[own[v,u]]: BT[v,u]=c[v,u]; q.append((v,u))
while q:
    v,u=q.popleft()
    for dv,du in ((1,0),(-1,0),(0,1),(0,-1)):
        vv,uu=v+dv,u+du
        if 0<=vv<H and 0<=uu<W and own[vv,uu]==own[v,u] and BT[vv,uu]==0: BT[vv,uu]=BT[v,u]; q.append((vv,uu))
def lichaamstint(i,X,Y,R=2.0):
    # gladde lichaamstint: aandeel schaduwtint (R1) onder de lichaamspixels van deze anemoon binnen R spritepx
    if len(BODY[i])==1: return min(BODY[i])
    if '--licht' not in sys.argv: return 3      # lijf tussen de klonten in de schaduwtint (kleur mag afwijken: contrast met de tentakels)
    uc,vc=ctr(X,Y); r=R/S; n1=n2=0
    for v in range(int(vc-r),int(vc+r)+1):
        for u in range(int(uc-r),int(uc+r)+1):
            if 0<=v<H and 0<=u<W and own[v,u]==i and (u+.5-uc)**2+(v+.5-vc)**2<=r*r:
                if c[v,u]==3: n1+=1
                elif c[v,u]==4: n2+=1
    return 3 if n1>n2 else 4
def ctr(X,Y): return U0+(X+0.5-X0)/S, V0+(Y+0.5-Y0)/S
def rdisc(i,t): return RDISC[i][int((t+np.pi)//(np.pi/18))%36]
# ---- 1. kale reductie ----
o,F=kaal(); kaal_o=o.copy()
kr_ell=lambda u,v: ((u-100.0)/18.5)**2+((v-57.5)/10.5)**2<=1
# ---- 2. klonteren ----
# klont = dikke tentakel: lijnstuk van r_in naar r_uit langs de modelrichting (massamidden van de modeltentakels in de
# sector), breedte BREED spritepx met ronde punt; elke pixel hoort bij de dichtstbijzijnde klont (KLID).
BREED=float(sys.argv[2]) if len(sys.argv)>2 and sys.argv[2][0].isdigit() else 2.4
EENZIJDIG='--rond' not in sys.argv
def punt(i,t,d):
    n,cx,cy,l,r,b,ov,f=AN[i]; ct,st=np.cos(t),np.sin(t)
    return cx+d*ct*(l if ct<0 else r), cy+d*st*(b if st<0 else ov)
SEG=[]   # (anemoon, klontnr, p0, p1)
for i in range(5):
    for k,(cm,ri,ru,n) in enumerate(KLONT[i]):
        SEG.append((i,k,punt(i,cm,max(ri,RIN_MIN)),punt(i,cm,ru)))
def segafst(p,a0,a1):
    p=np.array(p); a0=np.array(a0); a1=np.array(a1); v=a1-a0; t=np.clip(np.dot(p-a0,v)/max(np.dot(v,v),1e-9),0,1)
    return np.linalg.norm(p-(a0+t*v))
OWN=np.full((64,64),-1); KL=np.zeros((64,64),bool); KLID=np.full((64,64),-1); MOND=np.zeros((64,64),bool)
for Y in range(1,40):
    for X in range(1,63):
        k=o[Y,X]
        if k in WG or k in KR: continue
        if k==1 and F[Y,X,2:6].sum()<0.15: continue      # zwarte lijn zonder anemoonrood (lijf/arm) blijft kaal
        uc,vc=ctr(X,Y)
        if kr_ell(uc,vc) and k!=0: continue
        i=eigenaar(uc,vc); d=afstand(i,uc,vc)
        if d>1.6: continue
        best=None
        for j,(ii,kk,p0,p1) in enumerate(SEG):
            if ii!=i: continue
            e=segafst((uc,vc),p0,p1)*S        # in spritepixels
            if e<=BREED/2 and (best is None or e<best[0]): best=(e,j)
        if best:
            o[Y,X]=TINT[i]; OWN[Y,X]=i; KL[Y,X]=True; KLID[Y,X]=best[1]
        elif k!=0:
            if F[Y,X,0]>=0.2 and d>0.8: o[Y,X]=0      # tussen de dunne punten (deels achtergrond in het model) -> achtergrond
            else:
                o[Y,X]=lichaamstint(i,X,Y); OWN[Y,X]=i
# mondjes: ovaal (ring R0, binnen R2) precies op de bbox van de modelring; zoals een oog een benoemde reparatie,
# want de 2,3x-verkleining maakt van ring+binnenkant een streepje
for i,(x0,x1,y0,y1) in enumerate(MONDBOX):
    for Y in range(y0,y1+1):
        for X in range(x0,x1+1):
            hoek_=(Y in (y0,y1)) and (X in (x0,x1))
            if hoek_: continue
            rand_=(Y in (y0,y1)) or (X in (x0,x1))
            o[Y,X]=2 if rand_ else 4; OWN[Y,X]=i; MOND[Y,X]=True; KL[Y,X]=False; KLID[Y,X]=-1
print('klonteren + mondjes: %d px anders dan kaal'%(o!=kaal_o).sum())
# klontpunten die aan de achtergrond grenzen krijgen hun lijn BUITEN de klont (op de achtergrondpixel), zodat de punt dik blijft
for Y,X in zip(*np.where(KL)):
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        if 1<=Y+dy<=62 and 1<=X+dx<=62 and o[Y+dy,X+dx]==0 and OWN[Y+dy,X+dx]<0:
            o[Y+dy,X+dx]=2; OWN[Y+dy,X+dx]=OWN[Y,X]
stap=o.copy()
# klontrand: lichaamspixel naast een klont van dezelfde anemoon -> donkerrood (R0);
# twee klonten die elkaar raken: de klontpixel die verder van zijn eigen lijnstuk ligt wordt R0 (scheiding)
ZIJDEN=((-1,0),(0,-1)) if EENZIJDIG else ((1,0),(-1,0),(0,1),(0,-1))
for Y,X in zip(*np.where((OWN>=0)&~KL&~MOND&(o>0))):
    for dy,dx in ZIJDEN:      # eenzijdig: alleen lichaamspixels rechts/onder een klont (schaduwkant) worden R0
        if KL[Y+dy,X+dx] and OWN[Y+dy,X+dx]==OWN[Y,X]: o[Y,X]=2; break
for Y,X in zip(*np.where(KL)):
    for dy,dx in ((1,0),(0,1)):
        j=KLID[Y+dy,X+dx]
        if j>=0 and j!=KLID[Y,X] and OWN[Y+dy,X+dx]==OWN[Y,X]:
            e1=segafst(ctr(X,Y),*SEG[KLID[Y,X]][2:]); e2=segafst(ctr(X+dx,Y+dy),*SEG[j][2:])
            if e1>=e2: o[Y,X]=2
            else: o[Y+dy,X+dx]=2
# anemoonrand: pixel van een verder-achter-anemoon naast een voorste -> zwart
for Y,X in zip(*np.where(OWN>=0)):
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        if not(0<=Y+dy<64 and 0<=X+dx<64): continue
        j=OWN[Y+dy,X+dx]
        if j>=0 and j<OWN[Y,X] and o[Y+dy,X+dx]>0 and o[Y,X]>0: o[Y,X]=1; break
print('randen klonten/anemonen: %d px'%(o!=stap).sum())
stap2=o.copy()
# dunne lijnen in poten/lijf: een lijnpixel (W0 of zwart) met links en rechts lijf/poot is een gemiddelde van twee
# modellijnen met vulling ertussen; onder 50 % lijndekking wint de meest voorkomende vultint uit het model
for Y in range(30,63):
    for X in range(1,63):
        if o[Y,X] in (1,6) and o[Y,X-1] in WG|{1} and o[Y,X+1] in WG|{1} and o[Y,X-1]>0 and o[Y,X+1]>0:
            f=F[Y,X]
            if f[o[Y,X]]<0.5 and f[7:11].sum()>0:
                o[Y,X]=7+int(np.argmax(f[7:11]))
print('lijn midden in poot/lijf -> vultint: %d px'%(o!=stap2).sum())
# poten: model is 6 natieve px = 2,6 spritepx (lijn-vulling-lijn); de reductie wisselt 2 en 3 px, en 2 px = twee lijnen
# zonder vulling. Elke potenrij wordt 3 px: de ontbrekende pixel komt aan de kant met de meeste modeldekking; patroon
# lijn (W0) - vulling (meest voorkomende vultint in het model) - zwart, zoals het model (lichte lijn links, zwart rechts).
pt=o.copy()
for Y in range(42,62):
    for xa,xb in ((20,31),(31,46)):
        xs=[X for X in range(xa,xb) if o[Y,X]>0]
        if not xs or xs[-1]-xs[0]+1!=len(xs) or len(xs)>3: continue
        if len(xs)==2:
            l,r=xs[0]-1,xs[-1]+1
            xs=[l]+xs if F[Y,l,0]<=F[Y,r,0] else xs+[r]
        if len(xs)!=3: continue
        f=F[Y,xs[1]]; vul=7+int(np.argmax(f[7:11])) if f[7:11].sum()>0 else 9
        o[Y,xs[0]],o[Y,xs[1]],o[Y,xs[2]]=6,vul,1
print('poten 3 px: %d px'%(o!=pt).sum())
stap2=o.copy()
# ---- 3. buitenlijn ----
def rand(o):
    fg=o>0; uit=[]
    for Y,X in zip(*np.where(fg)):
        if o[Y,X]==1: continue
        bL=not fg[Y,X-1]; bR=not fg[Y,X+1]; bU=not fg[Y-1,X]; bD=not fg[Y+1,X]
        if not(bL or bR or bU or bD): continue
        sch=bR or (bD and not bL)      # schaduwkant rechts/onder; een linkerrand blijft selout (geen zwart/selout om en om)
        if o[Y,X] in RED: uit.append((Y,X,1 if sch else 2))
        elif o[Y,X] in WG: uit.append((Y,X,1 if sch else 6))
    for Y,X,k in uit: o[Y,X]=k
rand(o); print('buitenlijn: %d px'%(o!=stap2).sum())
# ---- 4. losse pixels: een pixel zonder gelijke 8-buur (buiten mondjes en krater) neemt de meest voorkomende
# 4-buurkleur aan (niet-achtergrond); op de buitenrand blijft de lijnkleur (zwart/selout) staan ----
stap3=o.copy()
for ronde in range(3):
    P=np.pad(o,1)
    for Y,X in zip(*np.where(o>0)):
        k=o[Y,X]
        if MOND[Y,X] or k in KR: continue
        n8=[P[Y+1+dy,X+1+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
        if k in n8: continue
        n4=[P[Y+1+dy,X+1+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
        if 0 in n4 and k in (1,2,6): continue
        kand=[v for v in n4 if v>0 and v not in KR]
        if kand: o[Y,X]=max(set(kand),key=kand.count)
print('losse pixels: %d px'%(o!=stap3).sum())
opslaan(o,PAL,RONDE+'/vileplume_'+RONDE+'.png')
ch='.K0123abcdeGuomy'
print('   '+''.join(str(x%10) for x in range(64)))
for y in range(64): print('%2d '%y+''.join(ch[v] for v in o[y]))
print('totaal anders dan kaal: %d px, kleuren %d'%((o!=kaal_o).sum(),len(set(o.ravel()))))
if '--diag' in sys.argv:
    for i in range(5):
        print(AN[i][0],[(round(np.degrees(cm)),round(ri,2),round(ru,2),n) for cm,ri,ru,n in KLONT[i]])
        print('  rdisc',[round(x,2) for x in RDISC[i]])
    from PIL import Image
    img=np.full((64,64,3),255,'uint8'); kl=[(255,0,0),(0,0,255),(0,170,0),(0,170,170),(200,0,200)]
    for Y,X in zip(*np.where(OWN>=0)):
        col=np.array(kl[OWN[Y,X]]); img[Y,X]=(col*(0.55+0.45*(KLID[Y,X]%2))).astype(int) if KL[Y,X] else (col*0.35+255*0.65).astype(int)
        if MOND[Y,X]: img[Y,X]=(0,0,0)
    Image.fromarray(img).resize((512,512),Image.NEAREST).save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/fabbb773-9d3c-5783-a635-6cbf1e7c7be6/scratchpad/diag.png')
# ---- telling per zone: pixels die afwijken van de kale reductie ----
zk=np.zeros((64,64),bool)
for Y in range(64):
    for X in range(64):
        if kaal_o[Y,X] in KR or o[Y,X] in KR or (OWN[Y,X]<0 and kr_ell(*ctr(X,Y))): zk[Y,X]=True
diff=o!=kaal_o
zones={'krater':zk,'anemonen':(~zk)&(np.arange(64)[:,None]<=31)&((OWN>=0)|np.isin(kaal_o,[1,2,3,4,5])|np.isin(o,[1,2,3,4,5])),
       'mondjes':MOND}
zones['lijf+armen']=(~zk)&~zones['anemonen']&(np.arange(64)[:,None]<=41)
zones['poten']=(np.arange(64)[:,None]>=42)
for n,m in zones.items(): print('zone %-10s afwijking van kaal: %d px'%(n,(diff&m).sum()))
