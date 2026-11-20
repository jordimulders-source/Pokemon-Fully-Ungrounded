# Vileplume (Kelp-/anemoonlijn) r8 = r7 + Jordi over r7:
#  "De voorste twee anemonen zijn nu veel te simpel" -> VL/VR zelfde opbouw als de achterste 3: vingers (±2 px,
#     licht met schaduwkant, donkere scheiding waar ze raken) in de gemeten modelrichtingen (r8/meet.py), van het
#     mondje tot de rand; boven steken ze uit tot de modelpunt (kroon boven lager, zoals L/R/T).
#  "de cirkel in het midden is wat slordig" (= alle mondjes) -> één vast stempel voor alle vijf (ovaaltje 6x3,
#     ring R0, binnen licht) met een lichte rand van 1 px eromheen, op de modelplek.
#  "Het gezicht is nog steeds niet zichtbaar" -> gelaatvarianten (ogen 2x2/2x3, met/zonder glans, met/zonder mondje).
#  "de poot misschien toch maar het model na maken met de knik erin" -> linkerpoot rij voor rij uit het model.
#  Krater, achterste anemonen (op de mondjes na), lijf, armen en rechterpoot: als r7.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); sys.path.insert(0,'r1')
from PIL import Image
from klassen import klassen; from gemeen import *; from anemonen import *
from kaal import kaal, PAL
RONDE=sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('-') else 'r8'
def opt(n,d):
    for x in sys.argv:
        if x.startswith('--'+n+'='): return float(x.split('=')[1])
    return d
UIT=opt('uit',3.0)             # max. lengte (px) waarmee een punt buiten de kroonrand uitsteekt
LIJN=int(opt('lijn',0))        # 1 = donkere lijn aan de schaduwkant van elke tentakel
LIJNK=int(opt('lijnk',2))      # paletindex van die lijn (2 = R0, 3 = R1)
BASISK=int(opt('basis',4))     # kroontint van de vier grote anemonen (4 = R2, 3 = R1)
START=opt('start',0.9)         # afstand (px) tussen mondring en tentakelbegin (modus straal)
MODUS='straal' if '--straal' in sys.argv else 'wig'
HALF=opt('half',0.55); SIKKEL=opt('sikkel',0.75); SCHADUWK=4; BUITEN=opt('buiten',1.1); VR_=opt('vinger',0.95); BOL=opt('bol',0.1); HUB=opt('hub',1.6); PUNTBREED=int(opt('puntbreed',1)); WRIN=opt('wrin',0.0); WLIJN=opt('wlijn',0)
# MODUS wig (standaard): kroon in wiggen; HALF = deel van elke sector dat tentakel is; HUB = lichte ring (px) rond het mondje;
# BOL = bolling van de voet (cilinderzijde); PUNTBREED = breedte van de uitstekende punten
N=9; KERN=0.70; RIN=0.30; LENGTE=0.62
BREED=int(opt('breed',1))      # tentakelbreedte in px (overal gelijk)
SEPSTART=opt("sepstart",1.4)
KRIMP=opt("krimp",0.75); ACHTER=(2,3,4)
a,c,L=klassen(); H,W=c.shape
RED={2,3,4,5}; WG={6,7,8,9,10}; KR={7,11,12,13,14,15}
TINT=[5,5,5,5,4]              # tentakeltint (model: T heeft vrijwel geen R3)
KROON=[3,3,3,3,3] if '--r1kroon' in sys.argv else [4,4,4,4,3]   # tussenkleur van de kroon: R1 (donkerder dan de tentakels; model R2 met veel R0-lijnen)
VOLG=[4,3,2,1,0]              # tekenvolgorde achter -> voor (T, R, L, VR, VL)
def wrap(x): return (x+np.pi)%(2*np.pi)-np.pi
def ctr(X,Y): return U0+(X+0.5-X0)/S, V0+(Y+0.5-Y0)/S
def sp(u,v): return X0+(u-U0)*S, Y0+(v-V0)*S          # natief (continu) -> sprite (continu)
# ---- natieve statistiek ----
own=np.full((H,W),-1); D=np.zeros((H,W)); T=np.zeros((H,W))
for v in range(105):
    for u in range(W):
        if c[v,u] in (1,2,3,4,5):
            i=eigenaar(u+.5,v+.5); own[v,u]=i; D[v,u]=afstand(i,u+.5,v+.5); T[v,u]=hoek(i,u+.5,v+.5)
def kroon_i(rc,t):
    x=(t+np.pi)/(np.pi/9)-0.5; i0=int(np.floor(x))%18; f=x-np.floor(x); return rc[i0]*(1-f)+rc[(i0+1)%18]*f
KLONT=[]; RC=[]
for i in range(5):
    licht=(own==i)&(c==TINT[i])&(D>0.18)
    for v,u in zip(*np.where(licht)):
        if in_mond(i,u+.5,v+.5,0.5): licht[v,u]=False
    th=T[licht]; dd=D[licht]
    tent=(own==i)&np.isin(c,[TINT[i],2])&(D>0.18)
    # kroonrand per 20 graden: 95e percentiel van d over het tentakelmateriaal (tentakeltint + R0-lijnen)
    rc=[]
    for b in range(18):
        t0=-np.pi+b*np.pi/9; mm=tent&(T>=t0)&(T<t0+np.pi/9)
        rc.append(np.percentile(D[mm],95) if mm.sum()>5 else None)
    vul=[x for x in rc if x is not None]; rc=[x if x is not None else max(vul) for x in rc]
    rc=[(rc[k-1]+2*rc[k]+rc[(k+1)%18])/4 for k in range(18)]          # glad: geen hapjes in de kroonrand
    RC.append(rc)
    sec=2*np.pi/N; best=None
    for phi in np.linspace(0,sec,80,endpoint=False):
        rel=np.abs(wrap(th-phi-sec*np.round((th-phi)/sec)))
        sc=(rel<=KERN*sec/2).sum()-(rel>KERN*sec/2).sum()
        if best is None or sc>best[0]: best=(sc,phi)
    kl=[]
    for k in range(N):
        c0=wrap(best[1]+k*sec)                                       # vaste sectoren: 9 gelijk verdeelde klonten
        m=np.abs(wrap(th-c0))<=sec/2
        cm=np.angle(np.exp(1j*th[m]).mean()) if m.sum()>=4 else c0  # richting = massamidden van de modeltentakels
        mt=tent&(np.abs(wrap(T-cm))<=sec/2)
        if np.sin(cm)<-0.2 and mt.sum()>4: ru=np.percentile(D[mt],97)   # boven/zijkant: tot de modelpunt (steekt uit)
        else: ru=kroon_i(rc,cm)-0.04                                      # onder: tot de kroonrand
        kl.append((cm,max(RIN,ru-LENGTE),ru))
    KLONT.append(kl)
# lichaamstint voor de voet (modelschaduw: R2, R1 waar het model R1 heeft)
def voettint(i,X,Y,R=1.6):
    uc,vc=ctr(X,Y); r=R/S; n=[0,0]
    for v in range(int(vc-r),int(vc+r)+1):
        for u in range(int(uc-r),int(uc+r)+1):
            if 0<=v<H and 0<=u<W and own[v,u]==i and (u+.5-uc)**2+(v+.5-vc)**2<=r*r and c[v,u] in (3,4): n[c[v,u]-3]+=1
    return 3 if n[0]>n[1] else 4
# ---- 1. kale reductie ----
o,F=kaal(); kaal_o=o.copy()
SIL=(kaal_o>0)&~np.isin(kaal_o,list(WG))&(np.arange(64)[:,None]<=31)
o[(np.arange(64)[:,None]<=31)&~np.isin(kaal_o,list(WG))]=0
OWN=np.full((64,64),-1)
# ---- 2. krater eerst (T, L en R liggen erachter, VL en VR ervoor) ----
# ---- 3. krater: nette ovaal, maten uit het model (natief: buitenrand x82-118 y48-67, gloed x88-112 y53-60,
# lichtgrijze bovenrand y49-52, bruine band y60-62, donkergrijze onderwand y62-67) ----
gd=(np.abs(a-a.mean(2,keepdims=True)).max(2)<12)&(L>=18)&(L<52)
yy,xx=np.mgrid[0:H,0:W]; kel=((xx+.5-100.0)/18.5)**2+((yy+.5-57.5)/10.5)**2<=1
PAL=list(PAL); PAL[7]=tuple(int(x) for x in np.median(a[gd&kel],axis=0))   # index 7 = donkergrijs (W1 komt niet voor)
# Krater uit het model overgenomen (keuring r6 punt 3, Jordi: "de krater mag wat netter rond"): ovale zwarte rand met
# gebogen boven- en onderlip (model x24-39, y10-17), lichtgrijze binnenrand boven/opzij, bruine schaduw onder de
# bovenlip, lensvormig bad met spitse uiteinden (oranje, geel alleen in het midden), bruine band eronder, donkergrijze
# onderwand. Per rij gemeten op het model (raster 30x, scratch mk.png); (x0, x1, index).
KRIJ={10:[(27,37,1)],
      11:[(25,26,1),(27,27,11),(28,36,12),(37,37,11),(38,39,1)],
      12:[(24,24,1),(25,27,11),(28,35,13),(36,38,11),(39,39,1)],
      13:[(24,24,1),(25,25,11),(26,28,14),(29,34,15),(35,37,14),(38,38,11),(39,39,1)],
      14:[(24,24,1),(25,27,7),(28,29,14),(30,33,15),(34,35,14),(36,38,7),(39,39,1)],
      15:[(25,25,1),(26,28,7),(29,34,12),(35,37,7),(38,38,1)],
      16:[(26,27,1),(28,35,7),(36,37,1)],
      17:[(28,35,1)]}
KRATER=np.zeros((64,64),bool)
for Y,rij in KRIJ.items():
    for x0,x1,k in rij:
        for X in range(x0,x1+1): o[Y,X]=k; KRATER[Y,X]=True; OWN[Y,X]=-1
print('krater: %d px'%KRATER.sum())
# ---- 3. anemonen ----
# kroonellips (sprite, continu): cx, cy, a, b; gemeten op het model (overlay ell.png in NOTITIES)
KROONELL=[(25.0,21.5,10.2,6.2),(43.5,20.0,8.8,6.0),(14.0,14.0,9.0,5.6),(49.0,12.3,8.6,5.4),(33.5,6.3,7.4,2.7)]
BASIS=[BASISK]*5
TUSSEN=[int(opt('tussen',3))]*5
TUSSEN[0]=TUSSEN[1]=int(opt('vtussen',2))   # voorste: scheidingslijnen R0 (meer definitie, als de vingers achter)
VHUB=opt('vhub',2.6)      # kleur tussen de tentakels (3 = R1: meer definitie dan R2)
# gemeten tentakelpunten van de achterste anemonen (gereedschap/punten.py); punten < 1,6 px uit elkaar samengevoegd;
# T: gat van >40 graden bovenin gevuld met de klontrichting uit het model (-80 graden)
sys.path.insert(0,'gereedschap'); from punten import punten
TIPS={}
for i,tp in punten(0.08,0.08,0.2).items():
    pts=[]
    for q,x,y in tp:
        if pts and np.hypot(x-pts[-1][0],y-pts[-1][1])<1.6: pts[-1]=((pts[-1][0]+x)/2,(pts[-1][1]+y)/2)
        else: pts.append((x,y))
    TIPS[i]=[np.array(p) for p in pts]
VOETSCHUIF=[(0,3.0),(0.5,3.2),(-1.5,6.5),(1.5,6.5),(0,4.0)]   # gemeten: onderkant van de voet in het model      # kroon = tussenkleur (model R2; T ligt in de schaduw: R1)
LICHT=[5,5,5,5,5]      # tentakels = modeltentakeltint R3 (alle vijf gelijk)
MBIN=[int(opt('mbin',5))]*5       # binnenkant mondje: R3 (licht, zoals het model: lichte binnenkant in een donkere ring)
ZONE=np.zeros((64,64),int)      # 1 kroon, 2 voet, 3 punt buiten de kroon
TENT=np.zeros((64,64),bool); MOND=np.zeros((64,64),bool); HALO=np.zeros((64,64),bool)
# achterste anemonen: de schijf is boven lager (b_boven), zodat de vingers als in het model ±4-5 px uitsteken
BBOVEN={2:opt('bl',3.6),3:opt('br',3.4),4:opt('bt',2.0),0:opt('bvl',4.2),1:opt('bvr',4.0)}
# mondjes (Jordi: 'de cirkel in het midden is wat slordig', alle vijf): één stempel 6x3 op het modelmidden
MW,MH=6,3
MHOEK='--geenhoek' not in sys.argv     # hoeken van de ring in R1: leest als ovaal i.p.v. '='
def mondbox(i):
    x0,x1,y0,y1=MONDBOX_M[i]; mx,my=(x0+x1+1)/2,(y0+y1+1)/2
    X0_=int(np.floor(mx-MW/2+0.5+opt('mdx',0))); Y0_=int(np.floor(my-MH/2+0.5))
    return X0_,X0_+MW-1,Y0_,Y0_+MH-1
MONDBOX_M=list(MONDBOX); MONDBOX=[mondbox(i) for i in range(5)]
print('mondjes', MONDBOX)
sys.path.insert(0,'r8'); from meet import meet
VR_V=opt('vvinger',0.95)   # straal van de vingers op VL/VR
def voorvingers(i,m):
    # gemeten modelrichtingen (pieken van licht R3 rond het mondje); te dicht bij elkaar (<SAMEN graden) samenvoegen,
    # gaten > GAT graden vullen met de klontrichting uit het model (KLONT)
    SAMEN=opt('samen',18); GAT=opt('gat',55)
    ps=[[np.radians(h),g,np.array([x,y])] for h,g,r,x,y in meet(i)]
    ps.sort(key=lambda p:p[0])
    while len(ps)>1:
        d=[np.degrees((ps[(k+1)%len(ps)][0]-ps[k][0])%(2*np.pi)) for k in range(len(ps))]
        k=int(np.argmin(d))
        if d[k]>=SAMEN: break
        a,b=ps[k],ps[(k+1)%len(ps)]; w=a[1]+b[1]
        t=np.angle(a[1]*np.exp(1j*a[0])+b[1]*np.exp(1j*b[0]))
        tip=a[2] if np.linalg.norm(a[2]-m)>=np.linalg.norm(b[2]-m) else b[2]
        n=[t,w,tip]; ps=[p for j,p in enumerate(ps) if j not in (k,(k+1)%len(ps))]+[n]; ps.sort(key=lambda p:p[0])
    extra=[]
    for cm,ri,ru in KLONT[i]:
        pt=punt(i,cm,ru); t=np.arctan2(*(pt-m)[::-1])
        if all(abs(np.degrees(wrap(t-p[0])))>=GAT/2 for p in ps+extra): extra.append([t,0,pt])
    ps=sorted(ps+extra,key=lambda p:p[0])
    return [(np.array([np.cos(p[0]),np.sin(p[0])]),p[2]) for p in ps]
# r8: voorste anemonen krijgen dezelfde opbouw als de achterste 3 (Jordi: "zoals de achterste 3"): de gemeten
# modelpunten boven (r8/meet.py, richting omhoog) worden vingers die boven de (lagere) kroonrand uitsteken, over de
# achterste anemonen heen; binnenin stralen zoals L/R/T.
VSTRAAL='--vstraal' in sys.argv   # proef r8a: Lileep-vingers (afgekeurd door Claude, zie NOTITIES)
if not VSTRAAL:
    for i in (0,1):
        pts=[]
        for h,g,r_,x,y in meet(i):
            if np.sin(np.radians(h))>-opt('vsin',0.25): continue
            if pts and np.hypot(x-pts[-1][0],y-pts[-1][1])<opt('vsamen',1.8): pts[-1]=((pts[-1][0]+x)/2,(pts[-1][1]+y)/2)
            else: pts.append((x,y))
        TIPS[i]=[np.array(p_) for p_ in pts]
def inc(i,x,y):
    cx,cy,a_,b_=KROONELL[i]
    if y<cy and i in BBOVEN: b_=BBOVEN[i]
    return ((x-cx)/a_)**2+((y-cy)/b_)**2<=1
def inell(i,X,Y,s=1.0):
    if s!=1.0:
        cx,cy,a_,b_=KROONELL[i]; return ((X+.5-cx)/(a_*s))**2+((Y+.5-cy)/(b_*s))**2<=1
    return inc(i,X+.5,Y+.5)
def punt(i,t,d):
    n,cx,cy,l,r,b,ov,f=AN[i]; ct,st=np.cos(t),np.sin(t)
    return np.array(sp(cx+d*ct*(l if ct<0 else r), cy+d*st*(b if st<0 else ov)))
def lijn(p0,p1):
    v=p1-p0; out=[]
    if abs(v[0])>=abs(v[1]):
        st=1 if v[0]>0 else -1
        for X in range(int(np.floor(p0[0])),int(np.floor(p1[0]))+st,st):
            out.append((X,int(np.floor(p0[1]+(X+0.5-p0[0])*v[1]/v[0]))))
    else:
        st=1 if v[1]>0 else -1
        for Y in range(int(np.floor(p0[1])),int(np.floor(p1[1]))+st,st):
            out.append((int(np.floor(p0[0]+(Y+0.5-p0[1])*v[0]/v[1])),Y))
    return out,abs(v[0])>=abs(v[1])
def randpunt(i,m,e):      # waar de straal m+t*e de kroon verlaat
    t=0.0
    while inc(i,*(m+e*t)) and t<30: t+=0.05
    return m+e*t
def mag(i,X,Y,voor):
    if not(1<=X<=62 and 2<=Y<=31): return False
    if KRATER[Y,X]: return False      # krater blijft de r4-ovaal (Jordi: rond, behouden)
    return True
VOLG=[4,2,3,1,0]; VOOR={0,1}
for i in VOLG:
    voor=i in VOOR
    # voet: de kroonellips naar beneden geschoven (zijkant van een lage cilinder, curven i.p.v. rechte naden),
    # binnen het modelsilhouet; tinten van de kale reductie (R1/R2 = modelschaduw)
    cx,cy,a_,b_=KROONELL[i]; vx,vy=VOETSCHUIF[i]
    for Y in range(2,32):
        for X in range(1,63):
            if not SIL[Y,X] or inell(i,X,Y) or KRATER[Y,X] or Y+.5<cy: continue
            if not any(((X+.5-cx-vx*t)/(a_*(1+BOL*np.sin(np.pi*t))))**2+((Y+.5-cy-vy*t)/b_)**2<=1 for t in np.linspace(0,1,13)): continue
            f=F[Y,X]; o[Y,X]=3 if f[3]+f[2]>f[4]+f[5] else 4; OWN[Y,X]=i; ZONE[Y,X]=2; TENT[Y,X]=False; MOND[Y,X]=False
    # kroon
    for Y in range(2,32):
        for X in range(1,63):
            if inell(i,X,Y) and mag(i,X,Y,voor) and not KRATER[Y,X]: o[Y,X]=TUSSEN[i]; OWN[Y,X]=i; ZONE[Y,X]=1; TENT[Y,X]=False; MOND[Y,X]=False
    # mondje: vast stempel (6x3, hoeken weg)
    x0,x1,y0,y1=MONDBOX[i]; mx,my,hx,hy=(x0+x1+1)/2,(y0+y1+1)/2,(x1-x0+1)/2,(y1-y0+1)/2; m=np.array([mx,my])
    for Y in range(y0,y1+1):
        for X in range(x0,x1+1):
            if (Y in (y0,y1)) and (X in (x0,x1)):
                if MHOEK: o[Y,X]=3; MOND[Y,X]=True; OWN[Y,X]=i; ZONE[Y,X]=1
                continue
            o[Y,X]=2 if ((Y in (y0,y1)) or (X in (x0,x1))) else MBIN[i]; MOND[Y,X]=True; OWN[Y,X]=i; ZONE[Y,X]=1
    # tentakels
    hk=[]      # (richting e vanaf het mondje, punt in sprite of None)
    if voor and not VSTRAAL:   # voorste: alle gemeten modelrichtingen (r8/meet.py); boven met de modelpunt
        hk=[(e,(tip if e[1]<-opt('vsin',0.25) else None)) for e,tip in voorvingers(i,m)]
    elif i in TIPS:          # achterste anemonen: punten boven = de gemeten modelpunten; onder = de klonten
        for pt in TIPS[i]:
            e=pt-m; hk.append((e/np.linalg.norm(e),pt))
        for cm,ri,ru in KLONT[i]:
            e=punt(i,cm,ru)-m; e=e/np.linalg.norm(e)
            if e[1]>0.45 and all(np.degrees(np.arccos(np.clip(e@f,-1,1)))>25 for f,_ in hk): hk.append((e,None))
    else:
        for cm,ri,ru in KLONT[i]:
            pt=punt(i,cm,ru); e=pt-m; e=e/np.linalg.norm(e); hk.append((e,pt if np.sin(cm)<-0.2 else None))
    if MODUS=='wig' and not (voor and VSTRAAL):
        # stralen (keuring r6 punt 2): de hele kroon licht (tentakels), per twee tentakels één doorlopende scheidingslijn
        # in R1 van de lichte ring rond het mondje tot de rand (1 px, buitenste deel 2 px), zodat elke tentakel één
        # doorlopende straal is. Licht linksboven, schaduwsikkel rechtsonder (punt 5): tentakels daar R2.
        cx,cy,a_,b_=KROONELL[i]
        for Y in range(2,32):
            for X in range(1,63):
                if OWN[Y,X]!=i or ZONE[Y,X]!=1 or MOND[Y,X]: continue
                nx,ny=(X+.5-cx)/a_,(Y+.5-cy)/b_
                o[Y,X]=SCHADUWK if (0.55*nx+0.83*ny)>SIKKEL else LICHT[i]; TENT[Y,X]=True
        ang=sorted(np.arctan2(e[1]/b_,e[0]/a_) for e,_ in hk)
        for k in range(len(ang)):
            q0,q1=ang[k],ang[(k+1)%len(ang)]
            if q1<=q0: q1+=2*np.pi
            qm=(q0+q1)/2; e=np.array([np.cos(qm)*a_,np.sin(qm)*b_]); e=e/np.linalg.norm(e)
            H_=VHUB if voor else HUB; p0=m+e*(1/np.sqrt((e[0]/(hx+H_))**2+(e[1]/(hy+H_*0.7))**2)); pr=randpunt(i,m,e)
            if (pr-p0)@e<=0.5: continue
            pix,vlak=lijn(p0,pr+e*0.6); L0=np.linalg.norm(pr-p0)
            for X,Y in pix:
                for extra in ((0,),(0,1))[int(np.linalg.norm(np.array([X+.5,Y+.5])-p0)>BUITEN*L0)]:
                    x,y=(X,Y+extra) if vlak else (X+extra,Y)
                    if 1<=x<=62 and y<=31 and OWN[y,x]==i and ZONE[y,x]==1 and not MOND[y,x]: o[y,x]=TUSSEN[i]; TENT[y,x]=False
    if i in TIPS:
        # vingers (keuring r6 punt 1): elke gemeten modelpunt = afgeronde vinger van ±2 px, waaiervormig (richting
        # mondje -> punt), licht (R3) met de schaduwkant R2; buiten de kroon, omlijning alleen om de vinger (stap 4)
        FD=np.full((64,64),9.0); FI=np.full((64,64),-1); FS=np.zeros((64,64),bool); FT=np.zeros((64,64))
        for fi,(e,pt) in enumerate(hk):
            if pt is None: continue
            pt=np.array([pt[0],max(pt[1],2.0)]); e=(pt-m)/np.linalg.norm(pt-m)
            pb=randpunt(i,m,e)-e*1.0; v=pt-pb; ln=np.linalg.norm(v)
            if ln<0.5: continue
            nrm=np.array([-v[1],v[0]])/ln
            if nrm@np.array([1,1])<0: nrm=-nrm          # naar de schaduwkant (rechtsonder)
            for Y in range(1,32):
                for X in range(1,63):
                    q=np.array([X+.5,Y+.5]); t=np.clip((q-pb)@v/ln**2,0,1); d=np.linalg.norm(q-(pb+t*v))
                    if d>VR_ or d>=FD[Y,X] or inell(i,X,Y) or not mag(i,X,Y,False) or MOND[Y,X]: continue
                    if OWN[Y,X]>=0 and OWN[Y,X]!=i and not voor: continue
                    FD[Y,X]=d; FI[Y,X]=fi; FS[Y,X]=(q-pb)@nrm>0.35 and t<0.85
        # twee vingers die elkaar raken: de pixel die het verst van zijn eigen as ligt wordt een donkere scheiding
        # (R0; zwart als hij aan de schaduwkant van zijn vinger ligt), zodat elke vinger los leest
        SCHEI=np.zeros((64,64),bool)
        for Y,X in zip(*np.where(FI>=0)):
            for dy,dx in ((0,1),(1,0),(0,-1),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)):
                j=FI[Y+dy,X+dx]
                if j>=0 and j!=FI[Y,X] and FD[Y,X]>=FD[Y+dy,X+dx] and not SCHEI[Y+dy,X+dx]: SCHEI[Y,X]=True; break
        for Y,X in zip(*np.where(FI>=0)):
            OWN[Y,X]=i
            if SCHEI[Y,X]: o[Y,X]=1 if FS[Y,X] else 2; ZONE[Y,X]=1; TENT[Y,X]=False
            else: o[Y,X]=SCHADUWK if FS[Y,X] else LICHT[i]; TENT[Y,X]=True; ZONE[Y,X]=3
    if voor and VSTRAAL:
        # r8, Jordi: "De voorste twee anemonen zijn nu veel te simpel" / "zoals de achterste 3": vingers van ±2 px in de
        # gemeten modelrichtingen, van net buiten het mondje tot de rand (onder) of tot de modelpunt (boven, steekt uit
        # zoals bij L/R/T), licht met de schaduwkant R2; waar twee vingers raken een donkere scheiding; ertussen de
        # kroontint R1. Schaduwsikkel rechtsonder: vingers R2.
        # Lileep-opbouw (Gen 3, tentakels in een krans): elke tentakel een lichte vinger van ±2 px met ronde punt,
        # een donkere lijn (R0) aan de schaduwkant, ertussen de kroontint (R2; in de sikkel R1); lichte voet rond het mondje.
        hk=voorvingers(i,m); cx,cy,a_,b_=KROONELL[i]
        HUBV=opt('hubv',0.8); VW=opt('vw',0.75); VL_=opt('vl',1.55)
        for Y in range(1,32):
            for X in range(1,63):
                if OWN[Y,X]==i and ZONE[Y,X]==1 and not MOND[Y,X]:
                    nx,ny=(X+.5-cx)/a_,(Y+.5-cy)/b_; sik=(0.55*nx+0.83*ny)>SIKKEL
                    o[Y,X]=3 if sik else 4; TENT[Y,X]=False
        FD=np.full((64,64),9.0); FI=np.full((64,64),-1); FS=np.zeros((64,64),bool)
        for fi,(e,tip) in enumerate(hk):
            hub=m+e*(1/np.sqrt((e[0]/(hx+HUBV))**2+(e[1]/(hy+HUBV*0.7))**2))
            rim=randpunt(i,m,e)
            if e[1]<-0.2: pt=rim+e*np.clip((tip-rim)@e,opt('minuit',1.2),UIT)
            else: pt=rim-e*opt('rimin',0.6)
            v=pt-hub; ln=np.linalg.norm(v)
            if ln<0.5: continue
            nrm=np.array([-v[1],v[0]])/ln
            if nrm@np.array([1,1])<0: nrm=-nrm
            for Y in range(1,32):
                for X in range(1,63):
                    q=np.array([X+.5,Y+.5]); t=np.clip((q-hub)@v/ln**2,0,1); d=np.linalg.norm(q-(hub+t*v))
                    if d>VL_ or not mag(i,X,Y,True) or MOND[Y,X]: continue
                    if not inell(i,X,Y) and (Y+.5>=cy or d>VW): continue
                    zij=(q-hub)@nrm
                    if d<=VW:
                        if d<FD[Y,X]: FD[Y,X]=d; FI[Y,X]=fi
                    elif zij>0 and t<1 and FD[Y,X]>=9: FS[Y,X]=True
        for Y,X in zip(*np.where(FS&(FI<0))):
            o[Y,X]=2; TENT[Y,X]=False
        for Y,X in zip(*np.where(FI>=0)):
            OWN[Y,X]=i; binnen=inell(i,X,Y)
            nx,ny=(X+.5-cx)/a_,(Y+.5-cy)/b_; sik=(0.55*nx+0.83*ny)>SIKKEL
            o[Y,X]=SCHADUWK if sik else LICHT[i]; TENT[Y,X]=True; ZONE[Y,X]=1 if binnen else 3
        for Y in range(1,32):
            for X in range(1,63):
                if OWN[Y,X]==i and ZONE[Y,X]==1 and not MOND[Y,X] and ((X+.5-mx)/(hx+HUBV))**2+((Y+.5-my)/(hy+HUBV*0.7))**2<=1:
                    o[Y,X]=LICHT[i]; TENT[Y,X]=True
    # lichte rand van 1 px om elk mondje (alle vijf gelijk), zodat de ring los leest
    cx,cy,a_,b_=KROONELL[i]
    for Y in range(y0-1,y1+2):
        for X in range(x0-1,x1+2):
            if MOND[Y,X] or OWN[Y,X]!=i: continue
            if not any(MOND[Y+dy,X+dx] and OWN[Y+dy,X+dx]==i for dy in (-1,0,1) for dx in (-1,0,1)): continue
            nx,ny=(X+.5-cx)/a_,(Y+.5-cy)/b_
            o[Y,X]=SCHADUWK if (0.55*nx+0.83*ny)>SIKKEL else LICHT[i]; TENT[Y,X]=True; HALO[Y,X]=True
    print("TELLING",AN[i][0],len(hk)) if "--tel" in sys.argv else None
    for e,pt in hk:
        p0=m+e*(1/np.sqrt((e[0]/(hx+START))**2+(e[1]/(hy+START))**2))
        pr=randpunt(i,m,e)
        if MODUS=='wig': continue
        if pt is not None:       # boven/zijkant: tot de modelpunt, hooguit UIT px buiten de rand
            L_=np.linalg.norm(pt-pr)*(1 if (pt-pr)@e>0 else -1)
            p1=pr+e*np.clip(L_,0.6,UIT)
        else:
            if MODUS=='wig': continue
            p1=pr-e*0.4
        if MODUS=='wig': p0=pr-e*1.0
        pix,vlak=lijn(p0,p1)
        for X,Y in pix:
            for k in range(BREED if MODUS!='wig' else PUNTBREED):
                x,y=(X,Y-k) if vlak else (X-k,Y)
                if not mag(i,x,y,voor) or MOND[y,x]: continue
                if OWN[y,x]==i and ZONE[y,x]==2: continue
                if not inell(i,x,y): ZONE[y,x]=3
                o[y,x]=LICHT[i]; TENT[y,x]=True; OWN[y,x]=i
            if LIJN:
                x,y=(X,Y+1) if vlak else (X+1,Y)
                if 1<=x<=62 and y<=31 and OWN[y,x]==i and ZONE[y,x]==1 and not TENT[y,x] and not MOND[y,x]: o[y,x]=LIJNK
if '--vdiag' in sys.argv:
    for y in range(0,16): print('V%2d '%y+''.join('F' if (TENT[y,x] and ZONE[y,x]==3) else ('c' if ZONE[y,x]==1 else ('.' if o[y,x]==0 else '#')) for x in range(64)))
# keel onder de krater (tussen VL en VR): kale reductie terug (modelkleuren zwart/grijs/bruin), zoals r4
KEEL=SIL&(o==0)&~KRATER&np.isin(kaal_o,[1,7,11,12])
o[KEEL]=kaal_o[KEEL]
print('keel uit de kale reductie: %d px'%KEEL.sum())
gat=SIL&(o==0)&~KRATER
# gaten onder het kroonmidden van de eigenaar (rond de krater, tussen de voeten): voettint; erboven = ruimte tussen punten
for Y,X in zip(*np.where(gat)):
    i=eigenaar(*ctr(X,Y))
    if Y+.5>=KROONELL[i][1]:
        f=F[Y,X]; o[Y,X]=3 if f[3]+f[2]>f[4]+f[5] else 4; OWN[Y,X]=i; ZONE[Y,X]=2
gat=SIL&(o==0)&~KRATER
print('gaten in het silhouet (niet door een anemoon bedekt): %d'%gat.sum())
# ingesloten gaatjes (niet met de achtergrond verbonden, naast de krater): zwart zoals de kraterrand in het model
bgm=(o==0); lab,n=label(bgm,acht=False)
buiten={lab[0,0]}
INGESLOTEN=np.zeros((64,64),bool)
for j in range(1,n+1):
    m_=lab==j
    if j in buiten or m_[0,:].any() or m_[-1,:].any() or m_[:,0].any() or m_[:,-1].any(): continue
    if m_.sum()<=4 and np.where(m_)[0].max()<=31: INGESLOTEN|=m_
o[INGESLOTEN]=1
print('ingesloten gaatjes -> zwart: %d px'%INGESLOTEN.sum())
# ---- 4. lijnen ----
RANG={i:VOLG.index(i) for i in range(5)}
nw=o.copy()
for Y,X in zip(*np.where(OWN>=0)):
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        j=OWN[Y+dy,X+dx]
        if j>=0 and j!=OWN[Y,X] and RANG[j]>RANG[OWN[Y,X]] and not MOND[Y,X] and not HALO[Y,X]: nw[Y,X]=1; break
o=nw
# onderrand op het lijf: zwart (zoals r4)
for Y,X in zip(*np.where((OWN>=0)&(np.arange(64)[:,None]<=31))):
        if o[Y+1,X] in WG: o[Y,X]=1
# kroonrand onder (kroon -> voet): R0, behalve waar een tentakel eindigt
for Y,X in zip(*np.where(ZONE==2)):
    if OWN[Y-1,X]==OWN[Y,X] and ZONE[Y-1,X]==1 and not TENT[Y-1,X] and not MOND[Y-1,X] and o[Y-1,X]>1: o[Y-1,X]=2
# buitenrand: R0 aan de lichtkant (links/boven), zwart aan de schaduwkant
fg=o>0; uit=[]
for Y,X in zip(*np.where(fg&(np.arange(64)[:,None]<=31)&(OWN>=0))):
    bL=not fg[Y,X-1]; bR=not fg[Y,X+1]; bU=not fg[Y-1,X]; bD=not fg[Y+1,X]
    if not(bL or bR or bU or bD): continue
    uit.append((Y,X))
for Y,X in uit:
    if TENT[Y,X] and ZONE[Y,X]==3:      # punt: licht houden, lijn erbuiten
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            if o[Y+dy,X+dx]==0 and Y+dy>=1: o[Y+dy,X+dx]=1 if (dx==1 or dy==1) else 2; OWN[Y+dy,X+dx]=OWN[Y,X]
    else:
        bR=not fg[Y,X+1]; bD=not fg[Y+1,X]; bL=not fg[Y,X-1]
        o[Y,X]=1 if (bR or (bD and not bL)) else 2
# ruis weg: losse pixel (geen gelijke 8-buur) binnen een anemoon, niet aan de achtergrond en niet in het mondje ->
# meest voorkomende 4-buur (vlaktint gaat voor lijn)
RUIS=0
for ronde in range(2):
    P_=np.pad(o,1)
    for Y,X in zip(*np.where((o>=2)&(o<=5)&(OWN>=0)&~MOND&~HALO&(np.arange(64)[:,None]<=31))):
        n8=[P_[Y+1+dy,X+1+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
        if o[Y,X] in n8 or 0 in n8: continue
        n4=[P_[Y+1+dy,X+1+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
        k=[v for v in n4 if 3<=v<=5] or [v for v in n4 if 1<=v<=5]
        if k: o[Y,X]=max(set(k),key=k.count); RUIS+=1
print('ruis weggehaald: %d px'%RUIS)
# ---- 5. lijf, armen en rechterpoot bevroren op r4 (gelaat A); linkerpoot schuiner ----
r4A=np.asarray(Image.open('r4/vileplume_r4_gelaatA.png')).astype(int)
BEV=np.isin(r4A,list(WG))|(np.arange(64)[:,None]>=32)
o[BEV]=r4A[BEV]
# Linkerpoot (links op het scherm), Jordi over r7: "de poot misschien toch maar het model na maken met de knik erin".
# Rij voor rij uit het model (dekking per spritepixel, r8/NOTITIES): bovenbeen y44-50 naar links (x23-25), knik op y51,
# scheen y51-58 één kolom naar rechts (x24-26), voet y59 zwart (x25-26). Vulling en schaduwkant zoals het model
# (knie y46-51 rechts donkergrijs W0, scheen rechts zwart). Heup y41-43 = r4.
POOT=np.zeros((64,64),bool)
for Y in range(44,61):
    for X in range(18,31):
        if r4A[Y,X]>0 or o[Y,X]>0: o[Y,X]=0; POOT[Y,X]=True
a_,e_,d_,c_,K_=6,10,9,8,1
LINKS={44:(24,[a_,e_,K_]),45:(23,[a_,e_,e_,K_]),46:(23,[a_,e_,a_]),47:(23,[a_,d_,a_]),48:(23,[a_,d_,a_]),
       49:(23,[a_,d_,a_]),50:(23,[a_,d_,a_]),51:(24,[a_,d_,a_]),52:(24,[a_,d_,K_]),53:(24,[a_,d_,K_]),
       54:(24,[a_,c_,K_]),55:(24,[a_,c_,K_]),56:(24,[a_,c_,K_]),57:(24,[a_,c_,K_]),58:(24,[a_,c_,K_]),59:(25,[K_,K_])}
for Y,(x,rij) in LINKS.items():
    for k,v in enumerate(rij): o[Y,x+k]=v; POOT[Y,x+k]=True
# ---- 6. gelaat: varianten. Jordi: "Je mag qua gelaat afwerken van het model, het zou leuk zijn als we de ogen wel
# goed kunnen zien" / over r7: "Het gezicht is nog steeds niet zichtbaar". Gen 3 (Vileplume, Oddish): ogen van 2 px
# breed, met een lichte rij tussen de kroonrand en de ogen. Ogen op de plek van de U uit het model (x25 en x29 ->
# 2 px breed: x24-25 en x29-30), y33 en lager (y32 blijft licht).
basis=o.copy()
def gelaat(o,var):
    o=o.copy()
    if var=='A': return o                                   # model (U)
    for X in range(25,30): o[33,X]=10                       # U uit het model weg
    for X in range(26,29): o[34,X]=10
    hoog=3 if var in ('D',) else 2
    for X0_ in (24,29):
        for dy in range(hoog):
            for dx in (0,1): o[33+dy,X0_+dx]=1
        if var in ('C','D'): o[33,X0_]=10                   # glanspixel linksboven
    if var=='E':
        for X in (27,28): o[36,X]=6                         # klein mondje (W0)
    return o
VARS='ABCDE'
VAR={v:gelaat(basis,v) for v in VARS}
STANDAARD=sys.argv[sys.argv.index('--gelaat')+1] if '--gelaat' in sys.argv else 'B'
o=VAR[STANDAARD]
r4=np.asarray(Image.open('r4/vileplume_r4.png')).astype(int)
GEL=(np.arange(64)[:,None]>=32)&(np.arange(64)[:,None]<=36)&(np.arange(64)[None,:]>=23)&(np.arange(64)[None,:]<=31)
assert ((o!=r4)&BEV&~POOT&~GEL).sum()==0, 'lijf/armen/rechterpoot niet bevroren'
opslaan(o,PAL,RONDE+'/vileplume_%s.png'%RONDE)
for v in VARS: opslaan(VAR[v],PAL,RONDE+'/vileplume_%s_gelaat%s.png'%(RONDE,v))
r7=np.asarray(Image.open('r7/vileplume_r7.png')).astype(int)
assert ((o!=r7)&KRATER).sum()==0, 'krater niet gelijk aan r7'
opslaan(kaal_o,PAL,RONDE+'/kaal.png')
diff=o!=kaal_o; d4=o!=r7
Z={'anemonen':(np.arange(64)[:,None]<=31)&~KRATER,'krater':KRATER,'lijf+armen':(np.arange(64)[:,None]>=32)&~POOT&(np.arange(64)[:,None]<=41),
   'poten':(np.arange(64)[:,None]>=42)}
for n,m in Z.items(): print('zone %-10s t.o.v. kaal %4d px | t.o.v. r7 %4d px'%(n,(diff&m).sum(),(d4&m).sum()))
print('mondjes %d px, tentakels %d px'%(MOND.sum(),TENT.sum()))
ch='.K0123abcdeGuomy'
print('   '+''.join(str(x%10) for x in range(64)))
for y in range(64): print('%2d '%y+''.join(ch[v] for v in o[y]))
if '--gat' in sys.argv:
    for y in range(32): print('%2d '%y+''.join('#' if gat[y,x] else ('K' if KRATER[y,x] else ('.' if OWN[y,x]<0 else str(OWN[y,x]))) for x in range(64)))
