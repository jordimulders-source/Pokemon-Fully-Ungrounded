# Pinsir-evolutie r7: basis = r6 (segmentatie uit de modellijnen, doorlopende 1-px lijnen, buitenrand zwart, geen zwart
# binnenin). Jordi bij r6 (naast het model, letterlijk): "de rechterkaak is aan de bovenkant een beetje afgekapt tov het model,
# desnoods overlapt het de mond maar een klein beetje. links loopt weer net te ver door tov het model, daar zou je iets meer de
# aansluiting moeten kunnen zien. De ogen mogen iets meer zoals het model ook, niet intimiderend genoeg. Het hoofd is kaal, maar
# dat is veelal kleurgebruik en afwezigheid van stekels, de vraag is alleen of de stekels kunnen. Het vleugelpatroon is niet goed
# qua tinten. De rechterschouder is niet rond genoeg en het rechterbeen is ook een beetje een blurry mess, de staart is een
# stopmpje. Verder is het kleurgebruik en de tinten zijn gewoon niet goed, bijna overal slechts 2 kleurtinten maar"
# en over het dekschild: "vleugelpatroon van model is misschien wat te complex, dus kijk vooral naar hoe andere sprites dat
# doen, incl mega pinsir".
# Wat r7 anders doet dan r6:
#  A. KAKEN + OGEN (tabel KOP, gemeten op het model, rooster 16x/40x): rechterkaak een rij hoger en 1 px over de mondrand,
#     linkerkaak eindigt 1 px eerder met een donkere aansluiting; ogen als in het model: zwarte wenkbrauwband (rij 27) en lage
#     witte spleten (nabij oog x21-23 rij 28, ver oog x16 rij 27-28).
#  B. VULLING: per vlak een volle tintreeks (3-4 tinten) via rangorde van een lichtscore = modeltoon binnen het vlak
#     (gladgestreken, z-score) + vormlicht (bol: linksboven licht, rechtsonder schaduw + sikkel aan de rand rechtsonder).
#  C. STAART: staartsegmenten 209/206/213 samen met 193 (geen verticale strepen meer); de lichte bovenband van het model
#     loopt zo door tot de opgekrulde punt.
#  D. DEKSCHILD naar de aanpak van Mega Pinsir / Shuckle / Crustle: oker in 3 tinten met licht en schaduw per vorm, de
#     tekening als een paar grote vlakke donkere banden (gladgestreken modeltekening, drempel, >= 4 px), geen 1-px streepjes.
#     Palet: de aparte kaaklijntint vervalt (kaak gebruikt de schildlijntint, bijna gelijk), die plek wordt licht oker.
#  E. KOPSTEKELS (variant): de stekels van het model op de rand van het kopschild 3 px breed aan de basis met een lichte
#     voorkant; kegeltjes op het kopschild zelf (model) als licht/donker paar. pinsir_evo_r7.png = met, _zonder_stekels.png = zonder.
# Bouwen: cd pinsir_evo && python3 sprite_r7/bouw.py [raster|detail]
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from model import klassen
from PIL import Image; from scipy import ndimage
UIT='sprite_r7'
R6=np.asarray(Image.open('sprite_r6/pinsir_evo_r6.png')).astype(int)
H=W=64; yy,xx=np.mgrid[:H,:W]
PAL=[(120,200,160),(18,14,14),
     (40,32,28),                                            # 2 lijf lijn (selout)                33
     (66,54,46),(104,88,72),(148,128,102),(198,176,142),    # 3-6 lijf schaduw 55, midden 88, licht 126, glans 172 (donkerder dan r6, zoals het model)
     (204,158,106),                                         # 7 dekschild licht 156 (was kaaklijn; model licht 184,143,105)
     (118,52,38),(162,84,58),(206,130,94),                  # 8-10 kaak donker 69, midden 101, licht 143
     (66,36,18),(88,50,22),(124,82,46),(162,116,72),        # 11 lijn schild+kaak 40, 12 tekening 53, 13 schaduw 84, 14 midden 117 (model 139,100,69 / 77,46,22)
     (236,222,206)]                                         # 15 oog/tand crème
CH='.KL2345opqrsvwxT'                                       # tekens in raster/tabellen (o = licht oker 7)
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def nb(arr,Y,X,nbs=N4,fill=0):
    return [arr[Y+dy,X+dx] if 0<=Y+dy<H and 0<=X+dx<W else fill for dy,dx in nbs]
# ---------- basis uit r6 (kaak-lijn 7 -> 11) ----------
B=R6.copy(); B[R6==7]=11
KAAKM=np.isin(R6,[7,8,9,10])
# ---------- A. kaken en ogen (alleen deze pixels; assert op de r6-waarde) ----------
R6CH='.KL2345pqrsuvwxT'                                     # r6-tekens (p = kaaklijn)
def zet(Y,X,oud,nieuw,kaak=None):
    assert R6CH[R6[Y,X]]==oud,(Y,X,R6CH[R6[Y,X]],oud)
    B[Y,X]={'p':11,'q':8,'r':9,'s':10}.get(nieuw,None) if nieuw in 'pqrs' else CH.index(nieuw)
    if kaak is not None: KAAKM[Y,X]=kaak
KOP=[ # rechterkaak (in beeld): top een rij hoger (rij 29) en afgerond (hoekjes kaaklijn x25 rij 28, x26 rij 29-30);
     # 1 px over de mondrand: x22 wordt kaak, x21 (gezichtsrand) wordt de zwarte scheiding tegen de tanden
     (28,24,'4','K',False),(28,25,'3','p',True),
     (29,22,'3','K',False),(29,23,'L','s',True),(29,24,'L','s',True),(29,25,'L','r',True),(29,26,'2','p',True),
     (30,21,'3','K',False),(30,22,'K','s',True),(30,26,'L','p',True),
     (31,21,'3','K',False),(31,22,'K','s',True),
     (32,21,'3','K',False),(32,22,'K','r',True),
     (33,21,'3','K',False),(33,22,'K','r',True),
     # linkerkaak: eindigt bij x14 (donker) met de kaaklijn op x15; daarna de gezichtsplaat (aansluiting zichtbaar)
     (28,14,'r','q',True),(28,15,'T','K',False),
     (29,14,'r','q',True),(29,15,'q','p',True),
     (30,15,'q','p',True),
     (31,15,'q','p',True),
     # ogen (model): zwarte wenkbrauwband rij 27 (tussen de ogen donkere lijntint), lage witte spleten;
     # ver oog verticaal x16 rij 27-28, nabij oog x21-23 rij 28
     (27,15,'T','K',False),(27,18,'2','L',False),(27,19,'2','L',False),(27,20,'2','L',False),
     (27,22,'T','K',False),(27,23,'T','K',False),(27,24,'T','K',False),
     (28,16,'K','T',False),(28,22,'K','T',False)]
for Y,X,oud,nieuw,kaak in KOP: zet(Y,X,oud,nieuw,kaak)
SIL=B>0
GEZICHT=(xx>=14)&(xx<=25)&(yy>=26)&(yy<=35)                 # ogen + mond: uit B, niet herberekend
VAST=GEZICHT|KAAKM
for Y,X in zip(*np.where(B==1)):                            # zwarte kaakomlijning (aan de achtergrond / links) hoort bij de kaak
    n8=nb(B,Y,X,N8)
    if any(KAAKM[Y+dy,X+dx] for dy,dx in N8 if 0<=Y+dy<H and 0<=X+dx<W) and (0 in n8 or X<=13): VAST[Y,X]=True
# ---------- 1. segmentatie op modelresolutie (r6) ----------
a,c,fg=klassen(); L=a.mean(2)
LIJN=fg&(L<22)
lab,n=ndimage.label(fg&~LIJN)
sz=ndimage.sum(np.ones_like(L),lab,range(n+1)); sz[0]=0
groot=sz>=600; groot[0]=False
idx=ndimage.distance_transform_edt(~groot[lab],return_indices=True)[1]
LAB=lab[idx[0],idx[1]]*fg
VLAKKEN={12:('kopschild',9),1:('rug',4),2:('rug',4),7:('rug',4),24:('rug',4),39:('rug',4),
         46:('kop',10),
         50:('romp',5),55:('romp',5),60:('romp',5),92:('romp',5),99:('romp',5),179:('romp',5),
         69:('arm',8),87:('arm',8),135:('arm',8),247:('arm',8),275:('arm',8),297:('arm',8),
         159:('been',7),237:('been',7),300:('been',7),114:('been',7),
         35:('schild',7.5),
         185:('been_ver',5.5),217:('been_ver',5.5),243:('been_ver',5.5),
         100:('arm_ver',5.6),107:('arm_ver',5.6),221:('arm_ver',5.6),252:('arm_ver',5.6),
         193:('staart',3),209:('staart',3),206:('staart',3),213:('staart',3),166:('staart',3),169:('staart',3)}
grote=set(np.where(groot)[0]); assert grote==set(VLAKKEN)
MED={v:float(np.median(L[(lab==v)])) for v in VLAKKEN}
# r6: nekstrook 60 bij kraag 55. r7: staartsegmenten 209/206/213 bij 193 (C), punt 166/169 blijft eigen vlak
ALIAS={60:55,209:193,206:193,213:193,166:193}
for k,v in ALIAS.items(): LAB[LAB==k]=v
MED[193]=float(np.median(L[np.isin(lab,[193,209,206,213,166])]))
SCHILDM=np.isin(c,(9,10,11)); VLEK=c==9
CEL=974/64; MX0,MY0=31,134; DY=13
def cel(X,Y,k=0.0):
    ya,yb=MY0+(Y-DY)*CEL,MY0+(Y-DY+1)*CEL; xa,xb=MX0+X*CEL,MX0+(X+1)*CEL
    ya,yb,xa,xb=ya+k*CEL,yb-k*CEL,xa+k*CEL,xb-k*CEL
    return slice(max(int(round(ya)),0),max(int(round(yb)),0)),slice(max(int(round(xa)),0),max(int(round(xb)),0))
SL=np.zeros((H,W),int); MT=np.full((H,W),np.nan); ZW=np.zeros((H,W)); VL=np.zeros((H,W))
for Y in range(H):
    for X in range(W):
        s=cel(X,Y); f=fg[s]; li=LIJN[s]
        if f.size==0: continue
        ZW[Y,X]=li.mean()
        sm=cel(X,Y,0.2); l=LAB[sm]; k=l[fg[sm]&~LIJN[sm]]
        if k.size==0: k=LAB[s][f&~li]
        if k.size==0: k=LAB[s][f]
        if k.size: SL[Y,X]=np.bincount(k).argmax()
        if (f&~li).sum()>=6: MT[Y,X]=L[s][f&~li].mean()
        ms=f&SCHILDM[s]
        VL[Y,X]=VLEK[s][ms].mean() if ms.any() else 0
m=(SL>0)&SIL
ii=ndimage.distance_transform_edt(~m,return_indices=True)[1]
SL=np.where(SIL,SL[ii[0],ii[1]],0)
DEEL=np.vectorize(lambda v: VLAKKEN[v][0] if v in VLAKKEN else '')(SL)
MATR=np.where(DEEL=='schild','schild','lijf')
VER=np.isin(DEEL,['arm_ver','been_ver'])
# ---------- 2. lijnen (r6) ----------
paren={}
for Y,X in zip(*np.where(SIL)):
    for dy,dx in ((0,1),(1,0)):
        Y2,X2=Y+dy,X+dx
        if Y2<H and X2<W and SIL[Y2,X2] and SL[Y2,X2]!=SL[Y,X]:
            k=tuple(sorted((SL[Y,X],SL[Y2,X2]))); paren.setdefault(k,[]).append(((Y,X),(Y2,X2)))
lijn=np.zeros((H,W),bool); nlijnen=0
for (A_,B_),ps in paren.items():
    if len(ps)<3: continue
    dA,dB=VLAKKEN.get(A_,(0,0))[1],VLAKKEN.get(B_,(0,0))[1]
    if dA!=dB: kant=A_ if dA<dB else B_
    else:
        za=sum(ZW[p if SL[p]==A_ else q] for p,q in ps); zb=sum(ZW[q if SL[q]==B_ else p] for p,q in ps)
        kant=A_ if za>=zb else B_
    for p,q in ps: lijn[p if SL[p]==kant else q]=True
    nlijnen+=1
from skimage.morphology import skeletonize, thin
grens=np.zeros(L.shape,bool)
grens[:,1:]|=LAB[:,1:]!=LAB[:,:-1]; grens[1:,:]|=LAB[1:,:]!=LAB[:-1,:]
dgr=ndimage.distance_transform_edt(~grens)
sk=skeletonize(LIJN)&(dgr>=5)
lb,nn=ndimage.label(sk,structure=np.ones((3,3)))
szs=ndimage.sum(sk,lb,range(nn+1))
skl=np.isin(lb,np.where(szs>=80)[0])&(lb>0)
cnt=np.zeros((H,W))
for my,mx in zip(*np.where(skl)):
    X=int((mx-MX0)//CEL); Y=int((my-MY0)//CEL+DY)
    if 0<=X<W and 0<=Y<H: cnt[Y,X]+=1
intl=(cnt>=8)&SIL&(MATR!='schild')&(DEEL!='kop')&(DEEL!='staart')
lb2,n2=ndimage.label(intl,structure=np.ones((3,3)))
for i in range(1,n2+1):
    if (lb2==i).sum()<3: intl[lb2==i]=False
lijn|=intl
for Y,X in zip(*np.where(SIL&~VAST)):
    if any(KAAKM[Y+dy,X+dx] for dy,dx in N4 if 0<=Y+dy<H and 0<=X+dx<W): lijn[Y,X]=True
lijn=thin(lijn)
lijn&=~VAST
# ---------- 3. vulling: volle tintreeks per vlak (B) ----------
ZONE=SIL&~lijn&~VAST
mt=MT.copy()
for v in np.unique(SL[SIL]):
    mm=(SL==v)&SIL; mt[mm&~np.isfinite(mt)]=MED.get(v,40)
for _ in range(2):
    nm=mt.copy()
    for Y,X in zip(*np.where(ZONE)):
        vals=[mt[Y,X]]*2+[mt[Y+dy,X+dx] for dy,dx in N8 if 0<=Y+dy<H and 0<=X+dx<W and ZONE[Y+dy,X+dx] and SL[Y+dy,X+dx]==SL[Y,X]]
        nm[Y,X]=np.mean(vals)
    mt=nm
o=B.copy(); o[ZONE]=0
TINT={}                                                     # vlak -> gebruikte niveaus (voor het rapport)
for v in np.unique(SL[ZONE]):
    mm=(SL==v)&ZONE; P_=np.argwhere(mm); nv=len(P_)
    if nv==0: continue
    ys_,xs_=P_[:,0].astype(float),P_[:,1].astype(float)
    cy,cx=ys_.mean(),xs_.mean(); r=max(np.sqrt(nv/np.pi),1.5)
    z=mt[mm]; z=np.clip((z-z.mean())/(z.std()+6),-2,2)       # modeltoon binnen het vlak (+6: vlak model blijft vlak)
    geo=-((xs_-cx)+(ys_-cy))/(1.6*r)                          # bol: linksboven licht
    rim=np.array([(-0.9 if not (0<=Y+1<H and 0<=X+1<W and mm[Y+1,X+1]) else 0)+
                  (0.5 if not (0<=Y-1<H and 0<=X-1<W and mm[Y-1,X-1]) else 0) for Y,X in P_])
    med=MED.get(v,40); mat=MATR[P_[0][0],P_[0][1]]
    if mat=='schild':                                         # lang schild: licht langs de voorrand (links), schaduw rechts
        Ua=(xs_-(723.4-MX0)/CEL)*(-0.847)+(ys_-((470.1-MY0)/CEL+DY))*0.532
        geo=-Ua/4.0
    if DEEL[P_[0][0],P_[0][1]]=='staart':                     # hoorn: lichte band langs de bovenkant tot in de punt (model)
        top={x_:ys_[xs_==x_].min() for x_ in set(xs_)}
        geo=-np.array([(y_-top[x_]) for y_,x_ in zip(ys_,xs_)])/1.5
        rim=rim*0.3
    sc=1.0*z+1.0*geo+rim
    if mat=='schild':
        niv=[13,14,7]; aand=[.3,.5,.2]
    else:
        b=0 if med<45 else 1 if med<72 else 2
        d=DEEL[P_[0][0],P_[0][1]]
        if d in ('arm_ver','been_ver'): b-=1
        if d in ('arm','been') and med>=45: b+=1
        glans=(np.nanmax(mt[mm])>=med+20) or b>=2
        if nv>=30 and glans: k,aand=4,[.22,.43,.25,.10]
        elif nv>=10:         k,aand=3,[.28,.46,.26]
        elif nv>=4:          k,aand=2,[.6,.4]
        else:                k,aand=1,[1.]
        st=min(max(b-1,0),4-k)                                  # k opeenvolgende tinten rond de basistint, binnen 0..3
        lv=list(range(st,st+k))
        niv=[3+x for x in lv]
        if b<=0 and k>=3:                                       # donker vlak (romp, verre ledematen; model bijna zwart): lijntint
            niv=[2,3,4] if k==3 else [2,3,4,5]                  # als diepste schaduw, zodat de lijnen in het donker opgaan
            aand=[.3,.45,.25] if k==3 else [.28,.42,.2,.1]
    # rangorde -> niveaus (contigu, zodat de tinten vlakken vormen en geen ruis)
    volg=np.argsort(sc,kind='stable'); grenzen=np.cumsum(aand)[:-1]*nv
    for rnk,i in enumerate(volg):
        j=int(np.searchsorted(grenzen,rnk,side='right'))
        o[P_[i][0],P_[i][1]]=niv[j]
    TINT[v]=niv
# ---------- D. dekschildtekening ----------
# Model (gemeten dwars op de lengteas, u in spritepx): donkere rand links (u -5.5), lichte voorrand (u -4..-3), donkere
# langsstreep (u -2.2), gemengd midden, donkere langsstreep (u +2.5), lichte buitenrand (u +4.3). De fijne streepjes zelf zijn op
# 64 px ruis. Aanpak van Mega Pinsir (vleugel: een paar grote vlakke vlakken in een contrasttint direct tegen de basiskleur) en
# Crustle (banden die de vorm volgen): twee doorlopende donkere langsstrepen op de plek van de modelbanen, onderbroken waar
# het model daar licht is (zo blijven de streepjes van het model als lange stukken), lichte voorrand vrij.
SCH=(DEEL=='schild')&ZONE
AX=(0.532,0.847); SCX,SCY=(723.4-MX0)/CEL,(470.1-MY0)/CEL+DY       # lengteas en midden van het schild (model)
U=(xx+0.5-SCX)*(-AX[1])+(yy+0.5-SCY)*AX[0]
T=(xx+0.5-SCX)*AX[0]+(yy+0.5-SCY)*AX[1]
# basis per baan zoals het model: lichte randbanen (u -4.3..-3.0 en +3.6..+4.8), oker midden, schaduw aan de onderkant (punt)
for Y,X in zip(*np.where(SCH)):
    u_=U[Y,X]
    if -4.4<=u_<=-2.9 or 3.5<=u_<=4.9: o[Y,X]=7
    else: o[Y,X]=14
    onder=not (Y+1<H and X+1<W and DEEL[Y+1,X+1]=='schild' and SIL[Y+1,X+1])
    if T[Y,X]>9.5 or (onder and o[Y,X]==14): o[Y,X]=13
tek=SCH&(((np.abs(U+2.2)<1.0)|(np.abs(U-2.5)<1.2))&(VL>=0.15))
tek|=SCH&(np.abs(U)<1.6)&(VL>=0.55)&(o==14)                       # sterke modelvlekken in het midden
gap=SCH&(((T+20)%5.0)<0.9)                                         # streepjes zoals het model: om de ±5 px een onderbreking
tek&=~gap
lbt,nt=ndimage.label(tek,structure=np.ones((3,3)))
for i in range(1,nt+1):
    if (lbt==i).sum()<3: tek[lbt==i]=False
o[tek]=12
# ---------- F. ronde schouder en knie (cirkel gemeten op de modellijn, Hough; spritecoördinaten) ----------
# schouder nabije arm: midden (35.6, 35.0), straal 3.5; knie nabij been: midden (44.6, 52.8), straal 2.9; verre knie (24.2, 50.0), 2.4.
# Binnen de bol: geen binnenlijnen, bolschaduw met hooglicht linksboven (4 tinten); de rand van de bol wordt de lijntint
# waar het model daar een lijn heeft. Alleen pixels van het eigen onderdeel.
BOLLEN=[(35.6,35.0,3.5,('arm',),0),(44.6,52.8,2.9,('been',),0),(24.2,50.0,2.4,('been_ver',),-1)]   # laatste: verre knie, een stap donkerder
nbol=0
for bcx,bcy,br,delen,dt in BOLLEN:
    for Y,X in zip(*np.where(SIL&~VAST)):
        if DEEL[Y,X] not in delen and not (DEEL[Y,X] in ('romp','been','arm','been_ver') and np.hypot(X+0.5-bcx,Y+0.5-bcy)<=br-0.5): continue
        d=np.hypot(X+0.5-bcx,Y+0.5-bcy)
        if d<=br-0.5:
            hx,hy=bcx-0.4*br,bcy-0.4*br; dh=np.hypot(X+0.5-hx,Y+0.5-hy)
            t=6 if dh<0.38*br else 5 if dh<0.8*br else 4 if dh<1.15*br else 3
            if (X+0.5-bcx)+(Y+0.5-bcy)>0.95*br: t=3              # schaduwsikkel rechtsonder
            o[Y,X]=max(t+dt,2); lijn[Y,X]=False; nbol+=1
        elif d<=br+0.55 and DEEL[Y,X] in delen:
            zwm=max([ZW[Y+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if 0<=Y+dy<H and 0<=X+dx<W])
            if zwm>0.12: lijn[Y,X]=True
lijn=thin(lijn)&~VAST
# ---------- lijnen + buitenrand ----------
for Y,X in zip(*np.where(lijn)): o[Y,X]=2 if MATR[Y,X]=='lijf' else 11
P=np.pad(SIL,1)
for Y,X in zip(*np.where(SIL&~VAST)):
    if any(not P[Y+1+dy,X+1+dx] for dy,dx in N4): o[Y,X]=1
# ---------- opruimen: tintvlekjes < 3 px ----------
def opruimen(o,groep,minpx=3):
    for _ in range(6):
        ch=0
        for k in groep:
            lbq,nq=ndimage.label(o==k)
            for i in range(1,nq+1):
                pts=np.argwhere(lbq==i)
                if len(pts)>=minpx or any(VAST[Y,X] for Y,X in pts): continue
                bb={}
                for Y,X in pts:
                    for v in nb(o,Y,X):
                        if v in groep and v!=k: bb[v]=bb.get(v,0)+1
                if bb:
                    nv=max(bb,key=bb.get)
                    for Y,X in pts: o[Y,X]=nv
                    ch+=1
        if not ch: break
    return o
o=opruimen(o,[3,4,5,6]); o=opruimen(o,[12,13,14,7])
ZONDER=o.copy()
# ---------- E. kopstekels (variant met): posities gemeten op het model (rooster 24x) ----------
# randstekel: punt (x,y) zwart; rij eronder 3 breed: zwart | licht | zwart (silhouet +1 px links en rechts waar nodig);
# kegel op het kopschild: punt lijntint, rij eronder licht | lijntint (lichte voorkant links, schaduw rechts)
RAND=[(15,19),(18,18),(23,17),(26,15),(44,18)]
KEGEL=[(27,20),(32,19),(36,19)]
o2=o.copy(); sil_bij=[]
for X,Y in RAND:
    assert o2[Y,X]==1,(X,Y,o2[Y,X])
    for dx,t in ((-1,1),(0,5),(1,1)):
        if o2[Y+1,X+dx]==0: sil_bij.append((X+dx,Y+1))
        o2[Y+1,X+dx]=t
for X,Y in KEGEL:
    assert o2[Y,X]>1 and o2[Y+1,X]>1 and o2[Y+1,X+1]>1,(X,Y)
    o2[Y,X]=2; o2[Y+1,X]=5; o2[Y+1,X+1]=2
o=o2
# ---------- opslaan + controles ----------
def opslaan(q,path):
    p=Image.fromarray(q.astype('uint8'),'P'); pal=[v for cc in PAL for v in cc]; p.putpalette(pal+[0]*(768-len(pal))); p.save(path,transparency=0)
opslaan(o,UIT+'/pinsir_evo_r7.png'); opslaan(ZONDER,UIT+'/pinsir_evo_r7_zonder_stekels.png')
def binnenzwart(q):
    Pq=np.pad(q,1); return int(sum(1 for Y,X in zip(*np.where(q==1)) if all(Pq[Y+1+dy,X+1+dx]>0 for dy,dx in N8)))
FILL=[3,4,5,6,7,8,9,10,12,13,14]
def vlekjes(q,ks,st=None):
    t=0
    for k in ks:
        lbq,nq=ndimage.label(q==k,structure=st); t+=sum(1 for i in range(1,nq+1) if (lbq==i).sum()<3)
    return t
print('silhouet-diff met r6: zonder stekels %d, met stekels %d %s'%(int(((ZONDER>0)!=(R6>0)).sum()),int(((o>0)!=(R6>0)).sum()),sil_bij))
print('kleuren incl. transp.:',len(set(o.ravel())),'| zwart %.1f%% | zwarte binnenpixels r7 %d, r6 %d'%(100*(o==1).sum()/(o>0).sum(),binnenzwart(o),binnenzwart(R6)))
print('tintvlekjes < 3 px: 4-samenhang r7 %d (r6 %d) | 8-samenhang r7 %d (r6 %d)'%(vlekjes(o,FILL),vlekjes(R6,[3,4,5,6,8,9,10,12,13,14]),vlekjes(o,FILL,np.ones((3,3))),vlekjes(R6,[3,4,5,6,8,9,10,12,13,14],np.ones((3,3)))))
for nm,g in (('lijf',[2,3,4,5,6]),('kaak',[8,9,10,11]),('schild',[11,12,13,14,7])):
    print('%-6s'%nm,[(k,round(sum(PAL[k])/3),int((o==k).sum())) for k in g])
# tinten per vlak: alle tinten in het vlak buiten buitenrand en binnenlijnen (r7: ook de lijntint waar die als diepste schaduw
# in de vulling staat); r6 op dezelfde pixels
RAND_=np.zeros((H,W),bool)
for Y,X in zip(*np.where(SIL)):
    if any(not P[Y+1+dy,X+1+dx] for dy,dx in N4): RAND_[Y,X]=True
pv=[]
for v in np.unique(SL[SIL]):
    m=(SL==v)&SIL&~VAST&~RAND_&~lijn
    if m.sum()<6: continue
    t7=sorted(set(int(k) for k in o[m].ravel() if k>1)); t6=sorted(set(int(k) for k in R6[m].ravel() if k>1 and k not in (2,11)))
    pv.append((VLAKKEN.get(v,('?',))[0],int(v),int(m.sum()),len(t7),len(t6)))
pv.sort()
print('tinten per vlak (onderdeel, vlak, px vulling, r7, r6):'); [print('  ',r) for r in pv]
print('vlakken >= 20 px met < 3 tinten: r7',sum(1 for r in pv if r[2]>=20 and r[3]<3),'r6',sum(1 for r in pv if r[2]>=20 and r[4]<3),'van',sum(1 for r in pv if r[2]>=20))
if 'raster' in sys.argv:
    print('   '+''.join(str(x%10) for x in range(64)))
    for Y in range(12,62): print('%2d '%Y+''.join(CH[v] for v in o[Y]))
if 'detail' in sys.argv:
    for k in FILL:
        lbq,nq=ndimage.label(o==k,structure=np.ones((3,3)))
        for i in range(1,nq+1):
            pts=np.argwhere(lbq==i)
            if len(pts)<3: print(' vlekje',CH[k],[(int(x),int(y)) for y,x in pts],'gezicht/kaak' if any(VAST[y,x] for y,x in pts) else '')
# ---------- vel ----------
if 'detail' not in sys.argv and 'raster' not in sys.argv:
    from PIL import ImageDraw
    from vel import rgbp, M
    import os
    def modelbox(x0,y0,x1,y1,w,h):
        box=(MX0+x0*CEL,MY0+(y0-DY)*CEL,MX0+x1*CEL,MY0+(y1-DY)*CEL)
        big=Image.new('RGB',(1300,1300),'white'); big.paste(M,(100,100))
        return big.crop(tuple(int(round(v+100)) for v in box)).resize((w,h),Image.LANCZOS)
    G3='../../../../graphics/pokemon/'
    def gen3(sp,bg=(255,255,255)):
        im=Image.open(G3+sp+'/anim_front.png'); q=np.asarray(im)[:64]
        ls=open(G3+sp+'/normal.pal').read().split('\n')[3:19]; pal=np.array([[int(t) for t in l.split()] for l in ls if l.strip()])
        img=np.zeros((64,64,3),'uint8'); img[:]=bg
        for k in range(1,16): img[q==k]=pal[k]
        return Image.fromarray(img)
    r7=rgbp(UIT+'/pinsir_evo_r7.png'); r7z=rgbp(UIT+'/pinsir_evo_r7_zonder_stekels.png'); r6=rgbp('sprite_r6/pinsir_evo_r6.png')
    v=Image.new('RGB',(3*520,16+512+24+512+24+300),'white'); d=ImageDraw.Draw(v)
    for i,(nm,im) in enumerate((('r7 (met kopstekels)',r7),('r7 zonder kopstekels',r7z),('r6',r6))):
        v.paste(im.resize((512,512),Image.NEAREST),(i*520,16)); d.text((i*520+2,2),nm+' 8x',fill=(0,0,0))
    y=16+512+24
    d.text((2,y-14),'r7 naast het model op dezelfde maat (zoals sprite_r6/r6_naast_model.png)',fill=(0,0,0))
    v.paste(r7.resize((512,512),Image.NEAREST),(0,y)); v.paste(modelbox(0,0,64,64,512,512),(520,y))
    # dekschild 8x naast de voorbeelden
    sch=r7.crop((34,22,56,48)).resize((22*8,26*8),Image.NEAREST); v.paste(sch,(1040,y)); d.text((1040,y-14),'dekschild r7 8x | voorbeelden 8x',fill=(0,0,0))
    xo=1040+22*8+6
    for sp,box in (('pinsir/mega',(0,18,20,38)),('shuckle',(22,26,46,50)),('crustle',(10,8,40,38))):
        c_=gen3(sp).crop(box); c_=c_.resize((c_.width*6,c_.height*6),Image.NEAREST)
        if xo+c_.width>3*520: xo=1040; y2=y+26*8+20
        else: y2=y
        v.paste(c_,(xo,y2)); d.text((xo,y2+c_.height),sp,fill=(0,0,0)); xo+=c_.width+6
    y=y+512+24
    refs=('pinsir','heracross','tyranitar','aggron')
    for j,bg in enumerate(((255,255,255),(40,48,56))):
        for i,im in enumerate([rgbp(UIT+'/pinsir_evo_r7.png',bg),rgbp(UIT+'/pinsir_evo_r7_zonder_stekels.png',bg),rgbp('sprite_r6/pinsir_evo_r6.png',bg)]+[gen3(sp,bg) for sp in refs]):
            v.paste(im,(i*70,y+j*70))
    for i,im in enumerate([r7,r6]+[gen3(sp) for sp in refs]):
        v.paste(im.resize((128,128),Image.NEAREST),(520+i*132,y))
    d.text((2,y-14),'1x: r7 | r7 zonder stekels | r6 | Gen 3 Pinsir, Heracross, Tyranitar, Aggron (wit / donker)      2x: r7 | r6 | Gen 3',fill=(0,0,0))
    v.save(UIT+'/vel.png')
    n=Image.new('RGB',(1048,512),'white'); n.paste(r7.resize((512,512),Image.NEAREST),(0,0)); n.paste(modelbox(0,0,64,64,512,512),(536,0)); n.save(UIT+'/r7_naast_model.png')
    print('vel',v.size)
