# Guarana fase 1, r2: kleur/lijn binnen het bevroren r1-silhouet (alpha-diff 0 t.o.v. kaal/r1), niets getekend.
# Basis = dezelfde kale reductie als r1 (schaal 44/71, figuur x10-53, y15-51). Daarna, per Claudes benoemde reparaties:
#  1 tros: vruchtgrenzen = modelrasterlijnen (zwart + donkerrood L<72 in het natieve model) met lagere drempel -> 1-px binnenlijn (index 2);
#    vulling per pixel uit de modelhelderheid van alleen het vruchtvlees (lijnen niet meegeteld) -> schaduw/midden/licht; geen zwart meer
#    behalve pupil/oogcontour en buitenlijn aan de schaduwkant (en de puntjes, zoals het model).
#  2 buitenlijn: zwart alleen rechts/onder, lichtkant selout; selouttinten lichter (Gen 3: Bellsprout/Oddish-groen 82,98,41, Hoppip-rood 164,16,0).
#  3 krullen: zwart binnenin en aan de lichtkant -> groen/donkergroen; gaatjes in de krullen krijgen een donkergroene rand.
# Gebruik: python3 sprite_r2/bouw.py [UIT.png]   VARIANT=ogen_groter | zonder_puntjes
import sys, os, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen; import gemeen; from gemeen import *
a,c,L=klassen()
VAR=os.environ.get('VARIANT','')
PUNTJES=[(30,19),(31,19),(22,26),(22,27),(14,38),(24,53),(25,53),(47,30),(48,30)]
if VAR=='zonder_puntjes':
    for u,v in PUNTJES: c[v,u]=0
UIT='sprite_r3'
# palet r2: lijntinten iets lichter/verzadigder (Gen 3), vultinten = modeltonen (ongewijzigd)
gemeen.PAL[2]=(120,28,32)   # rood lijn/selout (model 119,35,32)
gemeen.PAL[6]=(66,96,52)    # groen lijn/selout (model 54,78,52; Gen 3 82,98,41)
TK=0.30; TW=0.30; TL=float(os.environ.get('TL','0.24'))   # TL: drempel modelrasterlijn in de tros
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
H,W=c.shape
# natieve lijnkaart in de tros: donkerrood (L<72) en zwart dat niet aan de achtergrond grenst en niet bij een oog hoort
from ogen import PUPIL, BOX, dekking
oogn=np.zeros(c.shape,bool)
for n,(u0,u1,v0,v1) in BOX.items():
    for v in range(v0,v1+1):
        for u in range(u0,u1+1):
            if c[v,u]==4 or (c[v,u]==1 and any(c[v+dy,u+dx]==4 for dy,dx in N8)): oogn[v,u]=True
NL=np.zeros(c.shape,bool)
for v in range(1,H-1):
    for u in range(1,W-1):
        if c[v,u]==2 and L[v,u]<72: NL[v,u]=True
        if c[v,u]==1 and not oogn[v,u] and all(c[v+dy,u+dx]!=0 for dy,dx in N4) and sum(c[v+dy,u+dx] in (1,2) for dy,dx in N8)>=4 and sum(c[v+dy,u+dx]==3 for dy,dx in N8)<=1: NL[v,u]=True
def tn(g,l):
    if g==2: return 3 if l<105 else 4 if l<140 else 5
    if g==3: return 6 if l<80 else 7 if l<118 else 8 if l<145 else 9
    if g==4: return 10 if l>=215 else 11
# --- kale reductie (identiek aan r1) ---
def tn1(g,l):
    if g==2: return 2 if l<72 else 3 if l<100 else 4 if l<140 else 5
    return tn(g,l)
o=np.zeros((64,64),int); F={}; FLI=np.zeros((64,64)); FSH=np.zeros((64,64))
for Y in range(64):
    for X in range(64):
        f=np.zeros(5); lum=np.zeros(5); fl=0; fr=0; lr=0
        for u,v,w in overlap(X,Y):
            k=c[v,u]; f[k]+=w; lum[k]+=w*L[v,u]
            if NL[v,u]: fl+=w
            elif k==2:
                fr+=w; lr+=w*L[v,u]
                if L[v,u]>=140: FLI[Y,X]+=w
                if L[v,u]<100: FSH[Y,X]+=w
        F[(X,Y)]=(f,fl,fr,(lr/fr if fr else 0))
        if f[1:].sum()<0.5: continue
        if f[1]>=TK: o[Y,X]=1; continue
        if f[4]>=TW: o[Y,X]=tn(4,lum[4]/f[4]); continue
        g=2+int(np.argmax(f[2:])); o[Y,X]=tn1(g,lum[g]/f[g])
kaal=o.copy(); opslaan(kaal,UIT+'/kaal.png')
fg0=kaal>0
tel={}
def stap(n,v,o): tel[n]=tel.get(n,0)+int((v!=o).sum())
SEL={**{k:2 for k in ROOD},**{k:6 for k in GROEN}}
GRP={**{k:ROOD for k in ROOD},**{k:GROEN for k in GROEN},**{k:WIT for k in WIT}}
# --- 0. ogen (zoals r1) ---
v=o.copy(); OOG=np.zeros((64,64),bool); PUP=np.zeros((64,64),bool)
for n in PUPIL:
    for (X,Y),(fp,fw) in dekking(n).items():
        if fp>=0.40: o[Y,X]=1; OOG[Y,X]=PUP[Y,X]=True
        elif fw>=0.40: o[Y,X]=10; OOG[Y,X]=True
if VAR=='ogen_groter':   # Weepinbell-nabij oog (anim_front_gba x26-32 y34-40), pixel voor pixel; zie r1/NOTITIES
    WEEP=['..OOO..','.OWWWK.','OWWWWWK','OWKKWWK','OWKKWWK','.KWWWK.','..KKK..']
    NIEUW=np.zeros((64,64),bool); NP=np.zeros((64,64),bool)
    for x0,y0 in ((16,17),(24,19),(14,27)):
        for dy,rij in enumerate(WEEP):
            for dx,ch in enumerate(rij):
                if ch=='.' or not fg0[y0+dy,x0+dx]: continue   # silhouet bevroren: niets buiten de r1-hoofdversie
                o[y0+dy,x0+dx]={'O':2,'W':10,'K':1}[ch]; NIEUW[y0+dy,x0+dx]=True; NP[y0+dy,x0+dx]=(ch=='K' and 2<=dx<=3 and 3<=dy<=4)
    # oogwit dat daardoor op de buitenrand komt -> zwart (de zwarte oogrand van Weepinbell schuift 1 px naar binnen)
    for Y,X in zip(*np.where(NIEUW&(o==10))):
        if any(not fg0[Y+dy,X+dx] for dy,dx in N4): o[Y,X]=1
    for Y,X in zip(*np.where(OOG&~NIEUW)): o[Y,X]=-1   # wordt hieronder als vrucht ingekleurd
    OOG=NIEUW; PUP=NP
else:
    # r3 hoofdversie: op modelmaat (wit ±4 px rond een 2x2-pupil) hangt het oogwit alleen diagonaal samen (keurder: "versplinterd").
    # Daarom per oog een klein rond Gen 3-oog 1-op-1: Psyduck (graphics/pokemon/psyduck/anim_front_gba.png, x21-25 y22-25):
    # wit 5x4 (afgeronde hoeken), 1-px pupil boven-midden, wit aaneengesloten. Psyducks oogrand (eigen donkergeel 'n') -> rechts/onder
    # zwart zoals de oogrand van het model, links/boven onze donkerrode lijntint (zelfde rolvertaling als bij het Weepinbell-ooglid).
    # Plaats: pupil op de modelpupil; rechteroog zo dat het wit niet op de buitenrand komt (pupil 2 px van de buitenlijn).
    PSY=['.WWW.',
         'WWKWW',
         'WWWWW',
         '.WWW.']
    NIEUW=np.zeros((64,64),bool); NP=np.zeros((64,64),bool)
    for x0,y0 in ((16,19),(25,21),(15,29)):
        for dy,rij in enumerate(PSY):
            for dx,ch in enumerate(rij):
                if ch=='.': continue
                X,Y=x0+dx,y0+dy
                o[Y,X]=10 if ch=='W' else 1; NIEUW[Y,X]=True; NP[Y,X]=(ch=='K')
        rand_=set()
        for dy,rij in enumerate(PSY):
            for dx,ch in enumerate(rij):
                if ch=='.': continue
                for ddy,ddx in N4:
                    X,Y=x0+dx+ddx,y0+dy+ddy
                    if not NIEUW[Y,X] and fg0[Y,X]: rand_.add((X,Y,ddx>0 or ddy>0))
        for X,Y,sch in rand_:
            if (X,Y,True) in rand_ or sch: o[Y,X]=1
            else: o[Y,X]=2
            NIEUW[Y,X]=True
    for Y,X in zip(*np.where(OOG&~NIEUW)): o[Y,X]=-1
    OOG=NIEUW; PUP=NP
stap('ogen',v,o)
# oogcontour: zwart dat 4-buur is van oogwit
def oogrand(o,Y,X): return any(0<=Y+dy<64 and 0<=X+dx<64 and o[Y+dy,X+dx] in WIT for dy,dx in N4)
# --- 1. tros: vruchten uit het model, grenzen = modelrasterlijnen, vulling uit de modelhelderheid ---
# vruchten = samenhangende stukken vruchtvlees (rood L>=72) in het natieve model (7 grote stukken, gemeten); per spritepixel de vrucht met de meeste dekking.
VM=(c==2)&(L>=72)&~NL; VM[:,52:]=False; VM[54:,:]=False
vl,vn=label(VM,acht=False); groot=[i for i in range(1,vn+1) if (vl==i).sum()>=8]
TROS=np.zeros((64,64),bool); FID=np.zeros((64,64),int); FL=np.zeros((64,64)); LR=np.zeros((64,64))
for (X,Y),(f,fl,fr,lr) in F.items():
    if fg0[Y,X] and X<=34 and Y<=37 and f[2]>=f[3] and f[2]+f[1]>0 and not (f[3]>0.3):
        TROS[Y,X]=True; FL[Y,X]=fl; LR[Y,X]=lr
        d={}
        for u,v_,w in overlap(X,Y):
            if vl[v_,u] in groot: d[vl[v_,u]]=d.get(vl[v_,u],0)+w
        if d: FID[Y,X]=max(d,key=d.get)
v=o.copy()
VRIJ=TROS&~OOG&~((o==1)&np.array([[oogrand(o,Y,X) for X in range(64)] for Y in range(64)]))
LIJN=np.zeros((64,64),bool)
LIJN|=VRIJ&(FID==0)                      # geen vruchtvlees onder de pixel: lijn
LIJN|=VRIJ&(FL>=0.5)                     # sterke modellijn
for Y in range(64):                      # grens tussen twee vruchten: 1 px lijn op de pixel met de meeste modellijn
    for X in range(64):
        for dy,dx in ((0,1),(1,0)):
            Y2,X2=Y+dy,X+dx
            if Y2<64 and X2<64 and VRIJ[Y,X] and VRIJ[Y2,X2] and FID[Y,X] and FID[Y2,X2] and FID[Y,X]!=FID[Y2,X2] and not (LIJN[Y,X] or LIJN[Y2,X2]):
                if max(FL[Y,X],FL[Y2,X2])>=TL:
                    if FL[Y,X]>=FL[Y2,X2]: LIJN[Y,X]=True
                    else: LIJN[Y2,X2]=True
# vulling: modelhelderheid van het vruchtvlees per pixel (lijnen niet meegeteld): >=145 licht, <100 schaduw, anders midden
# r3: aandeel licht (L>=140) en schaduw (L<100) in het vruchtvlees onder de pixel, zodat kleine modelglimplekken niet wegmiddelen
TLI=float(os.environ.get('TLI','0.30')); TSH=float(os.environ.get('TSH','0.50'))
for Y,X in zip(*np.where(VRIJ&~LIJN&(LR>0))):
    fr=F[(X,Y)][2]; li=FLI[Y,X]/fr; sh=FSH[Y,X]/fr
    o[Y,X]=5 if li>=TLI else 3 if sh>=TSH else 4
for Y,X in zip(*np.where(VRIJ&~LIJN&((FID==0)|(LR==0)))): o[Y,X]=2
o[LIJN]=2
o[o==-1]=4
stap('tros: lijnen + vulling uit model',v,o)
# --- 2. binnenlijnen groen: zwart dat niet aan de achtergrond grenst -> donkergroen (rood is al gedaan) ---
v=o.copy(); fg=o>0
for Y,X in zip(*np.where(o==1)):
    if PUP[Y,X] or oogrand(o,Y,X): continue
    if any(not fg[Y+dy,X+dx] for dy,dx in N4): continue
    r=sum(o[Y+dy,X+dx] in ROOD for dy,dx in N8); g=sum(o[Y+dy,X+dx] in GROEN for dy,dx in N8)
    o[Y,X]=2 if r>g else 6
stap('binnenlijnen',v,o)
# --- 3. buitenlijn: achtergrond rechts/onder -> zwart, anders selout; zwart aan de lichtkant -> selout (niet: pupil, oogcontour, puntjes) ---
# buitenachtergrond = verbonden met de beeldrand; kleine ingesloten gaatjes (<= 6 px, de krulletjes) krijgen een selout-rand
bg=~fg0; lab,n=label(bg,acht=False); buiten=lab==lab[0,0]
klein=np.zeros((64,64),bool)
for i in range(1,n+1):
    m=lab==i
    if i!=lab[0,0] and m.sum()<=6: klein|=m
PUNT=np.zeros((64,64),bool)
for Y in range(64):
    for X in range(64):
        if sum(w for u,v_,w in overlap(X,Y) if (u,v_) in PUNTJES)>=0.15: PUNT[Y,X]=True
v=o.copy(); uit=[]
for Y,X in zip(*np.where(fg0)):
    k=o[Y,X]
    if k in WIT or PUP[Y,X] or (k==1 and oogrand(o,Y,X)) or (k==1 and PUNT[Y,X]): continue
    sch=any(bg[Y+dy,X+dx] and not klein[Y+dy,X+dx] for dy,dx in ((0,1),(1,0)))
    licht=any(bg[Y+dy,X+dx] for dy,dx in N4)
    if not licht: continue
    if sch: n_=1
    else:
        if k==1:
            r=sum(o[Y+dy,X+dx] in ROOD for dy,dx in N8); g=sum(o[Y+dy,X+dx] in GROEN for dy,dx in N8); n_=2 if r>g else 6
        else: n_=SEL[k]
    if n_!=k: uit.append((Y,X,n_))
for Y,X,k in uit: o[Y,X]=k
stap('buitenlijn',v,o)
# --- 4. krullen (dunne ranken onder en naast het lijf): zoals Bellsprouts wortels en bladranden (gemeten in anim_front_gba:
#        1-px ranken in eigen donkere tint, bladrand donkergroen 82,98,41, geen zwart): zwart in de krullen blijft alleen waar het
#        de schaduwrand (rechts/onder) is van een groene vulpixel; overige zwart (1-px stukken, lichtkant, binnenkant) -> donkergroen. ---
def krul(X,Y): return Y>=42 and (X<=24 or X>=42 or Y>=47)
v=o.copy(); uit=[]
for Y,X in zip(*np.where(o==1)):
    if not krul(X,Y) or PUNT[Y,X]: continue
    if any(o[Y+dy,X+dx] in (7,8,9) for dy,dx in ((-1,0),(0,-1))): continue
    uit.append((Y,X))
for Y,X in uit: o[Y,X]=6
stap('krullen: zwart -> donkergroen',v,o)
# --- 5. ontkorrelen (zoals r1) en losse zwarte pixels ---
def ontkorrel(o):
    for k,minim in ((3,3),(4,3),(5,2),(7,3),(8,3),(9,2)):
        lab_,n_=label(o==k,acht=False)
        for i in range(1,n_+1):
            m=lab_==i
            if m.sum()>=minim: continue
            buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(m)) for dy,dx in N4 if o[Y+dy,X+dx] in GRP[k] and o[Y+dy,X+dx]!=k and o[Y+dy,X+dx]!=SEL[k]]
            if buur: o[m]=max(set(buur),key=buur.count)
v=o.copy(); ontkorrel(o); ontkorrel(o); stap('ontkorrelen',v,o)
# --- 6. r3: benoemde reparaties van de keurder (sprite_r2/KEURING.md), elk gelezen op het model (raster.py, 40x); silhouet onveranderd,
#        nooit op oogpixels. Rood: 2 lijn, 3 schaduw, 4 midden. Groen: 6 lijn, 7 schaduw. ---
v=o.copy()
P={
 # vruchtje links van het bovenoog: model heeft een middenrode kern op x15 (y21-22), rest donker -> geen rechte schaduwkolom meer
 (15,21):4,(15,22):4,
 # linkervrucht: de onderlijn (rij 28) loopt in het model door tot x15 en buigt bij de middenvrucht omhoog naar de verticale grens x17
 # (17,24-25); daaronder hoort (16-17,28) bij de oogvrucht (modelschaduw). Sikkel = de donkere onderkant van de modelvrucht (x13-16, y26-27).
 (15,28):2,(16,27):2,(17,26):2,(16,28):3,(17,28):3,(13,27):3,(14,27):3,(15,27):3,(16,26):3,
 # rechtsondervrucht: model is links (x23-24) middenrood, schaduw als sikkel onder/rechts -> de schaduwkolom x23 en het linkereind van rij 32 weg
 (23,29):4,(23,30):4,(23,31):4,(23,32):4,(24,31):4,
 # oogvrucht linksonder: modelglimplek rechtsonder van het oog (18-19,33-34); door de zwarte oogrand niet meer tegen het oogwit
 (19,33):5,(19,34):5,
 # ruis rood
 (27,27):3,
 # blad (x48-51, y25-29): model lichte helft linksboven (schaduwgroen 7), donkere helft rechtsonder (6); randen blijven lijn
 (49,26):7,(50,26):7,(48,27):7,(49,27):7,(51,26):6,(50,27):6,(51,27):6,(49,28):6,(50,28):6,
 # krul onder links (x26-30, y48-51): model rij 50 = groene krulstreng, rij 51 = onderrand -> streng terug in groen
 (27,50):7,(28,50):7,(29,50):7,
 # losse groene pixels in de krullen -> lijntint (keurder)
 (19,43):6,(18,44):6,(44,49):6,(44,50):6,(22,48):6,
}
for (X,Y),k in P.items():
    if OOG[Y,X] or not fg0[Y,X]: continue
    o[Y,X]=k
# losse groene vulpixels op de rank-onderrand -> meest voorkomende groene vulburen (7/8/9)
for X,Y in ((31,46),(31,47),(23,46),(47,45),(48,46),(52,46)):
    nb=[o[Y+dy,X+dx] for dy,dx in N4 if o[Y+dy,X+dx] in (7,8,9) and o[Y+dy,X+dx]!=o[Y,X]]
    if nb and o[Y,X] in (7,8,9): o[Y,X]=max(set(nb),key=nb.count)
stap('r3-reparaties (keurder)',v,o)
NAAM=sys.argv[1] if len(sys.argv)>1 else UIT+'/guarana_r3.png'
assert ((o>0)==fg0).all(), 'silhouet gewijzigd'
opslaan(o,NAAM); toon(o,12,54,6,58)
print('stappen',tel); print('anders dan kaal: %d px'%(o!=kaal).sum(),'| kleuren',len(set(o.ravel()))-1,'| figuur px',(o>0).sum(),'| zwart %.1f%%'%(100*(o==1).sum()/(o>0).sum()))
