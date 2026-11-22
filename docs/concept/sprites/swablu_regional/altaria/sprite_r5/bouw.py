# Altaria (onweerswolk) r3: op het kop x1,5-dy10-model (model_kop/natief_kop15_dy10.png). Jordi: "let er bij altaria op dat het linkeroog ook
# zichtbaar moet zijn voor de sprite om mooi te worden, als dat niet past is het hoofd nog steeds te klein".
# Silhouet = r1-reductie op dat model (sprite_r5/basis.py -> basis_kop15.png), alpha nooit veranderd.
# Kleur: per spritepixel de MEEST VOORKOMENDE modeltoon in het 3x3-blok (modus i.p.v. gemiddelde: de bollen van het model blijven bollen:
# lichte kap, lijf, donkere onderboog), daarna alleen technisch opschonen. Keuring r2 (MOETEN 1-6) verwerkt, zie NOTITIES.md.
# Jordi: "iets minder detail is niet erg tov het model, zolang die niet blurry wordt" / "De belijning moet juist zachter en niet zwart" /
# "het ligt aan dat er meer dan 2 kleurtinten moeten zijn om minder blur te hebben".
import sys, numpy as np
sys.path.insert(0,'gereedschap'); sys.path.insert(0,'sprite_r5')
import gemeen as G; from gemeen import label
import basis as B; from basis import blok
from PIL import Image
UIT='sprite_r5'
# 0 transp | 1 pupil | wolk 2 selout L55, 3 donker L73, 4 midden L95, 5 licht L123, 6 hooglicht L178 (dicht bij de modeltonen L44/72/122/186; selout lichter) |
# violet 7 selout L53, 8 donker L78, 9 midden L112, 10 licht L156 | 11 static (r4: (150,206,230) L190, tussen het wolkhooglicht en het r3-cyaan in: subtiel lichtblauw) | 12 glans
PAL=[(152,208,160),(16,18,40),
     (34,58,92),(46,80,112),(62,104,138),(84,134,166),(136,192,214),
     (44,44,116),(66,68,160),(98,100,210),(144,146,236),
     (150,206,230),(240,244,255)]
G.PAL=PAL
WS,WD,WM,WL,WH=2,3,4,5,6; VS,VD,VM,VL=7,8,9,10; ST,GL,PU=11,12,1
VULW=[WD,WM,WL,WH]; VULV=[VD,VM,VL]
CH='.Ks0123vabcSW'
def toon(o,y0=4,y1=64,x0=0,x1=64):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in o[y,x0:x1]))
a,c,L=B.a,B.c,B.L
bas=np.asarray(Image.open('sprite_r5/basis_kop15.png')).astype(int); fig=bas>0
KUIF=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fig)): KUIF[Y,X]=B.kuif(X,Y) and bas[Y,X] in (1,6,7,8,9)
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def meest(l): return max(set(l),key=l.count)
tel={}
def stap(naam,v,o): tel[naam]=tel.get(naam,0)+int((v!=o).sum())
# --- modeltonen per natieve pixel (alleen indelen, niets getekend). Grenzen = dalen tussen de vier tonen van het model
#     (wolk: L44 / L72 / L122 / L186; violet: L64 / L107 / L140+lavendelwit). K = zwarte modellijn. ---
T=np.full(L.shape,-1); w=c==2; vi=(c==3)|(c==5)
T[w&(L<58)]=WD; T[w&(L>=58)&(L<100)]=WM; T[w&(L>=100)&(L<156)]=WL; T[w&(L>=156)]=WH
T[vi&(L<85)]=VD; T[vi&(L>=85)&(L<130)]=VM; T[vi&(L>=130)]=VL
T[c==1]=99
import os; KORREL=int(os.environ.get('KORREL','4')); SMIN=int(os.environ.get('SMIN','10'))
KW=float(os.environ.get('KW','2')); DW=float(os.environ.get('DW','1.4'))
LAAG=int(os.environ.get('LAAG','2')); LT=int(os.environ.get('LT','5')); HT=int(os.environ.get('HT','4')); DT=int(os.environ.get('DT','4'))
GEM=int(os.environ.get('GEM','1')); TD=float(os.environ.get('TD','62'))
LTV=int(os.environ.get('LTV','5')); KH=int(os.environ.get('KH','8'))
KMIN=2   # >=2 zwarte modelpixels in het blok = lijnkandidaat (alleen als hij doorloopt, zie stap 2)
# --- 1. modus per blok ---
o=np.zeros((64,64),int); K=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fig)):
    u,v=blok(X,Y); b=T[v:v+3,u:u+3].ravel(); b=b[b>=0]
    nw=np.isin(b,VULW).sum(); nv=np.isin(b,VULV).sum()
    if (b==99).sum()>=KMIN or nw+nv==0: K[Y,X]=True
    grp=VULW if nw>=nv else VULV
    # gewogen modus: zwarte modellijn telt als donkerste vultint (onderboog/dal), met gewicht KW; de donkerste toon met gewicht DW,
    # zodat de smalle dalen tussen de bollen bij het verkleinen niet wegvallen (anders smelten de lichte kappen samen)
    wt={}
    for t in b:
        if t==99: t,g=(WD if grp is VULW else VD),KW
        elif t in grp: g=DW if t in (WD,VD) else 1.0
        else: continue
        wt[t]=wt.get(t,0)+g
    o[Y,X]=max(wt,key=wt.get) if wt else (WD if grp is VULW else VD)
    if grp is VULW and LAAG:
        # gelaagde dekking i.p.v. modus: een lichte kap alleen waar het model voor >= LT/9 licht is (dan blijven de dalen tussen de kappen
        # staan en smelten de kappen niet samen); hooglicht waar >= HT/9 hooglicht; donker waar >= DT/9 donker of zwart
        n=lambda t:(b==t).sum()
        if n(WL)+n(WH)>=LT: o[Y,X]=WH if n(WH)>=HT else WL
        elif n(WD)+n(99)>=DT: o[Y,X]=WD
        else: o[Y,X]=WM
# kappen per modelbol (LAAG=2): de lichte kappen (licht+hooglicht) van het model zijn per bol een eigen samenhangend vlak; elk krijgt zijn
# eigen spritepixels (grootste dekking wint) en waar twee kappen elkaar raken blijft de pixel met de minste dekking lijftint: zo smelten de
# bollen niet samen (MOET 2). Niets getekend: vorm en plek van elke kap komen uit het model.
if LAAG==2:
    capn=(T==WL)|(T==WH)
    ER=int(os.environ.get('ER','1'))      # kapmasker ER keer 1 px insnoeren vóór het labelen: dunne bruggetjes tussen twee bollen breken
    ce=capn.copy()
    for _ in range(ER):
        ce=ce&np.roll(ce,1,0)&np.roll(ce,-1,0)&np.roll(ce,1,1)&np.roll(ce,-1,1)
    lc,nc=label(ce,acht=False)
    # terug uitbreiden binnen het oorspronkelijke kapmasker (elke kappixel krijgt het label van de dichtstbijzijnde kern)
    for _ in range(ER+1):
        l2=lc.copy()
        for dy,dx in N4:
            sh=np.roll(np.roll(lc,dy,0),dx,1); m=(l2==0)&capn&(sh>0); l2[m]=sh[m]
        lc=l2
    own=np.zeros((64,64),int); cov=np.zeros((64,64))
    for Y,X in zip(*np.where(fig&np.isin(o,VULW))):
        u,v=blok(X,Y); b=lc[v:v+3,u:u+3].ravel(); b=b[b>0]
        if len(b)==0: continue
        cnt=np.bincount(b); k=cnt.argmax(); tot=len(b)
        if tot>=(LTV if B.vleugel(X,Y) else LT): own[Y,X]=k; cov[Y,X]=cnt[k]   # r4: vleugels strenger (lichte kappen alleen op de bollen)
    for Y,X in zip(*np.where(own>0)):
        for dy,dx in N4:
            k2=own[Y+dy,X+dx]
            if k2 and k2!=own[Y,X] and cov[Y,X]<=cov[Y+dy,X+dx]: own[Y,X]=-1; break
    for Y,X in zip(*np.where(fig&np.isin(o,VULW))):
        u,v=blok(X,Y); b=T[v:v+3,u:u+3].ravel(); n=lambda t:(b==t).sum()
        if own[Y,X]>0: o[Y,X]=WH if n(WH)>=HT else WL
        elif GEM:   # lijf buiten de kappen: gemiddelde blokhelderheid (onderbogen, dalen en de lagen van de onderrok blijven zo staan)
            Lm=L[v:v+3,u:u+3].mean(); o[Y,X]=WD if Lm<TD else WM
        elif n(WD)+n(99)>=DT: o[Y,X]=WD
        else: o[Y,X]=WM
kaal=o.copy()
# --- 2. naden: zwarte modellijnen (K) die als lijn doorlopen (8-samenhangend >= 3 px) worden selout van hun materiaal (geen zwart);
#        losse K-stippen verdwijnen in de modustint ---
lab,n=label(K,acht=True)
for i in range(1,n+1):
    m=lab==i
    if m.sum()<3: continue
    for Y,X in zip(*np.where(m)): o[Y,X]=WS if o[Y,X] in VULW else VS
stap('naden',kaal,o)
# --- 3. ontkorrelen: tintvlakjes < 4 px (hooglicht < 3) -> meest voorkomende buurtint van hetzelfde materiaal ---
def groep(k): return VULW if k in VULW else VULV if k in VULV else [k]
def ontkorrel(o):
    for k in VULW+VULV:
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            mm=lab==i
            if mm.sum()>=(3 if k==WH else (KORREL if k in VULW else 4)): continue
            buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(mm)) for dy,dx in N4 if o[Y+dy,X+dx] in groep(k) and o[Y+dy,X+dx]!=k]
            if buur: o[mm]=meest(buur)
v=o.copy()
# afronden: 3x3-meerderheidsfilter op de wolkvultinten (MF keer). Een vultint die in het 3x3-venster in de minderheid is (<= 3 van 9) en
# een buurtint die >= 5 van 9 heeft -> die buurtint: hoekjes en tandjes van de bolvormen gaan eraf, de vormen worden ronder (geen nieuw detail)
MF=int(os.environ.get('MF','0'))
for _ in range(MF):
    o2=o.copy()
    for Y,X in zip(*np.where(np.isin(o,VULW))):
        win=[o[Y+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1)]
        if win.count(o[Y,X])>3: continue
        best=max(VULW,key=win.count)
        if win.count(best)>=5: o2[Y,X]=best
    o=o2
for _ in range(3): ontkorrel(o)
for _ in range(2):                      # uitsteeksels van 1 px (3 buren van een andere tint) gladstrijken
    for Y,X in zip(*np.where(np.isin(o,VULW+VULV))):
        k=o[Y,X]; nb=[o[Y+dy,X+dx] for dy,dx in N4]
        if nb.count(k)>1: continue
        for t in set(nb):
            if t!=k and t in groep(k) and nb.count(t)>=3: o[Y,X]=t; break
stap('ontkorrelen',v,o)
# kapvolume: hooglicht alleen linksboven in een kap; de onder-/rechterrand van elke kap (2 px van de rand rechtsonder) wordt lichttint,
# zodat een grote modelkap geen vlak hooglichtblok is (Gen 3: hooglicht linksboven, kap daaronder) ---
v=o.copy(); kap=np.isin(o,[WL,WH])
for Y,X in zip(*np.where(o==WH)):
    if any(not kap[Y+dy,X+dx] for dy,dx in ((1,0),(0,1),(1,1))): o[Y,X]=WL   # r4: 1 px rand rechtsonder (2 px liet kleine kappen zonder hooglicht)
lab,n=label(o==WH,acht=False)
for i in range(1,n+1):
    if (lab==i).sum()<2: o[lab==i]=WL
stap('kapvolume',v,o)
# r4 kappen ronder (coördinator: "Kappen ronder (3 tinten met een tussenstap aan de rand, geen hoekige vlakken)"): een kappixel op een bolle
# hoek (boven/onder én links/rechts geen kap, ook de diagonaal niet) wordt middentint, de tussenstap naar het lijf; hooglicht dat daardoor aan
# de kaprand komt wordt licht (hooglicht | licht | midden van binnen naar buiten)
v=o.copy(); kap=np.isin(o,[WL,WH]); lab,n=label(kap,acht=False)
for Y,X in zip(*np.where(kap)):
    if (lab==lab[Y,X]).sum()<KH: continue
    for dy,dx in ((-1,-1),(-1,1),(1,-1),(1,1)):
        if not kap[Y+dy,X] and not kap[Y,X+dx] and not kap[Y+dy,X+dx]: o[Y,X]=WM; break
kap=np.isin(o,[WL,WH])
for Y,X in zip(*np.where(o==WH)):
    if any(not kap[Y+dy,X+dx] for dy,dx in ((1,0),(0,1))): o[Y,X]=WL
stap('kaphoeken',v,o)
# onderbogen (MOET 2: "donkere onderboog per bol"): waar in de reductie een lichtere bol (midden/licht) direct boven een donker dal ligt,
# wordt de bovenste dalpixel wolk-selout; alleen stukken >= ONB px (gebogen lijnen langs de onderkant van een modelbol, geen stippen)
ONB=int(os.environ.get('ONB','3'))
if ONB:
    v=o.copy(); kand=np.zeros((64,64),bool)
    for Y,X in zip(*np.where(o==WD)):
        if o[Y-1,X] in (WM,WL,WH) and o[Y+1,X] in (WD,WS,0) and fig[Y+1,X]: kand[Y,X]=True
    lab,n=label(kand,acht=True)
    for i in range(1,n+1):
        if (lab==i).sum()>=ONB: o[lab==i]=WS
    stap('onderbogen',v,o)
# --- 4. static: modelplekken (statisch() uit klassen.py, natief). Spritepixel = static als >= 2 static-modelpixels in het blok, plus blokken
#        met 1 die aan zo'n pixel grenzen (de lijn loopt door); 2x2-klontjes uitgedund (pixel met de minste modeldekking eruit);
#        stukjes < 4 px weg (Keuring MOET 6: weinig, langere zigzaglijnen, geen stukjes < 4 px). Eigen cyaan (11), niet de hooglichttint. ---
st=B.st; cnt=np.zeros((64,64),int)
for Y in range(64):
    for X in range(64):
        u,v=blok(X,Y)
        if 0<=u<st.shape[1]-2 and 0<=v<st.shape[0]-2: cnt[Y,X]=st[v:v+3,u:u+3].sum()
S=cnt>=2
S|=(cnt==1)&np.array([[any(cnt[Y+dy,X+dx]>=2 for dy,dx in N8) if 0<Y<63 and 0<X<63 else False for X in range(64)] for Y in range(64)])
for _ in range(2):
    for Y in range(63):
        for X in range(63):
            q=[(Y,X),(Y,X+1),(Y+1,X),(Y+1,X+1)]
            if all(S[p] for p in q): S[min(q,key=lambda p:cnt[p])]=False
lab,n=label(S,acht=True)
for i in range(1,n+1):
    m=lab==i; xs=np.where(m)[1]
    vonk=xs.max()<=6 or xs.min()>=58          # de losse boogjes naast de vleugels (model) mogen korter
    if m.sum()<(4 if vonk else SMIN): S[m]=False   # Keuring MOET 6: weinig, langere lijnen -> alleen de langste modellijnen
# r4 (coördinator: "lijnen 1 px dik, ... alleen de langere modelstukken"): uitdunnen tot 1 px (Zhang-Suen) en daarna weer stukken < SMIN weg
def dun(m):
    m=m.copy(); ver=True
    while ver:
        ver=False
        for st in (0,1):
            weg=[]
            for Y,X in zip(*np.where(m)):
                P=[m[Y-1,X],m[Y-1,X+1],m[Y,X+1],m[Y+1,X+1],m[Y+1,X],m[Y+1,X-1],m[Y,X-1],m[Y-1,X-1]]
                b=sum(P); a=sum((not P[i]) and P[(i+1)%8] for i in range(8))
                if not(2<=b<=6 and a==1): continue
                if st==0 and not(P[0] and P[2] and P[4]) and not(P[2] and P[4] and P[6]): weg.append((Y,X))
                if st==1 and not(P[0] and P[2] and P[6]) and not(P[0] and P[4] and P[6]): weg.append((Y,X))
            for p in weg: m[p]=False
            ver|=bool(weg)
    return m
S=dun(S)
lab,n=label(S,acht=True)
for i in range(1,n+1):
    m=lab==i; xs=np.where(m)[1]
    if m.sum()<(4 if xs.max()<=6 else SMIN): S[m]=False
STAT=S.copy()
# --- 5. kuif (MOET 5): vorm = silhouet van de reductie (model), alleen opnieuw ingekleurd: strengen midden-violet, lichtviolet alleen
#        binnenin (pixel zonder achtergrondbuur), selout alleen aan de onderkant/schaduwkant (achtergrond onder/rechts) als de streng daar >= 2 dik is;
#        dunne takjes (1 px) midden-violet. Kuifzone = KUIF van r2 + de strengen boven de kop (Y<=17, X22-34). ---
KZ=KUIF|(fig&(np.arange(64)[:,None]<=17)&(np.arange(64)[None,:]>=22)&(np.arange(64)[None,:]<=34))
v=o.copy()
for Y,X in zip(*np.where(KZ)):
    bU=not fig[Y-1,X]; bD=not fig[Y+1,X]; bL=not fig[Y,X-1]; bR=not fig[Y,X+1]
    dikV=fig[Y-1,X] or fig[Y+1,X]; dikH=fig[Y,X-1] or fig[Y,X+1]
    if (bD and fig[Y-1,X]) or (bR and fig[Y,X-1] and not bU and not bD): o[Y,X]=VS
    elif not (bU or bL or bD or bR): o[Y,X]=VL      # licht alleen binnenin de streng (geen lichte kleur op de buitenrand)
    else: o[Y,X]=VM
stap('kuif',v,o)
# --- 6. buitenlijn (MOET 1): geen zwart en geen navy. Wolk: wolk-selout L57 rondom (zoals de game-Altaria een donkere wolktint rondom);
#        kop/hals: violet-selout L53. Kuif heeft zijn eigen rand (stap 5). ---
v=o.copy(); uit=[]
for Y,X in zip(*np.where(fig&~KZ)):
    if any(not fig[Y+dy,X+dx] for dy,dx in N4): uit.append((Y,X,WS if o[Y,X] in VULW+[WS] else VS))
# r4: waar de buitenlijn een kap opeet (de modelkap ligt tegen de modelomlijning), schuift de kaptint 1 px naar binnen (onder, of opzij
# van de achtergrond af) als daar lijf (midden/donker) ligt; zo houden de vleugelbollen hun lichte kap onder de lijn
oud=o.copy(); rand=set((Y,X) for Y,X,_ in uit)
for Y,X,k in uit:
    if oud[Y,X] not in (WL,WH): continue
    for dy,dx in ((1,0),(0,1),(0,-1)):
        if fig[Y-dy,X-dx] and (dy,dx)!=(1,0): continue      # opzij alleen weg van de achtergrond
        yy,xx=Y+dy,X+dx
        if (yy,xx) not in rand and o[yy,xx] in (WM,WD): o[yy,xx]=oud[Y,X]; break
for Y,X,k in uit: o[Y,X]=k
stap('buitenlijn',v,o)
# --- 7. static op de modelplekken (stap 4). Op de buitenrand alleen de vonken buiten de vleugels (links x3-5, rechts x59-61: in het model
#        liggen die boogjes los naast de wolk); elders op de rand blijft de wolklijn. ---
v=o.copy()
for Y,X in zip(*np.where(STAT&fig)):
    rand=any(not fig[Y+dy,X+dx] for dy,dx in N4)
    if rand and not X<=5: continue          # r4: alleen de vonk links buiten de vleugel op de rand; de boog rechts is weg
    o[Y,X]=ST
lab,n=label(o==ST,acht=True)               # wat de buitenlijn heeft opgesplitst: stukjes < 4 px terug naar de wolktint eronder
for i in range(1,n+1):
    if (lab==i).sum()<4: o[lab==i]=v[lab==i]
stap('static',v,o)
# --- 8. kop (Y19-28): vlakken/plekken uit het model (blokwaarden in NOTITIES), alleen hier per pixel gezet omdat de reductie ogen/snavel wist.
#        Jordi: "let er bij altaria op dat het linkeroog ook zichtbaar moet zijn". Ver oog 1x2 zwart op X22 (model-oog X20.7-21.7 ligt tegen de
#        koprand X20): 1 px naar rechts zodat er lijn | kopkleur | oog staat (X20 | X21 | X22). Nabij oog 2x2 (X27-28, Y22-23) met glans
#        linksboven. Snavel (model X19-26, Y24-27): licht teal met hooglicht boven, mondlijn Y26 X24-26 naar de mondhoek (27,26), lichte
#        onderkaak Y27 X22-25 (model L118-165), omlijnd in wolk-selout (geen zwart). Wang (model X28-31, Y25-26) licht met hooglicht.
#        Kopschaduw: rechterrand X32 donkerviolet, onder de wang (Y27) donkerviolet (model L60). '.' = laten zoals de reductie. ---
KOPGRID={  # X19..33
19:'...slllllmmmms',
20:'..sllllllmmmms.',
21:'..sllllllmmmmms',
22:'.smKlllmWKmmmds',
23:'.smKmmmmKKmmmds',
24:'.oLHHHHLdmmmmds',
25:'oLHHHHLMdLHHLds',
26:'ooLLLooosLLLMds',
27:'.ooMLMMsdddddds',
28:'...oo.sddmms....',
}
KC={'s':VS,'d':VD,'m':VM,'l':VL,'K':PU,'W':GL,'o':WS,'D':WD,'M':WM,'L':WL,'H':WH}
v=o.copy()
for Y,row in KOPGRID.items():
    for j,ch in enumerate(row):
        X=19+j
        if ch=='.': continue
        assert fig[Y,X], (X,Y)          # silhouet blijft gelijk
        o[Y,X]=KC[ch]
for Y in (16,17,18):                     # kopbovenkant: wolk-selout uit de reductie in de kopzone -> violet-selout
    for X in range(22,34):
        if o[Y,X]==WS: o[Y,X]=VS
stap('kop',v,o)
# --- 9. losse wolkpixels (geen 8-buur van dezelfde tint, niet op de buitenrand, niet in de kop) -> meest voorkomende wolkbuurtint ---
v=o.copy()
for Y,X in zip(*np.where(np.isin(o,[WS]+VULW))):
    if any(not fig[Y+dy,X+dx] for dy,dx in N4) or (19<=X<=33 and 16<=Y<=28): continue
    if any(o[Y+dy,X+dx]==o[Y,X] for dy,dx in N8): continue
    nb=[o[Y+dy,X+dx] for dy,dx in N4 if o[Y+dy,X+dx] in [WS]+VULW]
    if nb: o[Y,X]=meest(nb)
stap('losse pixels',v,o)
# --- 10. dubbele lijn langs de hals: waar wolk-selout direct naast de violette halsrand ligt (Y29-40) is er één lijn genoeg (de halsrand);
#         de wolkpixel krijgt de meest voorkomende wolkvultint ernaast ---
v=o.copy()
for Y,X in zip(*np.where(np.isin(o,VULV))):   # de hals zelf krijgt een doorlopende violet-selout waar hij aan de wolk grenst (model: donkere halsrand)
    if 29<=Y<=40 and any(o[Y,X+dx] in [WS,ST]+VULW for dx in (-1,1)): o[Y,X]=VS
for Y,X in zip(*np.where(o==VM)):            # halsvolume (licht linksboven): naast de linker halsrand lichtviolet, naast de rechter donkerviolet
    if not (29<=Y<=40): continue
    if o[Y,X-1]==VS and o[Y,X+1] in VULV: o[Y,X]=VL
    elif o[Y,X+1]==VS and o[Y,X-1] in VULV: o[Y,X]=VD
for Y,X in zip(*np.where(o==WS)):
    if not (29<=Y<=40) or any(not fig[Y+dy,X+dx] for dy,dx in N4): continue
    if not any(o[Y,X+dx] in (VS,VD,VM) for dx in (-1,1)): continue
    nb=[o[Y+dy,X+dx] for dy,dx in N8 if o[Y+dy,X+dx] in VULW]
    if nb: o[Y,X]=meest(nb)
o[(np.arange(64)[:,None]>=41)&np.isin(o,VULV+[VS])]=WS     # halspuntje onder de wolkrand (1 px) hoort bij de wolklijn
stap('halsrand',v,o)
# --- 11. r5 vleugels (coördinator: "Label de bollen in het model ... geef elke bol in de sprite een eigen kap van minstens 3x2 px:
#         hooglicht/licht linksboven, midden als tussenstap, donkere onderboog die tegelijk de naad naar de volgende bol is" / "Rand: volg per
#         bol de bolling van het model: ... dip een inham van 1 px, op de bol een ronde bult"). Bollen en kappen gemeten op natief_kop15_dy10
#         (blokdekking en blokhelderheid per spritepixel, tabel in NOTITIES.md); per bol: plek van de modelkap (blok-L >= ±150), onderboog
#         = donkere modelband onder de kap. Tekens: . achtergrond, s wolk-selout, 0 donker, 1 midden, 2 licht, 3 hooglicht.
VL5={  # linkervleugel: L1 (X6-8,Y17-18), L2 (X11-13,Y19-20), L3 (X15-17,Y21-22), L4 (X16-18,Y24-25), L5 (X7-9,Y22-23), L6 (X11-13,Y23-24)
 16:{8:'s'},
 17:{6:'3',7:'3',8:'2',9:'s'},
 18:{6:'2',7:'2',8:'1',9:'s',10:'.',11:'s',12:'s',13:'s'},
 19:{6:'1',7:'1',8:'0',9:'0',10:'s',11:'3',12:'3',13:'2',14:'s'},
 20:{7:'0',8:'0',9:'0',10:'1',11:'2',12:'2',13:'1',14:'s',15:'s',16:'s'},
 21:{7:'1',8:'1',9:'1',10:'0',11:'0',12:'0',13:'0',14:'1',15:'3',16:'3',17:'s',18:'s'},
 22:{7:'3',8:'3',9:'2',10:'1',11:'1',12:'1',13:'0',14:'0',15:'2',16:'2',17:'2',18:'s'},
 23:{7:'2',8:'2',9:'1',10:'1',11:'2',12:'2',13:'1',14:'0',15:'0',16:'0',17:'0'},
 24:{11:'2',12:'1',13:'0',16:'2',17:'2',18:'1'},
 25:{12:'0',13:'0',16:'2',17:'1',18:'1'},
 26:{15:'0',16:'0',17:'0',18:'0'},
}
VR5={  # rechtervleugel: R1 punt (X56-59,Y17-18), Ra (X47-51,Y21-22), Rb (X44-47,Y22-23), Rc (X40-43,Y25-26), Rd (X42-44,Y27-28)
 17:{57:'3',58:'3',59:'2'},
 18:{56:'2',57:'2',58:'2',59:'0'},
 19:{56:'0',57:'0',58:'0'},
 21:{47:'3',48:'3',49:'2',50:'2',51:'1'},
 22:{46:'3',47:'2',48:'2',49:'2',50:'1',51:'0'},
 23:{44:'2',45:'2',46:'3',47:'1',48:'0',49:'0',50:'0'},
 24:{43:'1',44:'0',45:'0',46:'0',47:'0'},
 25:{41:'3',42:'3',43:'1'},
 26:{40:'2',41:'2',42:'2',43:'0',44:'0'},
 27:{40:'0',41:'0',42:'2',43:'2',44:'1'},
 28:{42:'2',43:'1',44:'1'},
 29:{42:'0',43:'0',44:'0',45:'0'},
}
TK={'.':0,'s':WS,'0':WD,'1':WM,'2':WL,'3':WH}
v=o.copy(); ALPHA5=[]
for naam,grid in (('links',VL5),('rechts',VR5)):
    for Y,row in grid.items():
        for X,ch in row.items():
            assert o[Y,X] in [0,WS]+VULW, (naam,X,Y,o[Y,X])      # nooit kuif, kop, hals of static
            if (o[Y,X]>0)!=(TK[ch]>0): ALPHA5.append((naam,X,Y,'+' if TK[ch] else '-'))
            o[Y,X]=TK[ch]
stap('vleugelbollen',v,o)
if __name__=='__main__':
    G.opslaan(o,UIT+'/altaria_r5.png'); print(tel); toon(o)
    im=G.rgb(o,(255,255,255)); im.resize((512,512),Image.NEAREST).save(UIT+'/altaria_r5_8x.png')
