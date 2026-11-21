# Vileplume (Kelp-/anemoonlijn) r7 = r6 + keuring r6 punt 1-6: vingers op de achterste anemonen, doorlopende stralen, krater-ovaal met lensbad, gelaat B 1 px lager, licht/schaduw per kroon, beeneinden uit het model.
#  1. anemonen netjes en alle vijf gelijk opgebouwd (Jordi over r3: "de anemonen zijn niet allemaal even netjes";
#     over r4: "nu neemt wel de definitie af idd"): per anemoon kroon (rustig vlak in de tussenkleur) -> mondje (ovaal,
#     modelkleur) -> 9 rechte tentakels in modelrichting, elk met een vaste breedte en een vaste donkere lijn aan de
#     schaduwkant -> punten steken uit waar het model ze laat uitsteken -> donkere rand om elke anemoon -> voet uit de
#     kale reductie. Geen tapse tentakels, geen losse blokjes.
#  2. krater: als r4 (rond).
#  3. linkerpoot (links op het scherm): Jordi "schuiner", hele poot schuiner, meer naar buiten; 3-px-opbouw
#     lijn - vulling - zwart zoals r4.
#  4. lijf, armen, rechterpoot: bevroren op r4 (gelaat A als basis, B standaard, A/C varianten).
# Opbouw per anemoon (r5): kroonschijf = nette ellips gemeten op het model (de mondjes liggen op het model) -> 9
# tentakels als rechte lichte stralen met één vaste breedte, in modelrichting, van net buiten het mondje tot de
# kroonrand; boven/opzij steken ze uit tot de modelpunt (begrensd) -> mondje -> voet = kale reductie onder de kroon
# (alleen modeltinten R1/R2) -> donkere rand om elke anemoon. Volgorde achter -> voor: T, L, R, (krater), VR, VL.
# Gebruik (vanuit vileplume_sprite/): python3 r5/bouw.py [RONDE] [--breed=2] [--uit=3] [--lijn=0|1]
# Gebruik (vanuit vileplume_sprite/): python3 r5/bouw.py [RONDE] [opties]
import sys, numpy as np
sys.path.insert(0,'gereedschap'); sys.path.insert(0,'r1')
from PIL import Image
from klassen import klassen; from gemeen import *; from anemonen import *
from kaal import kaal, PAL
RONDE=sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('-') else 'r7'
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
TUSSEN=[int(opt('tussen',3))]*5      # kleur tussen de tentakels (3 = R1: meer definitie dan R2)
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
TENT=np.zeros((64,64),bool); MOND=np.zeros((64,64),bool)
# achterste anemonen: de schijf is boven lager (b_boven), zodat de vingers als in het model ±4-5 px uitsteken
BBOVEN={2:opt('bl',3.6),3:opt('br',3.4),4:opt('bt',2.0)}
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
    # mondje (bbox van de modelring)
    x0,x1,y0,y1=MONDBOX[i]; mx,my,hx,hy=(x0+x1+1)/2,(y0+y1+1)/2,(x1-x0+1)/2,(y1-y0+1)/2; m=np.array([mx,my])
    for Y in range(y0,y1+1):
        for X in range(x0,x1+1):
            if (Y in (y0,y1)) and (X in (x0,x1)): continue
            o[Y,X]=2 if ((Y in (y0,y1)) or (X in (x0,x1))) else MBIN[i]; MOND[Y,X]=True; OWN[Y,X]=i; ZONE[Y,X]=1
    # tentakels
    hk=[]      # (richting e vanaf het mondje, punt in sprite of None)
    if i in TIPS:          # achterste anemonen: punten boven = de gemeten modelpunten; onder = de klonten
        for pt in TIPS[i]:
            e=pt-m; hk.append((e/np.linalg.norm(e),pt))
        for cm,ri,ru in KLONT[i]:
            e=punt(i,cm,ru)-m; e=e/np.linalg.norm(e)
            if e[1]>0.45 and all(np.degrees(np.arccos(np.clip(e@f,-1,1)))>25 for f,_ in hk): hk.append((e,None))
    else:
        for cm,ri,ru in KLONT[i]:
            pt=punt(i,cm,ru); e=pt-m; e=e/np.linalg.norm(e); hk.append((e,pt if np.sin(cm)<-0.2 else None))
    if MODUS=='wig':
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
            p0=m+e*(1/np.sqrt((e[0]/(hx+HUB))**2+(e[1]/(hy+HUB*0.7))**2)); pr=randpunt(i,m,e)
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
                    if OWN[Y,X]>=0 and OWN[Y,X]!=i: continue
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
        if j>=0 and j!=OWN[Y,X] and RANG[j]>RANG[OWN[Y,X]] and not MOND[Y,X]: nw[Y,X]=1; break
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
    for Y,X in zip(*np.where((o>=2)&(o<=5)&(OWN>=0)&~MOND&(np.arange(64)[:,None]<=31))):
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
# Linkerpoot (links op het scherm), Jordi: "schuiner". Rijen y44-59 opnieuw als 3 px (W0-lijn | vulling | zwart),
# vulling per rij zoals r4; linkerkant x = 25 - 0,27*(y-44) (y44 x25 -> y59 x21), gelijkmatige trap van ±4 rijen.
# Heup (y41-43) en voetrij blijven de r4-opbouw.
POOT=np.zeros((64,64),bool)
oud={}
for Y in range(44,60):
    xs=[X for X in range(18,31) if r4A[Y,X]>0]; oud[Y]=[r4A[Y,X] for X in xs]
    for X in xs: o[Y,X]=0; POOT[Y,X]=True
for Y in range(44,60):
    x=int(round(25-0.27*(Y-44)+0.0001))
    vul=[v for v in oud[Y] if v in (8,9,10)]
    rij=[6,vul[0] if vul else (oud[Y-1] and [v for v in oud[Y-1] if v in (8,9,10)][0]) or 8,1]
    for k,v in enumerate(rij): o[Y,x+k]=v; POOT[Y,x+k]=True
# beeneinde uit het model (keuring r6 punt 6): de poot loopt licht uit tot de laatste rij (lijn | licht | zwart) met
# eronder een zwart kapje van 2 px onder lijn en licht (model: linkervoet y59 + kap y60, rechtervoet y60-61 + kap y62;
# de rechtervoet had dat al, ongewijzigd)
xl=int(round(25-0.27*(59-44)+0.0001)); o[60,xl]=1; o[60,xl+1]=1; POOT[60,xl]=POOT[60,xl+1]=True
# ---- 6. gelaat: varianten (zoals r4) ----
basis=o.copy()
def gelaat(o,var):
    o=o.copy()
    if var=='A': return o
    # B/C: ogen 1x2 zwart, één rij lager dan in r4 (y33-34) zodat de lichte modelrij y32 tussen kroonrand en ogen blijft
    # (keuring r6 punt 4); B: balkje van het model mee één rij lager (y35), C: zonder balkje
    for X in (25,29): o[33,X]=1; o[34,X]=1
    for X in (26,27,28): o[34,X]=10
    if var=='B':
        for X in (26,27,28): o[35,X]=6
    return o
VAR={v:gelaat(basis,v) for v in 'ABC'}
o=VAR['B']
r4=np.asarray(Image.open('r4/vileplume_r4.png')).astype(int)
GEL=(np.arange(64)[:,None]>=32)&(np.arange(64)[:,None]<=35)&(np.arange(64)[None,:]>=24)&(np.arange(64)[None,:]<=30)
assert ((o!=r4)&BEV&~POOT&~GEL).sum()==0, 'lijf/armen/rechterpoot niet bevroren'
opslaan(o,PAL,RONDE+'/vileplume_%s.png'%RONDE)
for v in 'AC': opslaan(VAR[v],PAL,RONDE+'/vileplume_%s_gelaat%s.png'%(RONDE,v))
opslaan(kaal_o,PAL,RONDE+'/kaal.png')
diff=o!=kaal_o; d4=o!=r4
Z={'anemonen':(np.arange(64)[:,None]<=31)&~KRATER,'krater':KRATER,'lijf+armen':(np.arange(64)[:,None]>=32)&~POOT&(np.arange(64)[:,None]<=41),
   'poten':(np.arange(64)[:,None]>=42)}
for n,m in Z.items(): print('zone %-10s t.o.v. kaal %4d px | t.o.v. r4 %4d px'%(n,(diff&m).sum(),(d4&m).sum()))
print('mondjes %d px, tentakels %d px'%(MOND.sum(),TENT.sum()))
ch='.K0123abcdeGuomy'
print('   '+''.join(str(x%10) for x in range(64)))
for y in range(64): print('%2d '%y+''.join(ch[v] for v in o[y]))
if '--gat' in sys.argv:
    for y in range(32): print('%2d '%y+''.join('#' if gat[y,x] else ('K' if KRATER[y,x] else ('.' if OWN[y,x]<0 else str(OWN[y,x]))) for x in range(64)))
