# Vileplume (Kelp-/anemoonlijn) r4. Benoemde reparaties (coordinator + Jordi over r3):
#  1. elke anemoon = vlak tentakelschijfje (kroon, gemeten op het model) + gladde voet eronder (kale reductie);
#  2. klonten taps naar de punt, tussenkleur van de kroon zichtbaar, punten steken uit waar het model ze laat uitsteken;
#     elke anemoon op dezelfde manier opgebouwd (Jordi: "de anemonen zijn niet allemaal even netjes");
#  3. krater: nette ovaal met de maten en verhouding van het model (zwarte rand, lichtgrijze bovenrand, donkergrijze
#     onderwand, bruine band, grote oranje-gele gloed) (Jordi: "de krater mag wat netter rond");
#  4. linkerpoot: gemeten, niet aangepast (zie stap 5; vraag aan Jordi);
#  5. gelaat: ogen leesbaar (Jordi: "het zou leuk zijn als we de ogen wel goed kunnen zien"), varianten A/B/C.
# Lijf en poten: bevroren op r3 (pixeldiff 0 buiten het gelaat, geassert).
# Gebruik (vanuit vileplume_sprite/): python3 r4/bouw.py
import sys, numpy as np
sys.path.insert(0,'gereedschap'); sys.path.insert(0,'r1')
from PIL import Image
from klassen import klassen; from gemeen import *; from anemonen import *
from kaal import kaal, PAL
RONDE='r4'
N=9; KERN=0.70; RIN=0.30; LENGTE=0.62
DIK=float(sys.argv[1]) if len(sys.argv)>1 else 0.3   # deel van de tentakel (vanaf de voet) dat 2 px breed is; daarna 1 px (taps)
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
r3=np.asarray(Image.open('r3/vileplume_r3.png')).astype(int)
# ---- 2. anemonen: elke anemoon dezelfde opbouw ----
OWN=np.full((64,64),-1); ZONE=np.zeros((64,64),int)     # 1 kroon, 2 voet, 3 punt/rand buiten de kroon
kr_ell=lambda u,v: ((u-100.0)/18.5)**2+((v-57.5)/10.5)**2<=1
for Y in range(1,32):
    for X in range(1,63):
        k=kaal_o[Y,X]
        if k in WG: continue
        if k==1 and F[Y,X,2:6].sum()<0.15: continue
        uc,vc=ctr(X,Y)
        if k in KR or (kr_ell(uc,vc) and F[Y,X,2:6].sum()<0.5): continue
        i=eigenaar(uc,vc); d=afstand(i,uc,vc); t=hoek(i,uc,vc)
        if d>1.6: continue
        rc=kroon_i(RC[i],t)
        if d<=rc:
            if k==0 and np.sin(t)<-0.2: continue      # boven de schijf: alleen punten (stap hieronder)
            o[Y,X]=KROON[i]; ZONE[Y,X]=1
        elif k==0: continue
        elif np.sin(t)>0.2:
            o[Y,X]=k if k in (3,4) else voettint(i,X,Y); ZONE[Y,X]=2
        else:
            if F[Y,X,0]>=0.2: o[Y,X]=0; continue
            o[Y,X]=KROON[i]; ZONE[Y,X]=1
        OWN[Y,X]=i
print('kroon/voet: %d px anders dan kaal'%(o!=kaal_o).sum())
# tentakels: lijn van basis naar punt, 2 px breed in het eerste deel DIK (tweede pixel aan de lichtkant), daarna 1 px (taps)
STRAAL=np.zeros((64,64),bool); SCHADUW=[]
def punt(i,t,d):
    n,cx,cy,l,r,b,ov,f=AN[i]; ct,st=np.cos(t),np.sin(t)
    return sp(cx+d*ct*(l if ct<0 else r), cy+d*st*(b if st<0 else ov))
for i in VOLG:
    for cm,ri,ru in KLONT[i]:
        p0=np.array(punt(i,cm,ri)); p1=np.array(punt(i,cm,ru)); v=p1-p0; ln=np.linalg.norm(v)
        if ln<1: continue
        nrm=np.array([-v[1],v[0]])/ln
        if nrm@np.array([-1,-1])<0: nrm=-nrm                  # naar linksboven (licht)
        for t in np.linspace(0,1,int(ln*4)+2):
            p=p0+t*v; pix=[p]
            if t<DIK: pix.append(p+nrm*0.9)
            for q in pix:
                X,Y=int(np.floor(q[0])),int(np.floor(q[1]))
                if not(1<=X<=62 and 1<=Y<=31): continue
                if OWN[Y,X]==i or (OWN[Y,X]<0 and kaal_o[Y,X] not in KR and np.sin(cm)<-0.2 and not kr_ell(*ctr(X,Y))):
                    o[Y,X]=TINT[i]; OWN[Y,X]=i; STRAAL[Y,X]=True
                    if ZONE[Y,X]==0: ZONE[Y,X]=3
            q=p-nrm*0.9; SCHADUW.append((int(np.floor(q[1])),int(np.floor(q[0])),i))   # schaduwkant (weg van het licht)
print('tentakels: %d px straal'%STRAAL.sum())
# R0 aan de schaduwkant van elke tentakel, binnen de eigen kroon; punt tegen achtergrond: lijn erbuiten
for y,x,i in (SCHADUW if '--geenschaduw' not in sys.argv else []):          # optie: R0-lijn langs de schaduwkant
    if 1<=y<=31 and 1<=x<=62 and OWN[y,x]==i and not STRAAL[y,x] and ZONE[y,x]==1: o[y,x]=2
for Y,X in zip(*np.where(STRAAL)):
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        y,x=Y+dy,X+dx
        if 1<=y<=62 and 1<=x<=62 and o[y,x]==0 and OWN[y,x]<0: o[y,x]=2; OWN[y,x]=OWN[Y,X]; ZONE[y,x]=3
# mondjes: ovaal op de bbox van de modelring
MOND=np.zeros((64,64),bool)
for i,(x0,x1,y0,y1) in enumerate(MONDBOX):
    for Y in range(y0,y1+1):
        for X in range(x0,x1+1):
            if (Y in (y0,y1)) and (X in (x0,x1)): continue
            o[Y,X]=2 if ((Y in (y0,y1)) or (X in (x0,x1))) else 4; OWN[Y,X]=i; MOND[Y,X]=True; STRAAL[Y,X]=False
# donkere rand om elke anemoon: pixel van een verder-achter-anemoon naast een voorste -> zwart
RANG={i:VOLG.index(i) for i in range(5)}      # hoger = meer vooraan
for Y,X in zip(*np.where(OWN>=0)):
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        j=OWN[Y+dy,X+dx]
        if j>=0 and j!=OWN[Y,X] and RANG[j]>RANG[OWN[Y,X]] and o[Y+dy,X+dx]>0 and o[Y,X]>0: o[Y,X]=1; break
# kroonrand van de voorste anemonen: overgang kroon -> voet als donkerrode lijn waar het model de kroonrand heeft
# (alleen als een tentakelpunt er niet al ligt)
for Y,X in zip(*np.where(ZONE==2)):
    if OWN[Y-1,X]==OWN[Y,X] and ZONE[Y-1,X]==1 and not STRAAL[Y-1,X] and not MOND[Y-1,X] and o[Y-1,X]==KROON[OWN[Y,X]]:
        o[Y-1,X]=2
print('anemonen: %d px anders dan kaal'%((o!=kaal_o)&(OWN>=0)).sum())
# ---- 3. krater: nette ovaal, maten uit het model (natief: buitenrand x82-118 y48-67, gloed x88-112 y53-60,
# lichtgrijze bovenrand y49-52, bruine band y60-62, donkergrijze onderwand y62-67) ----
gd=(np.abs(a-a.mean(2,keepdims=True)).max(2)<12)&(L>=18)&(L<52)
yy,xx=np.mgrid[0:H,0:W]; kel=((xx+.5-100.0)/18.5)**2+((yy+.5-57.5)/10.5)**2<=1
PAL=list(PAL); PAL[7]=tuple(int(x) for x in np.median(a[gd&kel],axis=0))   # index 7 = donkergrijs (W1 komt niet voor)
def ell(X,Y,cx,cy,rx,ry): return ((X+.5-cx)/rx)**2+((Y+.5-cy)/ry)**2
oc=sp(100.5,58.0); orx,ory=36.5*S/2,19.5*S/2          # buitenrand
gc=sp(100.5,57.0); grx,gry=25*S/2,8*S/2              # gloed
KRATER=np.zeros((64,64),bool)
gtop=int(np.floor(gc[1]-gry+0.5)); gbot=int(np.floor(gc[1]+gry-0.5))      # bovenste/onderste gloedrij
for Y in range(6,20):
    for X in range(20,44):
        if ell(X,Y,*oc,orx,ory)>1: continue
        # hele ovaal (Jordi: "de krater mag wat netter rond"); de keel eronder blijft de kale reductie
        KRATER[Y,X]=True
for Y,X in zip(*np.where(KRATER)):
    buiten=[not KRATER[Y+dy,X+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
    eg=ell(X,Y,*gc,grx,gry)
    if any(buiten): o[Y,X]=1                                     # zwarte buitenrand
    elif eg<=1:
        if Y==gtop: o[Y,X]=13                                    # bovenste gloedrij roodoranje
        elif ell(X,Y,gc[0],gc[1]+0.5,grx*0.7,gry)<=1: o[Y,X]=15   # geel hart
        else: o[Y,X]=14                                          # oranje
    elif Y<=gtop or (Y<=gbot and Y+.5<gc[1]): o[Y,X]=11           # lichtgrijze bovenrand (en zijkant naast de bovenste gloed)
    elif Y==gbot+1 and abs(X+.5-gc[0])<=grx: o[Y,X]=12            # bruine band direct onder de gloed
    else: o[Y,X]=7                                               # donkergrijze ring/onderwand
    OWN[Y,X]=-1
print('krater: %d px'%KRATER.sum())
# ---- 4. buitenlijn (rood), losse pixels en ontkorrelen in de anemonen ----
def rand(o):
    fg=o>0; uit=[]
    for Y,X in zip(*np.where(fg&(np.arange(64)[:,None]<=31))):
        if o[Y,X] not in RED: continue
        bL=not fg[Y,X-1]; bR=not fg[Y,X+1]; bU=not fg[Y-1,X]; bD=not fg[Y+1,X]
        if not(bL or bR or bU or bD): continue
        uit.append((Y,X,1 if (bR or (bD and not bL)) else 2))
    for Y,X,k in uit: o[Y,X]=k
rand(o)
for ronde in range(3):
    P=np.pad(o,1)
    for Y,X in zip(*np.where((o>0)&(OWN>=0))):
        k=o[Y,X]
        if MOND[Y,X]: continue
        n8=[P[Y+1+dy,X+1+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
        if k in n8: continue
        n4=[P[Y+1+dy,X+1+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
        if 0 in n4 and k in (1,2): continue
        kand=[v for v in n4 if v in RED or v==1]
        if kand: o[Y,X]=max(set(kand),key=kand.count)
for k in (3,4,5):
    lab,n=label(o==k,acht=False)
    for j in range(1,n+1):
        m=lab==j
        if m.sum()>=3 or MOND[m].any() or STRAAL[m].any(): continue
        buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(m)) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if o[Y+dy,X+dx] in (3,4,5) and o[Y+dy,X+dx]!=k]
        if buur: o[m]=max(set(buur),key=buur.count)
# ---- 5. lijf en rechterpoot bevroren op r3; linkerpoot (kijkerslinks) opnieuw uit het verloop van het model ----
BEV=np.isin(r3,list(WG))|(np.arange(64)[:,None]>=32)
o[BEV]=r3[BEV]
POOT=np.zeros((64,64),bool)
# Linkerpoot: NIET aangepast. Gemeten middenlijn van het model per spriterij (kijkerslinks: y41 28,1 -> knie y46-48 24,6
# -> y56-58 25,9 -> voet y60 25,5; kijkersrechts: 34,7 -> 40,0 gelijkmatig) valt bij beide poten in r3 binnen de
# middenpixel. Welke poot Jordi bedoelt en wat "te recht" is, is dus niet uit de meting af te leiden: vragen.
# ---- 6. gelaat: varianten ----
# model: ondiepe U (natief x86-95, y102-105): twee donkere puntjes bovenaan (x86-87 en x94-95, y102-103) met een balkje
# eronder (x88-93, y104-105). In de sprite: puntjes x25 en x29 op y33, balkje x26-28 op y34.
basis=o.copy()
def gelaat(o,var):
    o=o.copy()
    if var=='A': return o                                      # A = model (r3): U
    for X in (25,29):                                          # B/C: de twee puntjes als ogen, 1x2 zwart zoals kleine Gen 3-ogen
        o[32,X]=1; o[33,X]=1
    if var=='C':
        for X in (26,27,28): o[34,X]=r3[34,25] if r3[34,25] in (9,10) else 10   # balkje weg (alleen ogen)
    return o
VAR={v:gelaat(basis,v) for v in 'ABC'}
o=VAR['B']
assert ((o!=r3)&BEV&~((np.arange(64)[:,None]>=32)&(np.arange(64)[:,None]<=34)&(np.arange(64)[None,:]>=24)&(np.arange(64)[None,:]<=30))).sum()==0, 'lijf/rechterpoot niet bevroren'
opslaan(o,PAL,RONDE+'/vileplume_r4.png')
for v in 'AC': opslaan(VAR[v],PAL,RONDE+'/vileplume_r4_gelaat%s.png'%v)
opslaan(kaal_o,PAL,RONDE+'/kaal.png')
# ---- telling ----
diff=o!=kaal_o; d3=o!=r3
Z={'anemonen':(np.arange(64)[:,None]<=31)&~KRATER,'krater':KRATER,'lijf+armen':(np.arange(64)[:,None]>=32)&(np.arange(64)[:,None]<=41),
   'poten':np.arange(64)[:,None]>=42}
for n,m in Z.items(): print('zone %-10s t.o.v. kaal %4d px | t.o.v. r3 %4d px'%(n,(diff&m).sum(),(d3&m).sum()))
print('mondjes %d px; gelaat B t.o.v. A: %d px, C t.o.v. A: %d px'%(MOND.sum(),(VAR['B']!=VAR['A']).sum(),(VAR['C']!=VAR['A']).sum()))
print('totaal t.o.v. kaal %d px, t.o.v. r3 %d px'%(diff.sum(),d3.sum()))
ch='.K0123abcdeGuomy'
for y in range(64): print('%2d '%y+''.join(ch[v] for v in o[y]))
if '--diag' in sys.argv:
    ch='.KVP'
    for y in range(32): print('%2d '%y+''.join('M' if MOND[y,x] else ('S' if STRAAL[y,x] else ch[ZONE[y,x]]) for x in range(64)))
    img=np.full((64,64,3),255,'uint8'); kl=[(255,0,0),(0,0,255),(0,170,0),(0,170,170),(200,0,200)]
    for Y,X in zip(*np.where(OWN>=0)):
        col=np.array(kl[OWN[Y,X]]); img[Y,X]=col if STRAAL[Y,X] else (col*0.3+255*0.7).astype(int)
        if MOND[Y,X]: img[Y,X]=(0,0,0)
    for i in range(5):
        for cm,ri,ru in KLONT[i]:
            p0=punt(i,cm,ri); p1=punt(i,cm,ru)
    Image.fromarray(img).resize((512,512),Image.NEAREST).save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/fabbb773-9d3c-5783-a635-6cbf1e7c7be6/scratchpad/diag4.png')
    for i in range(5): print(AN[i][0],[(round(np.degrees(cm)),round(ri,2),round(ru,2)) for cm,ri,ru in KLONT[i]],[round(x,2) for x in RC[i]])
