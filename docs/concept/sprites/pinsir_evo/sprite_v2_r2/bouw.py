# Pinsir-evolutie v2 r2: frontsprite uit model_v2_r4 (natief raster 91x78, pitch 10,24). Draaien vanuit docs/concept/sprites/pinsir_evo/:
#   python3 sprite_v2_r2/bouw.py
# Verschil met r1: r1 nam per spritepixel de MEERDERHEIDSKLASSE van de modelcellen -> dunne lijnen, glanzen en kleine tinten vielen weg.
# r2: (1) modellijnen worden apart als skelet verkleind (positie = modelpositie x 64/91) en blijven zo doorlopend 1 px;
#     (2) vlakken krijgen de GEMIDDELDE modelhelderheid van hun cellen zonder lijnen (gladde toonkaart), daarna per kleurgroep
#         gekwantiseerd in 3-4 tinten -> de lichte afschuining/donkere onderkant van het model blijft als vlak bestaan;
#     (3) silhouet = r1 (pixelgelijk, assert).
import sys, numpy as np
sys.path.insert(0,'sprite_v2'); sys.path.insert(0,'sprite_v2_r2')
from reductie import *            # a (natief rgb), L, K (klassen), BG, BLK, RED, CREAM, BROWN, EYE, FACE, kaart, X0, Y0, S
from scipy import ndimage as nd
from skimage.morphology import skeletonize
from collections import Counter
from PIL import Image
OUT='sprite_v2_r2/'
# gekozen instellingen (r2): python3 sprite_v2_r2/bouw.py A  of  ... B ; extra woorden (debug/ov/lab) blijven werken
STD=['A','6','0.2','x','14','15','12','5','2','ja','gem','16','86,110,136','zonder','5','4']
_extra=[w for w in sys.argv[1:] if w in ('debug','ov','lab','r2gezicht','r1gezicht') or w.endswith('.png')]
_pos=[w for w in sys.argv[1:] if w not in _extra]
if len(_pos)<=1: sys.argv=[sys.argv[0]]+[(_pos[0] if _pos else 'A')]+STD[1:]+_extra
VAR=sys.argv[1] if len(sys.argv)>1 else 'A'
N4=np.array([[0,1,0],[1,1,1],[0,1,0]]); N8=np.ones((3,3),bool)

# ---------- kaart natief -> sprite (zelfde als r1) ----------
cx,cy=kaart(0.3,0.3); OY=63-cy[88]
SX=cx; SY=cy+OY
r1=Image.open('sprite_v2/pinsir_evo_v2_r1.png'); R1=np.array(r1); SIL=R1>0
cells={}
for y in range(H):
    for x in range(W):
        if 0<=SX[x]<64 and 0<=SY[y]<64: cells.setdefault((SY[y],SX[x]),[]).append((y,x))

# ---------- 1. modellijnen (natief) ----------
OUTER=(K==1)&nd.binary_dilation(BG,np.ones((3,3)))
LIJNN=((K==1)&~OUTER)|(K==2)                       # zwart binnenin + donkerbruine lijntint
# Lijnkeuze = de lange modellijnen die r1 per zaadcel koos (kopschildrand, schouderkoepel, buikrand, armen/klauwen, knieen incl.
# kniecirkel, dij/staart, staartsegmenten, voetklauwen, rugplaatlijnen). Elke groep zwarte (Z) of donkerbruine (B) cellen = 1 lijn.
HOUD={
 'kopschildrand rechts (Z2)':(47,19),
 'rug: lijn onder de eerste rugstekels (Z6)':(57,29), 'rug: achterste plaatrand (Z14)':(76,40),
 'schouderkoepel boven (B22)':(51,38), 'schouderkoepel links (B38)':(47,48), 'schouderkoepel links-onder (Z20)':(50,46), 'schouderkoepel onder (Z23)':(56,49),
 'buik rechts + rechterarm/klauw + dijvoorkant (Z18)':(58,43), 'buik links boven (Z22)':(38,49), 'buik links onder (Z37)':(33,63), 'buik/dij onder (Z39)':(51,69),
 'linkerarm (Z30)':(26,56), 'linkerklauw vingers (Z34)':(23,59), 'linkerklauw (B55)':(18,58),
 'linkerknie boven (Z42)':(33,75), 'linkerknie (B69)':(35,70), 'linkerknie (B71)':(30,71), 'linkervoet teen (Z45)':(31,81),
 'rechterknie cirkel boven (B65)':(61,66), 'rechterknie cirkel (B73)':(61,71), 'rechterknie cirkel (Z41)':(65,74), 'rechterknie cirkel onder (Z44)':(57,76), 'rechterknie (B75)':(63,77),
 'dijvoorkant (B63)':(53,64), 'dij achterkant (B59)':(69,60), 'dij/staart grens (B64)':(75,65),
 'staartbasis boven (Z32)':(87,56), 'staartbasis (Z29)':(70,55), 'staartsegment (B57)':(74,58), 'staartsegment (B61)':(81,62), 'staartsegment (B67)':(86,68),
 'rechtervoet klauw (B77)':(58,82), 'rechtervoet klauw (B78)':(68,82),
}
labZ,_=nd.label((K==1)&~OUTER,N8); labB,_=nd.label(K==2,N8)
keep=np.zeros_like(LIJNN)
for naam,(x,y) in HOUD.items():
    l_=labZ if K[y,x]==1 else labB
    assert l_[y,x]>0,naam
    keep|=l_==l_[y,x]
keep|=FACE&LIJNN
# hand van de nabije arm (klauwen tegen de buik): het model scheidt klauwen en buik met korte bruine/zwarte lijnstukjes -> allemaal houden
HAND=np.zeros_like(BG); HAND[54:65,48:59]=True
keep|=HAND&((K==1)|(K==2))
# alle zwarte modellijnen (ook die tegen de achtergrond liggen: in de sprite liggen ze vaak binnenin), groepen >= 4 cellen
labA,nA=nd.label(K==1,N8); szA=nd.sum(np.ones_like(labA),labA,range(nA+1))
for i in range(1,nA+1):
    if szA[i]>=4: keep|=labA==i
yy,xx=np.mgrid[0:H,0:W]
RUGN=(xx>=50)&(yy>=28)&(yy<=60)&~((xx<=60)&(yy>=37))   # natieve rugzone (zonder schouderkoepel/arm)
LMIN=int(sys.argv[2]) if len(sys.argv)>2 else 6
# rugnaden van het model die >= LMIN cellen lang zijn (A: blijven; B: alleen om de grootste platen te meten)
lab,n=nd.label(LIJNN&RUGN,N8); sz=nd.sum(np.ones_like(lab),lab,range(n+1))
for i in range(1,n+1):
    if sz[i]>=LMIN: keep|=lab==i
SKEL=skeletonize(keep)|(keep&FACE&(K==1))
# primaire lijnen (vorm over vorm: lange zwarte modellijnen) -> donkerste lijntint; secundaire (plaatnaden, krassen) -> schaduwtint
PMIN=int(sys.argv[7]) if len(sys.argv)>7 else 12
PRIM=np.zeros_like(keep)
for i in range(1,nA+1):
    if szA[i]>=PMIN: PRIM|=labA==i             # gezicht: alle zwarte cellen houden

# ---------- 2. lijnvrije natieve kleur (lijncellen krijgen de buurkleur) ----------
F=a.astype(float).copy(); dicht=~(LIJNN|BG|OUTER|(K==1))
cls=np.zeros((H,W),int)          # kleurgroep: 1 bruin, 2 room, 3 rood, 4 oog
cls[BROWN]=1; cls[CREAM]=2; cls[RED]=3; cls[EYE]=4
todo=~dicht&~BG
while todo.any():
    acc=np.zeros((H,W,3)); cnt=np.zeros((H,W)); ccl=np.zeros((H,W,5))
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            s=np.roll(np.roll(dicht,dy,0),dx,1); acc+=np.roll(np.roll(F,dy,0),dx,1)*s[...,None]; cnt+=s
            c=np.roll(np.roll(cls,dy,0),dx,1)
            for k in range(1,5): ccl[...,k]+=(c==k)&s
    nw=todo&(cnt>0)
    if not nw.any(): break
    F[nw]=acc[nw]/cnt[nw,None]; cls[nw]=ccl[nw].argmax(1); dicht|=nw; todo&=~nw
LF=0.299*F[...,0]+0.587*F[...,1]+0.114*F[...,2]

# ---------- 3. per spritepixel: kleurgroep (meerderheid) + gemiddelde helderheid (toonkaart) ----------
grp=np.zeros((64,64),int); lum=np.zeros((64,64)); lijn=np.zeros((64,64),bool); zw=np.zeros((64,64),bool); prim=np.zeros((64,64),bool); lijnU=np.zeros((64,64),bool)
for (sy,sx),cl in cells.items():
    fig=[(y,x) for y,x in cl if not BG[y,x]]
    if not fig: continue
    ys,xs=zip(*fig)
    c=Counter(cls[ys,xs]).most_common(1)[0][0]
    grp[sy,sx]=c if c>0 else 1
    lum[sy,sx]=np.mean([LF[y,x] for y,x in fig if cls[y,x]==grp[sy,sx]] or [LF[ys,xs].mean()])
    if any(SKEL[y,x] and PRIM[y,x] for y,x in fig): prim[sy,sx]=True
    if any(SKEL[y,x] and not OUTER[y,x] for y,x in fig): lijn[sy,sx]=True
    elif any(SKEL[y,x] for y,x in fig): lijnU[sy,sx]=True
    if any(SKEL[y,x] and K[y,x]==1 and FACE[y,x] for y,x in fig): zw[sy,sx]=True
# modelbuitenlijn die in de sprite binnenin valt (bijv. buikrand naast het gat bij de arm) telt als binnenlijn,
# maar niet als hij tegen de spritebuitenlijn ligt (die is er al)
RAND0=SIL&~nd.binary_erosion(SIL,N4,border_value=0)
lijn|=lijnU&~nd.binary_dilation(RAND0,N4)
lijn&=SIL
# lijnen 1 px dik: skelet in spriteruimte (alleen buiten het gezicht; gezicht = model)
GEZ=np.zeros((64,64),bool); GEZ[19:34,12:25]=True
lijn=(skeletonize(lijn&~GEZ)|(lijn&GEZ))
SEC=int(sys.argv[9]) if len(sys.argv)>9 else 2
LKORT=int(sys.argv[8]) if len(sys.argv)>8 else 3
_l,_n=nd.label(lijn&~GEZ&~nd.binary_dilation(RAND0,N4),N8)
for _i in range(1,_n+1):
    _m=_l==_i
    # een stukje dat de buitenlijn raakt telt mee als aanhangsel van de buitenlijn
    if _m.sum()<LKORT and not (nd.binary_dilation(_m,N8)&lijn&~_m).any(): lijn&=~_m
# (debugbestanden niet meer opgeslagen)

# ---------- 4. buitenlijn: r1 (kleur per pixel uit het model) ----------
RAND=SIL&~nd.binary_erosion(SIL,N4,border_value=0)
# r1-index -> r2-index voor de buitenlijn: 1 zwart, 2 bruine lijntint, 8 donkerrood
# ---------- 5. vlakken: per vorm (vlak tussen de modellijnen) ----------
# basistint = gemiddelde modelhelderheid van de vorm (grote vormen: de gladde modeltoonkaart, zodat bv. de lichte bovenafschuining
# van het kopschild blijft); daarna Gen 3-volume per vorm: schaduwkant rechtsonder 1 stap donkerder (grote vormen 2 px),
# lichtkant linksboven 1 stap lichter. Geen nieuwe vormen: alleen de tint binnen de modelvorm.
# buiklijnen (tan op room in het model): eigen lijnsoort
BUIKN=nd.binary_closing(CREAM&~EYE,np.ones((5,5)))&(xx>=30)&(yy>=44)
crn=sum(np.roll(CREAM,sh,ax) for sh,ax in ((1,0),(-1,0),(1,1),(-1,1)))
BL=BUIKN&BROWN&(crn>=2)
buikl=np.zeros((64,64),bool)
for (sy,sx),cl in cells.items():
    if any(BL[y,x] for y,x in cl): buikl[sy,sx]=True
buikl&=SIL&~lijn&~RAND&(grp==2)
buikl=skeletonize(buikl)
# ---- lijnfilter per onderdeel: alleen modellijnen die op een onderdeelgrens liggen (vorm over vorm), plus kniecirkel, gezicht,
#      kaken en (A) de rugnaden. Krassen midden in een vlak vervallen (r5/r6-les: korte lijnstukjes = druk).
from onderdelen import kaart as delenkaart
DEEL=delenkaart(); DEEL[~SIL]=''
DG=np.where(SIL&(DEEL==''),np.where(grp==2,'buik',np.where(grp==3,'kaak','rest')),DEEL)
GRENS=np.zeros((64,64),bool)
for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)):
    sh=np.roll(np.roll(DG,dy,0),dx,1); GRENS|=(sh!=DG)
GRENS=nd.binary_dilation(GRENS,N4)&SIL
LFILT=sys.argv[10] if len(sys.argv)>10 else 'ja'
if LFILT=='ja':
    vrij=GRENS|GEZ|(DEEL=='knie')|nd.binary_dilation(DEEL=='knie',N8)|(grp==3)|(DEEL=='staart')
    vrij|=(DEEL=='rug')
    weg=lijn&~vrij
    lijn&=~weg
# kniecirkel als doorlopende ring op de gemeten modelplek (natief: boog rij 71 kol 59-63, links kol 56-57, rechts kol 65, onder rij 78 kol 59-62)
KNIERING=[(38,51),(39,51),(40,51),(41,51),(37,52),(42,52),(36,53),(42,53),(36,54),(42,54),(37,55),(41,55),(38,56),(39,56),(40,56)]
KR=np.zeros((64,64),bool)
for x,y in KNIERING: KR[y,x]=True
lijn&=~((DEEL=='knie')&~KR)      # binnen de knie alleen de ring
lijn|=KR&SIL&~RAND0
vul=SIL&~RAND&~lijn&~zw&~buikl
# ---- variant B: de NPL grootste rugplaten van het model (vlakken tussen de modelnaden, gemeten in de sprite) groeien tot ze de
#      hele rug vullen; tussen de platen een 1-px naad; de kleine plaatjes en krassen vervallen.
PLAAT=np.zeros((64,64),int)
if VAR=='B':
    NPL=int(sys.argv[16]) if len(sys.argv)>16 else 4
    RUGM=(DEEL=='rug')&SIL&~RAND
    rl,rn=nd.label(RUGM&~lijn,N4); rs=nd.sum(np.ones_like(rl),rl,range(rn+1)); rs[0]=0
    groot=np.argsort(rs)[::-1][:NPL]
    mk=np.zeros((64,64),int)
    for k_,i in enumerate(groot): mk[rl==i]=k_+1
    PLAATMAAT=[(int(rs[i]),tuple(np.round(np.argwhere(rl==i).mean(0)[::-1],1))) for i in groot]
    _,(iy,ix)=nd.distance_transform_edt(mk==0,return_indices=True)
    PLAAT=np.where(RUGM,mk[iy,ix],0)
    naad=np.zeros((64,64),bool)
    naad[:-1]|=(PLAAT[:-1]!=PLAAT[1:])&(PLAAT[1:]>0)&(PLAAT[:-1]>0)
    naad[:,:-1]|=(PLAAT[:,:-1]!=PLAAT[:,1:])&(PLAAT[:,1:]>0)&(PLAAT[:,:-1]>0)
    lijn&=~RUGM; lijn|=naad
    vul=SIL&~RAND&~lijn&~zw&~buikl
# ---- volume per onderdeel: bolle vorm uit de afstand tot de onderdeelrand (licht linksboven), gemengd met de modelhelderheid ----
LD=np.array([-0.55,-0.7,0.65]); LD/=np.linalg.norm(LD)
ALFA=float(sys.argv[3]) if len(sys.argv)>3 else 0.6
def bol(shape):
    d=nd.distance_transform_edt(np.pad(shape,1))[1:-1,1:-1]
    h=np.sqrt(d); h=nd.gaussian_filter(h,0.8)
    gy,gx=np.gradient(h); n=np.dstack([-gx,-gy,np.ones_like(h)*0.9]); n/=np.linalg.norm(n,axis=2,keepdims=True)
    return n@LD
def toon(M,shape,ladder,q=(0.30,0.72,0.93),alfa=None):
    """M = te kleuren pixels, shape = vorm voor de bolling. ladder = [schaduw, midden, licht, hooglicht]."""
    if M.sum()==0: return
    I=bol(shape)[M]; I=(I-I.mean())/(I.std()+1e-6)
    z=LUMG[M]; z=(z-z.mean())/(z.std()+1e-6)
    sc=I+(ALFA if alfa is None else alfa)*z
    qs=np.quantile(sc,q)
    t=np.searchsorted(qs,sc)
    if M.sum()<40 or len(ladder)<4: t=np.minimum(t,2)
    idx[M]=np.array(ladder)[np.minimum(t,len(ladder)-1)]
LUMG=nd.gaussian_filter(lum,0.7)
idx=np.zeros((64,64),int)
VER={'verre_arm','verre_been'}
for P in ['kopschild','schouderkoepel','schouder','nabije_arm','verre_arm','nabije_dij','knie','nabije_voet','verre_been','staart']:
    shape=(DEEL==P)&SIL; M=shape&vul&(grp==1)
    if P in VER: toon(M,shape,[3,3,4,5],q=(0.25,0.45,0.85))
    else: toon(M,shape,[3,4,5,6])
# rug: A = elke plaat tussen de modelnaden eigen bolling; B volgt later
RUGM=(DEEL=='rug')&SIL
platen,npl=nd.label(RUGM&vul&(grp==1),N4)
for i in range(1,npl+1):
    m=platen==i
    if m.sum()<4: continue
    toon(m,m,[3,4,5,6],q=(0.34,0.70,0.94),alfa=0.3)
klein=RUGM&vul&(grp==1)&(idx==0)
# overige bruine pixels (gezicht/hals tussen de kaken, kleine plaatjes): modelhelderheid -> tint
rest=vul&(grp==1)&(idx==0)
idx[rest]=np.array([3,4,5,6])[np.searchsorted([92,112,136],lum[rest])]
# buik (room): een bolle vorm, licht linksboven
BU=SIL&(grp==2)&~GEZ
toon(BU&vul,BU|buikl,[6,7,8],q=(0.30,0.62))
idx[vul&(grp==2)&(idx==0)]=8
# kaken: per kaak een bolle vorm
kk,nk=nd.label(SIL&(grp==3),N4)
for i in range(1,nk+1):
    m=kk==i; toon(m&vul,m,[10,11,12],q=(0.33,0.70),alfa=0.8)
# ---- FILL 'gem' (standaard): vlakgemiddelde van het model (SPRITE_KERN: "verkleinen met vlakgemiddelde + dichtstbijzijnde kleur"),
#      exact over de celoverlap, lijnen INCLUSIEF (zo blijven de zachte modelranden van platen, kniecirkel, koepel als donkere toon).
#      Per onderdeel een lichte bolling erbij (BETA) zodat elke vorm licht linksboven/schaduw rechtsonder krijgt.
FILL=sys.argv[11] if len(sys.argv)>11 else 'gem'
def wmat(n,o0,off):
    Wm=np.zeros((64,n))
    for i in range(n):
        a0=(i-o0)*S+0.3+off; a1=a0+S
        for j in range(int(np.floor(a0)),int(np.floor(a1))+1):
            if 0<=j<64: Wm[j,i]=max(0,min(a1,j+1)-max(a0,j))
    return Wm
Wx=wmat(W,X0,0); Wy=wmat(H,Y0,OY)
SRC=F if (len(sys.argv)>14 and sys.argv[14]=='zonder') else a.astype(float)
AV=np.einsum('jy,yxc,ix->jic',Wy,SRC,Wx)/(Wy.sum(1)[:,None,None]*Wx.sum(1)[None,:,None]+1e-9)
LAV=0.299*AV[...,0]+0.587*AV[...,1]+0.114*AV[...,2]
BETA=float(sys.argv[12]) if len(sys.argv)>12 else 8.0
TBR=[float(v) for v in (sys.argv[13] if len(sys.argv)>13 else '88,112,138').split(',')]
OFFS={'kopschild':10,'nabije_arm':12,'schouderkoepel':14,'nabije_dij':6,'knie':10,'rug':-4,'verre_arm':-6,'verre_been':-6}
if FILL=='gem':
    SC=LAV.copy()
    for P in set(DEEL[SIL])-{''}:
        sh=(DEEL==P)&SIL
        if sh.sum()<10: continue
        B=bol(sh); B=(B-B[sh].mean())/(B[sh].std()+1e-6); SC[sh]+=BETA*B[sh]+OFFS.get(P,0)
    m_=vul&(grp==1); idx[m_]=np.array([3,4,5,6])[np.searchsorted(TBR,SC[m_])]
    m_=vul&(grp==2); idx[m_]=np.array([6,7,8])[np.searchsorted([190,212],SC[m_])]
    # kaken: per kaak de bolling + modeltoon, verdeeld als Gen 3 (±30 % schaduw, ±40 % midden, ±30 % licht)
    kk,nk=nd.label(SIL&(grp==3),N4)
    for i in range(1,nk+1):
        km=(kk==i); m_=km&vul
        if m_.sum()<4: idx[m_]=11; continue
        B=bol(km); B=(B-B[m_].mean())/(B[m_].std()+1e-6)
        z=(LAV[m_]-LAV[m_].mean())/(LAV[m_].std()+1e-6)
        sc=B[m_]+0.7*z; qs=np.quantile(sc,(0.30,0.70))
        idx[m_]=np.array([10,11,12])[np.searchsorted(qs,sc)]
if VAR=='B':     # elke plaat bol: licht linksboven, schaduw rechtsonder, basistint = gemiddelde modeltoon van de plaat
    for k_ in range(1,PLAAT.max()+1):
        pm=(PLAAT==k_)&vul&(grp==1)
        if not pm.any(): continue
        B=bol((PLAAT==k_)); B=(B-B[pm].mean())/(B[pm].std()+1e-6)
        sc=LAV[pm].mean()+22*B[pm]
        idx[pm]=np.array([3,4,5,6])[np.searchsorted(TBR,sc)]
# schaduwsikkel aan de schaduwkant van de vorm (Gen 3): pixel waarvan de buur onder/rechts buiten het onderdeel ligt -> 1 stap donkerder
RANDSCH={'kopschild':('o',),'knie':('o','r'),'schouderkoepel':('o','r'),'nabije_arm':('o','r'),'nabije_dij':('o',),'staart':('o',)}
LADDER=[3,4,5,6]
for P,dirs in RANDSCH.items():
    sh=(DEEL==P)&SIL; m_=sh&vul&(grp==1)
    buiten=~sh|lijn|RAND
    e=np.zeros_like(sh)
    if 'o' in dirs: e[:-1]|=buiten[1:]
    if 'r' in dirs: e[:,:-1]|=buiten[:,1:]
    e&=m_
    for y,x in zip(*np.where(e)):
        if idx[y,x] in LADDER: idx[y,x]=LADDER[max(0,LADDER.index(idx[y,x])-1)]
idx[vul&(grp==4)]=13
idx[buikl]=5      # buiklijnen: model tan L 127 -> bruin licht
# lijnen: kleur naar het onderdeel eromheen (donkerste tint van dat onderdeel), zwart alleen in het gezicht waar het model zwart is
for y,x in zip(*np.where(lijn&~zw)):
    nb=[grp[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if 0<=yy<64 and 0<=xx<64 and vul[yy,xx]]
    g_=Counter(nb).most_common(1)[0][0] if nb else 1
    gs=set(nb)
    if gs<= {3}: idx[y,x]=9                              # lijn binnen een kaak
    elif gs<={1} and not prim[y,x]: idx[y,x]=SEC         # plaatnaad/kras binnen bruin
    else: idx[y,x]=2                                     # vorm over vorm (ook buikrand)
idx[zw]=1
R1MAP={1:1,2:2,8:9}
for y,x in zip(*np.where(RAND)): idx[y,x]=R1MAP.get(int(R1[y,x]),1)
# ---------- 5a. handen: klauwen per spritepixel uit de modelcellen (room = klauw, zwart = lijn ertussen), zoals het model ----------
inv={}
for y in range(H):
    for x in range(W): inv.setdefault((SY[y],SX[x]),[]).append((y,x))
def handzone(x0,y0,x1,y1,schaduwrechts=True):
    for sy in range(y0,y1+1):
        for sx in range(x0,x1+1):
            if not SIL[sy,sx] or RAND[sy,sx]: continue
            cl=inv.get((sy,sx),[]); nk=sum(K[y,x]==1 for y,x in cl); nc=sum(K[y,x] in (7,8) for y,x in cl)
            if nc and nc>=nk: idx[sy,sx]=8
            elif nk: idx[sy,sx]=2
    # klauwschaduw: roompixel met lijn/rand rechts of onder -> roomschaduw
    for sy in range(y0,y1+1):
        for sx in range(x0,x1+1):
            if idx[sy,sx]==8 and (idx[sy+1,sx] in (1,2) or idx[sy,sx+1] in (1,2)): idx[sy,sx]=7
HANDN=(32,40,37,46); handzone(*HANDN)
HANDV=(8,41,13,47); handzone(*HANDV)
HZ=np.zeros((64,64),bool); HZ[40:47,32:38]=True; HZ[41:48,8:14]=True
vul&=~HZ
# ---------- 5a2. stekels (rug, kopschild, staart): binnenpixels van uitsteeksels; flanken zoals het model (lichte linkerflank, donkere rechterflank) ----------
open3=nd.binary_opening(SIL,np.ones((3,3)))
STEK=SIL&~open3&~RAND&((grp==1))&~GEZ
STEK|=nd.binary_dilation(SIL&~open3,N4)&SIL&~RAND&(grp==1)&~GEZ&~open3
STEKZONE=np.zeros((64,64),bool); STEKZONE[8:15,:]=True; STEKZONE[15:46,33:]=True
STEK&=STEKZONE
for y,x in zip(*np.where(STEK)):
    l=not SIL[y,x-1] or RAND[y,x-1]; r=not SIL[y,x+1] or RAND[y,x+1]
    if l and r: idx[y,x]=5
    elif l: idx[y,x]=6 if y<15 else 5
    elif r: idx[y,x]=3
vul&=~STEK
# ---------- 5b. gezicht = r1 (ogen, mond, tanden kwamen daar cel voor cel uit het model; Jordi had er geen klacht over) ----------
R1IDX={1:1,2:2,3:3,4:4,5:5,6:6,7:8,8:9,9:10,10:11,11:13}
FACEBOX=np.zeros((64,64),bool); FACEBOX[20:34,11:25]=True
FACEBOX&=SIL&~RAND&(grp!=3)&(R1>0)
if 'r2gezicht' in sys.argv: FACEBOX[:]=False
FACEBOX&=~((R1==8)|(R1==9)|(R1==10))         # kaakpixels in het vak blijven r2
if 'r1gezicht' in sys.argv:
    for y,x in zip(*np.where(FACEBOX)): idx[y,x]=R1IDX[int(R1[y,x])]
else:
    # r2: gezicht per spritepixel uit de modelcellen, maar met de HELFT-regel i.p.v. 'een lijncel = lijn' (r1 maakte zo van de
    # 1 cel brede mondspleet een zwart blok van 4-5 px): oog als er oogcellen zijn; zwart als >= de helft van de cellen zwart is;
    # room (tanden) als >= de helft room is; anders bruin naar de gemiddelde modeltoon van de niet-zwarte cellen.
    for y,x in zip(*np.where(FACEBOX)):
        cl=inv.get((y,x),[]); n_=len(cl)
        ne=sum(EYE[c] for c in cl); nk=sum(K[c]==1 for c in cl); nc=sum(K[c] in (7,8) for c in cl)
        if ne and ne>=nk: idx[y,x]=13
        elif nk*2>=n_ and nk: idx[y,x]=1
        elif nc*2>=n_: idx[y,x]=8
        else:
            vs=[LF[c] for c in cl if K[c]!=1]
            idx[y,x]=[3,4,5,6][int(np.searchsorted([86,110,136],np.mean(vs)))] if vs else 2
    # tandschaduw: roompixel met zwart rechts of onder -> roomschaduw
    for y,x in zip(*np.where(FACEBOX&(idx==8))):
        if idx[y+1,x]==1 or idx[y,x+1]==1: idx[y,x]=7
vul&=~FACEBOX
# ---------- 6. opschonen: tintvlakjes < 3 px nemen de buurtint van dezelfde groep (gezicht uitgezonderd) ----------
GROEP={3:"b",4:"b",5:"b",6:"b",7:"c",8:"c",10:'r',11:'r',12:'r'}
MINB=int(sys.argv[15]) if len(sys.argv)>15 else 3
def opschonen(I,minpx=3):
    for _ in range(5):
        ch=0
        for k in GROEP:
            l_,n_=nd.label((I==k)&vul,N4)
            for j in range(1,n_+1):
                m=l_==j
                if m.sum()>=(MINB if GROEP[k]=='b' else minpx) or (m&GEZ).any(): continue
                ring=nd.binary_dilation(m,N4)&~m
                ks=[v for v in I[ring&vul] if GROEP.get(v)==GROEP[k]]
                if ks: I[m]=Counter(ks).most_common(1)[0][0]; ch+=1
        if not ch: break
    return I
idx=opschonen(idx)
PAL=[(152,208,160),(16,12,10),(46,32,22),(88,66,48),(124,100,76),(164,138,106),(204,182,144),
     (228,214,178),(248,242,220),(64,20,22),(104,38,36),(150,66,56),(196,112,92),(248,236,160)]
def opslaan(I,naam):
    im=Image.fromarray(I.astype('uint8'),'P'); pl=[c for t in PAL for c in t]; pl+=[0]*(768-len(pl)); im.putpalette(pl); im.save(naam,transparency=0)
assert ((idx>0)==SIL).all()
if 'lab' in sys.argv:
    from PIL import ImageDraw
    Z=14; labs,nl=nd.label(vul,N4); rng=np.random.RandomState(1); cols=rng.randint(90,255,(nl+1,3)); cols[0]=(255,255,255)
    im=cols[labs].astype('uint8'); im[lijn|zw|buikl]=(60,60,60); im[RAND]=(0,0,0)
    big=Image.fromarray(im).resize((64*Z,64*Z),0); d=ImageDraw.Draw(big)
    for i in range(1,nl+1):
        y_,x_=np.where(labs==i); k=len(y_)//2; d.text((x_[k]*Z+2,y_[k]*Z+1),str(len(y_)),fill=(0,0,0))
    for t in range(0,64,5): d.text((t*Z+2,2),str(t),fill=(255,0,0)); d.text((2,t*Z+2),str(t),fill=(255,0,0))
    big.save(sys.argv[-1])
if 'ov' in sys.argv:
    from vergelijk import modelstuk
    Z=10; m=np.array(modelstuk(0,0,64,64,Z)).astype(float); m=(m*0.55+255*0.45).astype('uint8')
    for y,x in zip(*np.where(lijn|buikl|zw|RAND)):
        c=(0,0,255) if RAND[y,x] else ((255,0,0) if prim[y,x] else ((0,170,0) if buikl[y,x] else (255,150,0)))
        m[y*Z+3:y*Z+7,x*Z+3:x*Z+7]=c
    Image.fromarray(m).crop((0,60,640,640)).save(sys.argv[-1])
opslaan(idx,OUT+'pinsir_evo_v2_r2_%s.png'%VAR)
if 'debug' in sys.argv:
    im=np.zeros((64,64,3),'uint8')+255
    v=np.clip(lum,0,255).astype('uint8')
    im[SIL]=np.dstack([v,v,v])[SIL]
    im[grp==3]=np.dstack([v,v//2,v//2])[grp==3]
    im[lijn]=(255,0,0); im[zw]=(0,0,255)
    ed=SIL&~nd.binary_erosion(SIL,N4,border_value=0); im[ed]=(0,160,0)
    Image.fromarray(im).resize((768,768),Image.NEAREST).save(sys.argv[-1])
